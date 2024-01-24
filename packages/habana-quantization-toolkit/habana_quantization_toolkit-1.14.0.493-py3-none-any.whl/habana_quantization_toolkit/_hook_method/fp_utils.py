import torch
import habana_frameworks.torch.core as htcore
from .common import *

EXP_WIDTH={torch.float32: 8, torch.bfloat16: 8, torch.float8_e4m3fn: 4, torch.float8_e5m2: 5}
def get_default_exp_bias(dtype):
  exp_width=EXP_WIDTH[dtype]
  return (2**(exp_width-1)-1)

FP8_143_EXP_BIAS_SET = [3, 7, 11, 15]

MAX_RANGE = {
            torch.float32: 2**((2**8-2-get_default_exp_bias(torch.float32)))*(2-2**-(23)),
            torch.bfloat16: 2**((2**8-2-get_default_exp_bias(torch.bfloat16)))*(2-2**-(7)),
            torch.float8_e4m3fn: 2**((2**4-2-get_default_exp_bias(torch.float8_e4m3fn)))*(2-2**-(8-1-4)),
            torch.float8_e5m2: 2**((2**5-2-get_default_exp_bias(torch.float8_e5m2)))*(2-2**-(8-1-5)),
          }

def get_fullscale(dtype, exp_bias=None):
  default_exp_bias=get_default_exp_bias(dtype)
  fullscale=MAX_RANGE[dtype]
  exp_bias=default_exp_bias if exp_bias==None else exp_bias
  fullscale=fullscale*(2**(default_exp_bias-exp_bias))
  return fullscale

FP8_143_FULLSCALE=[get_fullscale(torch.float8_e4m3fn, exp_bias=eb) for eb in FP8_143_EXP_BIAS_SET]
FP8_143_SCALES=[x/MAX_RANGE[torch.float8_e4m3fn] for x in FP8_143_FULLSCALE]
FP8_143_MAX_SCALE=max(FP8_143_SCALES)
FP8_143_MIN_SCALE=min(FP8_143_SCALES)


def calc_maxabs_scale(xmaxabs, fullscale, backoff=1):
  scale=xmaxabs/(fullscale*backoff)
  return scale

def scale_to_pow2(scale):
  scale_pow2 = 2 ** torch.ceil(torch.log2(scale))
  return scale_pow2

def scale_to_pow2_hw(scale):
  scale_pow2=scale_to_pow2(scale)
  scale_pow2_hw=torch.minimum(torch.maximum(2**(torch.ceil(torch.log2(scale_pow2)/4)*4), torch.tensor(FP8_143_MIN_SCALE, dtype=scale.dtype, device=scale.device)), torch.tensor(FP8_143_MAX_SCALE, dtype=scale.dtype, device=scale.device))
  return scale_pow2_hw

def mmse_scale_multi(x, ref_scale, scales, lp_dtype, hp_dtype):
  Nch=x.shape[-1]
  opt_err = torch.ones(Nch, dtype=hp_dtype, device=x.device)*torch.inf
  opt_scale= torch.ones(Nch, dtype=hp_dtype, device=x.device)*-1
  sum_axis=list(range(x.ndim-1))
  rs=ref_scale.unsqueeze(dim=1).transpose(0, 1)
  for s in scales:
    sv = torch.ones(Nch, dtype=hp_dtype, device=x.device)*s
    xscales = rs*sv
    y=scale_fcn(x, xscales)
    y=cast_to_fp8_fcn(y, lp_dtype)
    y=cast_fcn(y, hp_dtype)
    y=descale_fcn(y, xscales)
    err=torch.sum((x-y)**2, dim=sum_axis)
    opt_scale=torch.where(err<opt_err, sv, opt_scale)
    opt_err = torch.where(err < opt_err, err, opt_err)
    htcore.mark_step()
  return opt_scale*ref_scale


def mmse_scale(x, scales, lp_dtype, hp_dtype):
  opt_err = torch.ones(1, dtype=hp_dtype, device=x.device)*torch.inf
  opt_scale= -1
  for s in scales:
    y=scale_fcn(x, s)
    y=cast_to_fp8_fcn(y, lp_dtype)
    y=cast_fcn(y, hp_dtype)
    y=descale_fcn(y, s)
    err=torch.norm(x-y)
    opt_scale=torch.where(err<opt_err, s, opt_scale)
    opt_err = torch.where(err < opt_err, err, opt_err)
    htcore.mark_step()
  return opt_scale

def manipulate_scales(scales, func):
  new_inputs = [func(input) for input in scales.inputs]
  new_weights = {}
  if 'weight' in scales.params.keys():
    if isinstance(scales.params['weight'], (torch.Tensor, float)):
      new_weights = {'weight' : func(scales.params['weight'])}
    elif isinstance(scales.params['weight'], dict):
      new_weights_dict = {}
      for key, wt in scales.params['weight'].items():
        new_weights_dict[key] = func(wt)
      new_weights = {'weight' : new_weights_dict}
  new_scales = module_config((new_inputs), func(scales.outputs), new_weights)
  return new_scales

def invert_scales(scales):
  def invert(x):
    if isinstance(x, (list, tuple)):
      return [1 / x_i for x_i in x]
    return 1 / x
  return manipulate_scales(scales, invert)

def scales_to_scalar(scales):
  def scale_to_scalar(scale):
    if scale.dim() == 0:
      return scale.item()
    # TODO SW-169781: Uncomment and fix this for PCQ
    # return scale.tolist()
    return scale
  return manipulate_scales(scales, scale_to_scalar)

# TODO SW-169781: Remove this for PCQ and use scales_to_scalar instead
def pass_scales(scales):
  return scales
