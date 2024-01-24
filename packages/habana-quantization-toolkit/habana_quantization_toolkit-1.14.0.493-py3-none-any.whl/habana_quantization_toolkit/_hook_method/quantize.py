import torch
import torch.nn as nn
from os import environ
import habana_frameworks.torch.core as htcore
from collections import namedtuple
from .._quant_common.helper_modules import quant_dequant
from .._quant_common.quant_config import Fp8cfg
from .measure import load_measurements
from .scale import scale_method_mapping, get_config, scaling_methods, scale_convert_methods
from .common import mod_default_dict

config = Fp8cfg().cfg

mod_inst_info = namedtuple('ModInstInfo', ['name', 'parent'])

parent_child_mod_dict={}
def generate_model_info(model):
  def create_mod_info_recursion(parent):
    for name, mod in parent.named_children():
      parent_child_mod_dict[mod]=mod_inst_info(name=name, parent=parent)
      create_mod_info_recursion(mod)
  create_mod_info_recursion(model)

def patch_module(mod, qconfig, mod_dict):
    parent=parent_child_mod_dict[mod].parent
    name=parent_child_mod_dict[mod].name
    patched_mod=mod_dict[mod.__class__.__name__].patched_module(mod, qconfig, name)
    setattr(parent, name, patched_mod)


def prepare_model(model, qconfig, mod_list, hp_dtype=torch.float):
    patched_modules = []
    patched_module_types = set()
    with (torch.no_grad()):
        for name, mod in model.named_modules():
            if name in mod_list:
                mod_config=qconfig[name]
                for param in mod_config.params:
                    param_config=mod_config.params[param]
                    p=getattr(mod, param)
                    pq=quant_dequant(p.to("hpu"), scale_quant_fcn=param_config.scale_quant_fcn, quant_fcn=param_config.quant_fcn, scale_dequant_fcn=param_config.scale_dequant_fcn, dequant_fcn=param_config.dequant_fcn)
                    delattr(mod, param)
                    setattr(mod, param, nn.Parameter(pq))
                    pq = getattr(mod, param)
                    pq.requires_grad_(False)
                    htcore.mark_step()
                patch_module(mod, mod_config, mod_default_dict)
                patched_modules.append(name)
                patched_module_types.add(type(mod))
    if config['verbose']:
        print("Patched module types: ", patched_module_types)
        print("Patched modules: ", patched_modules)
        print("Total patched modules: ", len(patched_modules))
    # print(f"Maximal quantization error {max_quant_error}, in module {max_quant_error_mod}")
    pass


def quantize_hooks(model, mod_list):
    environ['USE_SCALE'] = '1' # TODO SW-166049 remove once tpc libs use scale by deafult
    generate_model_info(model)
    hp_dtype = config['hp_dtype']
    lp_dtype = config['fp8_config']
    measurement=load_measurements(config['measure_file'])
    # FIXME make sure this takes unit_scale or measured scale, from Configs
    scaling_method_name=scale_method_mapping[(config['scale_method'], config['observer'])]
    scaling_method = scaling_methods[scaling_method_name]
    scale_convert_method = scale_convert_methods[scaling_method_name]
    params = config['scale_params']
    params['hp_dtype'] = hp_dtype
    params['lp_dtype'] = lp_dtype
    qconfig = get_config(model, measurement, mod_default_dict, scaling_method, scale_convert_method, params, config['scale_file'], False, mod_list)
    prepare_model(model, qconfig, mod_list, hp_dtype=hp_dtype)
