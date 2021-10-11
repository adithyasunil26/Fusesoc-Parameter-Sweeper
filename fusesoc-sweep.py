# python3 fusesoc-sweep.py <core_name> 

import sys
import os
import yaml
import itertools
import numpy as np

user = os.getlogin()
path = "/home/"+user+"/.cache/fusesoc/"

def main():

  core_name = sys.argv[1]
  core_name_cpy = core_name+"_cpy"
  os.system("cp fusesoc_libraries/basejump/bsg_misc/{}.core fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name, core_name_cpy))
  core_file = open("fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name))
  parsed_yaml_file = yaml.load(core_file, Loader=yaml.FullLoader)
  path_in_core = parsed_yaml_file["filesets"]["makefile"]["files"][0]
  version = str(parsed_yaml_file["name"]).split(":")[-1]

  dirname = core_name+"_"+version
  path_to_makefile = os.path.join(path,dirname,path_in_core)

  with open(path_to_makefile) as f:
    file = f.readlines()

  k = file.index("#param\n")
  param = []

  for i in range(k+1,len(file)):
    if file[i]!="#endparam\n":
      param.append(file[i])
    else:
      break

  params = []
  for i in param:
    i = i.split(" = ")
    i[0] = i[0].replace(" ", "")
    i[1] = i[1].split("\n")[0]
    params.append(i)

  param_name = []
  param_values = []
  while len(params)!=0:
    k = params.pop()
    param_name.append(k[0].lower())
    param_values.append(k[1].split(" "))
  
  comb = list(itertools.product(*param_values))

  for i in range(len(comb)):
    core_file_write = open("fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name_cpy),'w')
    j = parsed_yaml_file["targets"]["verilator_tb"]["parameters"]
    k = j[0].split("=")
    k[1] = comb[i][0]
    j[0] = "=".join(k)
    k = j[1].split("=")
    k[1] = comb[i][1]
    j[1] = "=".join(k)
    k = j[2].split("=")
    k[1] = comb[i][2]
    j[2] = "=".join(k)
    parsed_yaml_file["targets"]["verilator_tb"]["parameters"] = j
    parsed_yaml_file["name"]=core_name_cpy
    yaml.dump(parsed_yaml_file,core_file_write)
    os. system('fusesoc run --target=verilator_tb {}'.format(core_name_cpy))

if __name__ == "__main__":
  main()