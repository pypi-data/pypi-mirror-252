import json
import os
import torch
import functools
import numpy as np
import torch.nn as nn
import importlib.util
import habana_frameworks.torch.core as htcore

from .._quant_common.quant_config import Fp8cfg, QuantMode, ScaleMethod
from .common import *

config = Fp8cfg().cfg
imod_dict = {}
gmod_list = []

class MeasureControl:
  def __init__(self, mod, name, observer_class, mod_type, d_shape=None, params=None):
    self.name=name
    self.mod=mod
    self.input_observer=[observer_class('input%d'%(i), mod, None if d_shape is None else d_shape.inputs[i], params=None if params is None else params.inputs[i]) for i in range(mod_type.inputs)]
    self.output_observer = observer_class('output', mod, None if d_shape is None else d_shape.outputs, params=None if params is None else params.outputs)
    self.params_observer = {param_name: observer_class(param_name, mod, None if d_shape is None else d_shape.params[param_name], params=None if params is None else params.params[param_name]) for param_name in mod_type.params}

def prepare_model(model, mod_list=None):
    observer_class = observer_types[config['observer']]
    if (config['shape_file'] is not None) and (observer_class!=ShapeObserver):
      shapes_fname = config['shape_file'] + '.json'
      d_shapes=load_file(shapes_fname, ShapeList, False)
    else:
      d_shapes=None
    gmod_list.extend(mod_list)
    register_hooks(model, mod_list, observer_class, d_shapes)

def register_hooks(model, mod_list, observer_class, d_shapes=None):
    patched_types = set()
    non_patched_types = set()
    patched_modules = []
    with torch.no_grad():
        for name, mod in model.named_modules():
            if (name in mod_list) or (mod_list is None):
                imod_dict[mod] = name
                mod_type_str=mod.__class__.__name__
                mod_type=config['mod_dict'][mod_type_str]
                params=observer_params[config['observer']][mod_type] if (config['observer'] in observer_params) and (mod_type in observer_params[config['observer']]) else None
                patched_types.add(type(mod))

                mod.__measure_control = MeasureControl(mod, name, observer_class, mod_types[mod_type], d_shapes[name] if ((d_shapes is not None) and (name in d_shapes)) else None, params)
                mod.register_forward_pre_hook(
                    functools.partial(
                        measure_input_hook, observer=mod.__measure_control.input_observer
                    )
                )
                mod.register_forward_hook(
                    functools.partial(
                        measure_output_hook, observer=mod.__measure_control.output_observer
                    )
                )
                for param_name in mod.__measure_control.params_observer:
                  param=getattr(mod, param_name)
                  param.to("hpu")
                  mod.__measure_control.params_observer[param_name].measure(param)
                  htcore.mark_step()
            if observer_class==SaveObserver:
                save_module(mod)
            patched_modules.append(name)
        else:
            non_patched_types.add(type(mod))
    if config['verbose']:
        print("Patched module types: ", patched_types)
        print("None-patched module types: ", non_patched_types)
        print("Patched modules: ", patched_modules)
        print("Total patched modules: ", len(patched_modules))


def get___measure_control_dict(model):
  mcd = {}
  for name, mod in model.named_modules():
    if hasattr(mod, '__measure_control'):
      mcd[name]=mod.__measure_control
  return mcd

def __measure_control_to_state_dict(mcd):
  sd={}
  sdl = {}
  for mname in mcd:
    sd[mname]={'inputs': [mcd[mname].input_observer[i].state.detach().cpu().float().numpy() for i in range(len(mcd[mname].input_observer)) if mcd[mname].input_observer[i].state is not None]}
    sdl[mname] = {'inputs': [mcd[mname].input_observer[i].state.detach().cpu().float().numpy().tolist() for i in range(len(mcd[mname].input_observer)) if mcd[mname].input_observer[i].state is not None]}
    if mcd[mname].output_observer.state is not None:
      sd[mname]['outputs'] = mcd[mname].output_observer.state.detach().cpu().float().numpy()
      sdl[mname]['outputs'] = mcd[mname].output_observer.state.detach().cpu().float().numpy().tolist()
    if len(mcd[mname].params_observer)>0:
      sd[mname]['params']=dict()
      sdl[mname]['params'] = dict()
      for param_name in mcd[mname].params_observer:
        if mcd[mname].params_observer[param_name].state is not None:
          sd[mname]['params'][param_name] = mcd[mname].params_observer[param_name].state.detach().cpu().float().numpy()
          sdl[mname]['params'][param_name] = mcd[mname].params_observer[param_name].state.detach().cpu().float().numpy().tolist()
  return sd, sdl

def save_measurements(model, fname=None):
  if config['mode'] in [QuantMode.MEASURE,QuantMode.SHAPE]:
    if (fname is None):
      if ('measure_file' in config) and (config['measure_file'] is not None):
        fname_base=config['measure_file']
        measure_type='DynamicRange'
      elif ('shape_file' in config) and (config['shape_file'] is not None) and (config['observer'] == 'shape'):
        fname_base = config['shape_file']
        measure_type='Shape'
      fname_np = fname_base + '.npz'
      fname_list = fname_base + '.json'
    else:
      print("fname is not None")
      return
    mcd = get___measure_control_dict(model)
    sd, sdl = __measure_control_to_state_dict(mcd)

    save_file(sd, np.ndarray, fname_np, measure_type)
    save_file(sdl, list, fname_list, measure_type)
    save_json(gmod_list, fname_base+'_mod_list.json')

def load_measurements(fname):
  source_fname=fname if fname is not None else config['measure_file']
  fname_np = source_fname + '.npz'
  d = load_file(fname_np, np.ndarray, fail_on_file_not_exist=config['scale_method'] not in [ScaleMethod.WITHOUT_SCALE, ScaleMethod.UNIT_SCALE])
  from collections import defaultdict
  d = defaultdict(lambda:None, d)

  return d


def get_default_config(mod_list):
    config = {k: "default" for k in mod_list}
    return config


def save_json(d, fname):
    with open(fname, "w") as f:
        json.dump(d, f, indent=4)


def load_json(fname):
    with open(fname, "r") as f:
        d = json.load(f)
    return d


def measure_input_hook(module, input, observer):
  # print('measure_input_hook')
  for i in range(len(observer)):
    observer[i].measure(input[i])

def measure_output_hook(module, input, output, observer):
  # print('measure_output_hook')
  observer.measure(output)

class MaxAbsObserver:
  def __init__(self, name, mod, d_shape=None, params=None):
    self.name=name
    self.mod=mod
    self.first=True
    self.state=None
    self.state=self.init_state_from_shape(d_shape)

  def init_state(self, x):
    device=x.device
    state = torch.zeros((1, 1), device=device, dtype=torch.float32)
    self.shape=list(x.shape)
    return state

  def init_state_from_shape(self, x_shape, device="hpu"):
    state = torch.zeros((1, 1), device=device, dtype=torch.float32)
    self.first = False
    return state

  def update_state(self, x):
    self.state.copy_(torch.maximum(torch.max(torch.abs(x)), self.state))

  def measure(self, x):
    if self.first:
      self.state=self.init_state(x)
      self.first=False
    self.update_state(x)

class MaxAbsPerChannelObserver:
  def __init__(self, name, mod, d_shape=None, params=None):
    self.name=name
    self.mod=mod
    self.first=True
    self.state=None
    self.dim=params['dim'] if (params is not None) and ('dim' in params) else -1
    if d_shape is not None:
      p=list(range(len(d_shape)))
      self.dim=self.dim if self.dim>=0 else len(d_shape)+self.dim
      p[-1]=self.dim
      p[self.dim]=len(d_shape)-1
      self.p=p
      self.state=self.init_state_from_shape(d_shape)

  def init_state(self, x):
    device=x.device
    Nch = x.shape[self.dim]
    self.Nch=Nch
    state = torch.zeros((Nch, 1), device=device, dtype=torch.float32)
    self.shape=list(x.shape)
    return state

  def init_state_from_shape(self, x_shape, device="hpu"):
    device=device
    Nch = x_shape[self.dim]
    self.Nch=Nch
    state = torch.zeros((Nch, 1), device=device, dtype=torch.float32)
    self.first = False
    return state

  def update_state(self, x):
    self.state.copy_(torch.maximum(torch.max(torch.abs(x.permute(self.p).reshape([-1, self.Nch])), dim=0, keepdim=True)[0].t(), self.state))

  def measure(self, x):
    if self.first:
      self.state=self.init_state(x)
      self.first=False
    self.update_state(x)

def save_module(mod):
  folder_name = os.path.join(config['dump_stats_base_path'], 'tensors')
  os.makedirs(folder_name, exist_ok=True)
  file_base_name = os.path.join(folder_name, imod_dict[mod] + '_module.pt')
  torch.save(mod.state_dict(), file_base_name)


class SaveObserver:
  def __init__(self, name, mod, d_shape=None, params=None):
    self.name=name
    self.mod=mod
    self.first = True
    self.cnt = -1
    self.folder_name=os.path.join(config['dump_stats_base_path'], 'tensors')
    os.makedirs(self.folder_name, exist_ok=True)
    self.file_base_name=os.path.join(self.folder_name, imod_dict[mod]+'_'+name+'_iter')
    self.state=self.init_state_from_shape(d_shape)

  def init_state(self, x):
    device=x.device
    state = torch.zeros((1, 1), device=device, dtype=torch.float32)
    self.shape=list(x.shape)
    return state

  def init_state_from_shape(self, x_shape, device="hpu"):
    state = torch.zeros((1, 1), device=device, dtype=torch.float32)
    self.first = False
    return state

  def update_state(self, x):
    self.cnt+=1
    torch.save(x, self.file_base_name+str(self.cnt)+'.pt')

  def measure(self, x):
    self.update_state(x)


class ShapeObserver:
  def __init__(self, name, mod, d_shape=None, params=None):
    self.name=name
    self.mod=mod
    self.state=None

  def init_state(self, x):
    device=x.device
    Ndim = len(x.shape)
    self.Ndim=Ndim
    state = torch.tensor(x.shape, device=device, dtype=torch.int32).reshape((1, Ndim))
    return state

  def init_state_from_shape(self, x_shape, device="hpu"):
    print("ShapeObserver doesn't support init_state_from_shape")
    return

  def update_state(self, x):
    print("ShapeObserver doesn't support update_state")
    return

  def measure(self, x):
    self.state=self.init_state(x)

observer_types = {
                'shape': ShapeObserver,
                'maxabs': MaxAbsObserver,
                'maxabs_per_channel': MaxAbsPerChannelObserver,
                'save': SaveObserver
              }

observer_params = {
                  'maxabs_per_channel': {'linear': module_config(({'dim': -1},), {'dim': -1}, {'weight': {'dim': 0}}),
                                         'matmul': module_config(({'dim': -1},{'dim': -2}), {'dim': -1}, None)}
                  }
