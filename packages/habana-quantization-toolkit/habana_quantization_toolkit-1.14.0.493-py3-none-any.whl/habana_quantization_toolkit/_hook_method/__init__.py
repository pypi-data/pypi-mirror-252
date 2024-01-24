
import os

import torch.distributed

import torch.nn as nn
from .._quant_common.quant_config import Fp8cfg, QuantMode
config = Fp8cfg().cfg
from .common import mod_default_dict
assert len(config['mod_dict']) == 0, f"Custom modules are not supported: {config['mod_dict'].keys()}. Please add it in the code."
config['mod_dict'].update({k: mod_default_dict[k].type for k in mod_default_dict})

from .measure import prepare_model as prepare_model_for_measure
from .quantize import quantize_hooks
from .scale import scaling_params, scale_method_mapping
from .._quant_common.helper_modules import *




def is_substr(substr_list, target):
  return any([x in target for x in substr_list])

def prepare_model(model):
  whitelist=set(config['mod_dict'].keys())
  blacklist=set()
  for type_st in config['blacklist']['types']:
    blacklist.add(type_st)
  whitelist.difference_update(blacklist)
  whitelist_tuple=tuple(whitelist)
  mod_list=[]
  for name, mod in model.named_modules():
    mod_type=mod.__class__.__name__
    if (mod_type in whitelist_tuple) and (is_substr(config['whitelist']['names'], name) or len(config['whitelist']['names'])==0) and (not is_substr(config['blacklist']['names'], name)):
      mod_list.append(name)
    if config['verbose']:
        print(f"Module list: {mod_list}")
  print(f"Total modules : {len(mod_list)}")
  if (config['mode']==QuantMode.MEASURE) or (config['mode']==QuantMode.SHAPE):
    return prepare_model_for_measure(model, mod_list)
  elif config['mode']==QuantMode.QUANTIZE:
    scaling_method_name = scale_method_mapping[(config['scale_method'], config['observer'])]
    scaling_params[scaling_method_name].update(config['scale_params'])
    config['scale_params'] = scaling_params[scaling_method_name]
    return quantize_hooks(model, mod_list)

