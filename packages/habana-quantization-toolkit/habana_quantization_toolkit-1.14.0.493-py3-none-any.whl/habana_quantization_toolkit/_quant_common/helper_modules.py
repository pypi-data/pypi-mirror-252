import torch.nn as nn
import torch
import math


class BMM(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x, y):
        return torch.bmm(x, y)

class MatMul(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, *args, **kwargs):
        return torch.matmul(*args, **kwargs)

class Identity(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x.clone()

class ScaledDotProductAttention(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, query, key, value, attn_mask=None, dropout_p=0.0,
    is_causal=False, scale=None) -> torch.Tensor:
        # Efficient implementation equivalent to the following:
        L, S = query.size(-2), key.size(-2)
        scale_factor = 1 / math.sqrt(query.size(-1)) if scale is None else scale
        attn_bias = torch.zeros(L, S, dtype=query.dtype)
        if is_causal:
            assert attn_mask is None
            temp_mask = torch.ones(L, S, dtype=torch.bool).tril(diagonal=0)
            attn_bias.masked_fill_(temp_mask.logical_not(), float("-inf"))
            attn_bias.to(query.dtype)

        if attn_mask is not None:
            if attn_mask.dtype == torch.bool:
                attn_mask.masked_fill_(attn_mask.logical_not(), float("-inf"))
            else:
                attn_bias += attn_mask
        attn_weight = query @ key.transpose(-2, -1) * scale_factor
        attn_weight += attn_bias
        attn_weight = torch.softmax(attn_weight, dim=-1)
        attn_weight = torch.dropout(attn_weight, dropout_p, train=True)
        return attn_weight @ value

def quant_dequant(
        x, scale_quant_fcn=None, quant_fcn=None, scale_dequant_fcn=None, dequant_fcn=None
):
  y = x if (scale_quant_fcn is None) else scale_quant_fcn(x)
  y = y if (quant_fcn is None) else quant_fcn(y)
  y = y if (dequant_fcn is None) else dequant_fcn(y)
  y = y if (scale_dequant_fcn is None) else scale_dequant_fcn(y)
  return y

def quant_dequant_config(x, config):
  return quant_dequant(x,
                       scale_quant_fcn=config.scale_quant_fcn,
                       quant_fcn=config.quant_fcn,
                       scale_dequant_fcn=config.scale_dequant_fcn,
                       dequant_fcn=config.dequant_fcn)

def matmul_fp8(input, other, out=None, out_dtype=torch.bfloat16, scale_input_inv=None, scale_other_inv=None):
  res = torch.ops.hpu.fp8_gemm_v2(input, False, other, False, out, out_dtype, scale_input_inv, scale_other_inv, None, False)
  return res

class PatchedMatmul(nn.Module):
  def __init__(self, mod, mod_config, name, *args, **kwargs):
    self.__dict__.update(mod.__dict__)
    self.name = name
    self._mod_config = mod_config
    self.scale_input = mod_config.scale.inputs[0]
    self.scale_other = mod_config.scale.inputs[1]

  def forward(self, input, other):
    qinput = quant_dequant_config(input,self._mod_config.inputs[0])
    qother = quant_dequant_config(other,self._mod_config.inputs[1])
    output = matmul_fp8(qinput, qother, out_dtype=self._mod_config.config_params['hp_dtype'], scale_input_inv=self.scale_input, scale_other_inv=self.scale_other)
    return output

class PatchedLinear(nn.Module):
  def __init__(self, mod, mod_config, name, *args, **kwargs):
    self.__dict__.update(mod.__dict__)
    self.name = name
    self._mod_config = mod_config
    self.scale_input = mod_config.scale.inputs[0]
    if isinstance(mod_config.scale.params['weight'], (torch.Tensor, float)):
      self.scale_weight = mod_config.scale.params['weight']
    elif isinstance(mod_config.scale.params['weight'], dict):
       # PCQ weight is calculated with actual weight [0] and ones [1]
       self.scale_weight = mod_config.scale.params['weight'][0]

  def forward(self, input):
    qinput = quant_dequant_config(input,self._mod_config.inputs[0])
    y = matmul_fp8(qinput, self.weight.t(), out_dtype=self._mod_config.config_params['hp_dtype'], scale_input_inv=self.scale_input, scale_other_inv=self.scale_weight)
    output = y+self.bias if (self.bias is not None) else y
    return output

class PatchedLinearAllReduce(nn.Module):
  def __init__(self, mod, mod_config, name, *args, **kwargs):
    self.__dict__.update(mod.__dict__)
    self.scoped_version =  mod.__class__.__name__ == "ScopedLinearAllReduce"
    self.name = name
    self._mod_config = mod_config
    self.scale_input = mod_config.scale.inputs[0]
    if isinstance(mod_config.scale.params['weight'], (torch.Tensor, float)):
      self.scale_weight = mod_config.scale.params['weight']
    elif isinstance(mod_config.scale.params['weight'], dict):
       # PCQ weight is calculated with actual weight [0] and ones [1]
       self.scale_weight = mod_config.scale.params['weight'][0]

  def forward(self, input):
    # pre_all_reduce
    qinput = quant_dequant_config(input,self._mod_config.inputs[0])
    output = matmul_fp8(qinput, self.weight.t(), out_dtype=self._mod_config.config_params['hp_dtype'], scale_input_inv=self.scale_input, scale_other_inv=self.scale_weight)
    dqoutput = quant_dequant_config(output, self._mod_config.outputs)
    if not self.scoped_version:
      self.all_reduce(dqoutput)
      dqoutput = self.post_all_reduce(dqoutput)
    return dqoutput

  def all_reduce(self, input):
    if self.mp_group is not None:
        from deepspeed import comm as dist
        dist.inference_all_reduce(input, group=self.mp_group)

  def post_all_reduce(self, input):
      output = input + self.bias if (self.bias is not None) else input
      return output

class PatchedLmHeadLinearAllreduce(nn.Module):
  def __init__(self, mod, mod_config, *args, **kwargs):
    self.__dict__.update(mod.__dict__)
    self._mod_config = mod_config
    self.scale_input = mod_config.scale.inputs[0]
    if isinstance(mod_config.scale.params['weight'], (torch.Tensor, float)):
      self.scale_weight = mod_config.scale.params['weight']
    elif isinstance(mod_config.scale.params['weight'], dict):
       # PCQ weight is calculated with actual weight [0] and ones [1]
       self.scale_weight = mod_config.scale.params['weight'][0]

  def forward(self, input):
      assert input.shape[
          -1] % self.world_size == 0, 'Please ensure that self.world_size is divisible by input.shape[-1]'
      input_shard = input.shape[-1] // self.world_size
      splittedInput = input[:, :, self.rank * input_shard:(self.rank + 1) * input_shard]
      qinput = quant_dequant_config(splittedInput, self._mod_config.inputs[0])
      output = matmul_fp8(qinput, self.weight.t(), out_dtype=self._mod_config.config_params['hp_dtype'], scale_input_inv=self.scale_input, scale_other_inv=self.scale_weight)
      dqoutput = quant_dequant_config(output, self._mod_config.outputs)

      if self.mp_group is not None:
          from deepspeed import comm as dist
          dist.inference_all_reduce(dqoutput, group=self.mp_group)
      if self.bias is not None:
          dqoutput += self.bias
      return dqoutput

class PatchedKVCache(nn.Module): # TODO SW-169816 utilize original module methods to reduce code duplication
    # Module to patch KVCache module from llama model
    def __init__(self, mod, mod_config, name, *args, **kwargs):
        super(PatchedKVCache, self).__init__()
        self.cache = None
        self.inp_seq_len = -1
        self._mod_config = mod_config

    # overwrite allocate function of original module to force allocation in fp8
    def allocate(self, inp_seq_len, kv_cache_fp8, dtype, device, shape):
        if self.cache is None or self.cache.shape != shape:
            self.inp_seq_len = inp_seq_len
            self.cache = torch.zeros(shape, dtype=torch.float8_e4m3fn, device=device)
        else:
            assert (
                    self.inp_seq_len == inp_seq_len
            ), f"inp_seq_len must be the same. self.inp_seq_len:{self.inp_seq_len} inp_seq_len:{inp_seq_len}"
            self.cache.fill_(0)

    def get_shape(self):
        if self.cache is None:
            return None
        return self.cache.shape

    # overwrite forward function of original module to force quant and dequant of cache input and output
    def forward(self, cur, dim, idx):
        qinput = quant_dequant_config(cur, self._mod_config.inputs[0])
        if cur.shape[2] > 1 and cur.shape[2] <= self.cache.shape[2]:
            # Initialize cache
            self.cache[:, :, :self.inp_seq_len, :].copy_(qinput)
            return cur
        assert cur.shape[2] == 1, f"Cannot update kv-cache. Unsupported shapes. cache:{self.cache.shape} cur:{cur.shape}"
        if idx is not None:
            self.cache.index_copy_(dim, idx - 1, qinput)
        else:
            torch.cat((self.cache, qinput), dim=dim)
        qoutput = quant_dequant_config(self.cache, self._mod_config.outputs)
        return qoutput
