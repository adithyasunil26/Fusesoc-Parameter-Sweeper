# python3 fusesoc-sweep.py <core_name> 

import sys
import os
import yaml
import itertools
import numpy as np

MAX_VAL_P  = [1, 2, 3, 4]
INIT_VAL_P = [0, 1, 2, 3]
MAX_STEP_P = [2, 3, 4, 8]

param_name = ['MAX_VAL_P', 'INIT_VAL_P', 'MAX_STEP_P']
param_values = [MAX_VAL_P, INIT_VAL_P, MAX_STEP_P]

user = os.getlogin()
path = "/home/"+user+"/.cache/fusesoc/"

def crossproduct(param_values):
  return list(itertools.product(*param_values))

def main():
  core_name = sys.argv[1]
  core_name_cpy = core_name+"_cpy"
  os.system("cp fusesoc_libraries/basejump/bsg_misc/{}.core fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name, core_name_cpy))
  core_file = open("fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name))
  parsed_yaml_file = yaml.load(core_file, Loader=yaml.FullLoader)

  comb = crossproduct(param_values)

  for i in range(len(comb)):
    core_file_write = open("fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name_cpy),'w')
    j = parsed_yaml_file["targets"]["verilator_tb"]["parameters"]
    k = j[0].split("=")
    k[1] = str(comb[i][0])
    j[0] = "=".join(k)
    k = j[1].split("=")
    k[1] = str(comb[i][1])
    j[1] = "=".join(k)
    k = j[2].split("=")
    k[1] = str(comb[i][2])
    j[2] = "=".join(k)
    
    parsed_yaml_file["targets"]["verilator_tb"]["parameters"] = j
    parsed_yaml_file["name"]=core_name_cpy
    yaml.dump(parsed_yaml_file,core_file_write)
    os. system('fusesoc run --target=verilator_tb {}'.format(core_name_cpy))

if __name__ == "__main__":
  main()