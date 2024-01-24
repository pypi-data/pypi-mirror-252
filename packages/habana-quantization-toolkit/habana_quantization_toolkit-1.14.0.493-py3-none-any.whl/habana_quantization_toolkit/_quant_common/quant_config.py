import json
import os
import sys
import torch
from enum import Enum
from json.decoder import JSONDecodeError

VERBOSE = os.environ.get('QUANT_VERBOSE') is not None

local_rank = int(os.getenv('LOCAL_RANK', '-1'))
world_size = int(os.getenv('WORLD_SIZE', '-1'))
global_rank = int(os.getenv('RANK', '-1'))

class ToolMethod(Enum):
    NONE = 0
    HOOKS = 1
    MODULES = 2

class QuantMode(Enum):
    NONE = 0
    QUANTIZE = 1
    MEASURE = 2
    SHAPE = 3

class ScaleMethod(Enum):
    MAX = 1
    WITHOUT_SCALE = 2
    UNIT_SCALE = 3
    MAXABS_HW = 4
    MAXABS_POW2 = 5
    SMOOTHQUANT_WEIGHTS_OUTPUT_CHANNEL_MAXABS_POW2 = 6
    WEAKSMOOTHQUANT_WEIGHTS_OUTPUT_CHANNEL_MAXABS_POW2 = 7
    ACT_MAXABS_HW_WEIGHTS_PCS_MAXABS_POW2 = 8
    ACT_MAXABS_HW_WEIGHTS_PCS_OPT_POW2 = 9
    ACT_MAXABS_POW2_WEIGHTS_PCS_MAXABS_POW2 = 10
    ACT_MAXABS_POW2_WEIGHTS_PCS_OPT_POW2 = 11
    SMOOTHQUANT_OPT = 12


class Fp8cfg():
    _instance = None


    def __init__(self):
        # Default config:
        if hasattr(self._instance, 'cfg'):
            return
        measured_global_config = {
            'method': ToolMethod.NONE, # Whether the tool will use the hook method for measurement+quant, or replace modules
            'dump_results': {'dump': False, 'out_path': 'experiments/'}, # Flag to dump experiment results, and specify where to dump
            'dump_stats_path': 'stats',
                # Where to dump measurement statistics (Path is different from out_path to enable reuse of statistics between experiments)
            'dump_stats_xlsx_path': 'stats.xlsx',# Where to dump excel containing statistics for analysis
            'history_len': 350, # The length of the measurements statistics tensor
            'collect_mse': {'collect': False},
                # If collect is set to true, the qdq mse will be collected and dumped to out_path
            'check_std': {'check': False,'limit': 0.2}, # If check is set to true, layers with std
                #larger than limit will not be quantized
            'stochastic': True,  # Stochastic rounding during to_fp8 casting
            'fp8_config': torch.float8_e4m3fn, # The parameters of the chosen Quantization methed
            'hp_dtype': torch.bfloat16, # The parameters of the chosen Quantization methed
            'clip': True, # Clip to max value before quantization
            'blacklist': {'names': [''], 'types': ()}, # types and names to not be quantized
            'whitelist': {'names': [''], 'types': ('torch.nn.Linear', 'torch.nn.Conv2d', 'BMM')}, \
                # types and names to be quantized. Whitelist by names is not yet implemented
            'mode': QuantMode.QUANTIZE, # Quantize or Measure
            'sweep_mse': False, # sweep scales in a brute force manner to find optimal scales for MSE
            'scale_method': ScaleMethod.WITHOUT_SCALE, # Method to quantize with
            'scale_params': {}, # scaling parameters that are different then the default ones
            'fake_quant': False,
# Additional Hooks method paramters:
            'observer': 'maxabs', # Supported ['shape', 'maxabs', 'maxabs_per_channel', 'save']
            'mod_dict': {},
            'local_rank': local_rank if local_rank>=0 else None,
            'global_rank':None,
            'world_size': world_size if world_size >= 0 else None,
            'verbose': VERBOSE # print extra info. TODO SW-166341 can turn it to log level configuration
        }
        # assert measured_global_config['whitelist']['names'] == [''], "Whitelist names not yet implemented"
        custom_config_name = str(os.getenv('QUANT_CONFIG'))
        print(f"QUANT PACKAGE: using {custom_config_name} config")
        module_directory = os.path.dirname(os.path.abspath(__file__))

        # if file in absolute path doesn't exist, try looking in cfg directory
        if not os.path.isfile(custom_config_name):
            custom_config_name = os.path.join(module_directory, '..', f'custom_config/{custom_config_name}.json')
        try:
            print(f"QUANT PACKAGE: Loading {custom_config_name}")
            with open(custom_config_name) as custom_config_json:
                custom_config = json.load(custom_config_json)
        except FileNotFoundError as e:
            raise Exception(f"Got exception: {e}. QUANT PACKAGE: Can't open {custom_config_name}!")
        except JSONDecodeError as e:
            custom_config_json.close()
            raise Exception(f"Got exception: {e}. QUANT PACKAGE: Can't load {custom_config_name} json!")

        # go over all user-defined keys from json, handle various cases
        for keys in custom_config:
            if keys == 'mode':
                if custom_config[keys] == 'NONE':
                    custom_config[keys] = QuantMode.NONE
                elif custom_config[keys] == 'QUANTIZE':
                    custom_config[keys] = QuantMode.QUANTIZE
                elif custom_config[keys] == 'MEASURE':
                    custom_config[keys] = QuantMode.MEASURE
                elif custom_config[keys] == 'SHAPE':
                    custom_config[keys] = QuantMode.SHAPE
                else:
                    raise ValueError('invalid mode in custom config. Enter Quantize or Measure')

            if keys == 'method':
                if custom_config[keys].lower() == 'hooks':
                    custom_config[keys] = ToolMethod.HOOKS
                elif custom_config[keys].lower() == 'modules':
                    custom_config[keys] = ToolMethod.MODULES
                else:
                    raise ValueError('invalid method in custom config. Enter Hooks or Modules')


            if keys == 'fp8_config':
                if custom_config[keys].lower() == 'e4m3':
                    custom_config[keys] = torch.float8_e4m3fn

                elif custom_config[keys].lower() == 'e5m2':
                    custom_config[keys] = torch.float8_e5m2
                else:
                    raise ValueError('invalid fp8_config in custom config. Enter E4M3 or E5M2')

            if keys == 'scale_method':
                if custom_config[keys].lower() == 'without_scale':
                    custom_config[keys] = ScaleMethod.WITHOUT_SCALE
                elif custom_config[keys].lower() == 'unit_scale':
                    custom_config[keys] = ScaleMethod.UNIT_SCALE
                elif custom_config[keys].lower() == 'max':
                    custom_config[keys] = ScaleMethod.MAX
                elif custom_config[keys].lower() == 'maxabs_hw':
                    custom_config[keys] = ScaleMethod.MAXABS_HW
                elif custom_config[keys].lower() == 'maxabs_pow2':
                    custom_config[keys] = ScaleMethod.MAXABS_POW2
                elif custom_config[keys].lower() == 'smoothquant_weights_output_channel_maxabs_pow2':
                    custom_config[keys] = ScaleMethod.SMOOTHQUANT_WEIGHTS_OUTPUT_CHANNEL_MAXABS_POW2
                elif custom_config[keys].lower() == 'weaksmoothquant_weights_output_channel_maxabs_pow2':
                    custom_config[keys] = ScaleMethod.WEAKSMOOTHQUANT_WEIGHTS_OUTPUT_CHANNEL_MAXABS_POW2
                elif custom_config[keys].lower() == 'act_maxabs_hw_weights_pcs_maxabs_pow2':
                    custom_config[keys] = ScaleMethod.ACT_MAXABS_HW_WEIGHTS_PCS_MAXABS_POW2
                elif custom_config[keys].lower() == 'act_maxabs_hw_weights_pcs_opt_pow2':
                    custom_config[keys] = ScaleMethod.ACT_MAXABS_HW_WEIGHTS_PCS_OPT_POW2
                elif custom_config[keys].lower() == 'act_maxabs_pow2_weights_pcs_maxabs_pow2':
                    custom_config[keys] = ScaleMethod.ACT_MAXABS_POW2_WEIGHTS_PCS_MAXABS_POW2
                elif custom_config[keys].lower() == 'act_maxabs_pow2_weights_pcs_opt_pow2':
                    custom_config[keys] = ScaleMethod.ACT_MAXABS_POW2_WEIGHTS_PCS_OPT_POW2
                elif custom_config[keys].lower() == 'smoothquant_opt':
                    custom_config[keys] = ScaleMethod.SMOOTHQUANT_OPT
                else:
                    raise ValueError(f'Invalid fp8_config in custom config ({custom_config[keys]}). should be in ["without_scale", "unit_scale", "max", "maxabs_hw", "maxabs_pow2", "maxabs_per_channel_pow2", "smoothquant_opt"]')

            if isinstance(custom_config[keys],dict):
                for keys_2 in custom_config[keys]:
                    measured_global_config[keys][keys_2] = custom_config[keys][keys_2]
            else:
                measured_global_config[keys] = custom_config[keys]

        out_path = measured_global_config['dump_results']['out_path']
        os.makedirs(out_path, exist_ok=True)
        base_count = len(os.listdir(out_path))
        measured_global_config['dump_results']['out_path'] = os.path.join(out_path,f'exp_no_{base_count}/')

        if measured_global_config['method'] == ToolMethod.HOOKS:
            base_name=measured_global_config['dump_stats_path'].split('/')[-1]
            folder_name=measured_global_config['dump_stats_path'][:-(len(base_name))]
            measured_global_config['dump_stats_base_path']=folder_name
            os.makedirs(folder_name, exist_ok=True)
            worker_st='' if measured_global_config['local_rank']==None else '_'+str(measured_global_config['local_rank'])+'_'+str(measured_global_config['world_size'])
            measured_global_config['shape_file'] = measured_global_config['dump_stats_path'] + '_hooks_shape' + worker_st
            measured_global_config['scale_file'] = measured_global_config['dump_stats_path'] + '_hooks_'+ measured_global_config['observer']+'_'+measured_global_config['scale_method'].name+ worker_st
            if (measured_global_config['mode']==QuantMode.MEASURE) or (measured_global_config['mode']==QuantMode.QUANTIZE):
                measured_global_config['measure_file']=measured_global_config['dump_stats_path']+'_hooks_'+measured_global_config['observer']+worker_st
            # measured_global_config['dump_stats_path'] += '_hooks_.json'

        else:
            measured_global_config['dump_stats_path'] += '_modules_.pt'

        def print_paths():
            print("HQT Paths:")
            print(f"{base_name=}")
            print(f"{folder_name=}")
            print(f"{measured_global_config['shape_file']=}")
            print(f"{measured_global_config['scale_file']=}")
            if 'measure_file' in measured_global_config.keys():
                print(f"{measured_global_config['measure_file']=}")
            print(f"{measured_global_config['dump_stats_path']=}")
        if VERBOSE:
            print_paths()

        self.cfg = measured_global_config

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance
