# python3 fusesoc-sweep.py <core_name> 

import sys
import os
import yaml

user = os.getlogin()
path = "/Users/"+user+"/.cache/fusesoc/"

def main():

  core_name = sys.argv[1]
  
  core_file = open("fusesoc_libraries/basejump/bsg_misc/{}.core".format(core_name))
  parsed_yaml_file = yaml.load(core_file, Loader=yaml.FullLoader)
  path_in_core = parsed_yaml_file["filesets"]["makefile"]["files"][0]
  version = str(parsed_yaml_file["name"]).split(":")[-1]

  dirname = core_name+"_"+version
  path_to_makefile = os.path.join(path,dirname,path_in_core)

  with open(path_to_makefile) as f:
    file = f.readlines()

  k = file.index("#param\n")
  param=[]

  for i in range(k+1,len(file)):
    if file[i]!="#endparam\n":
      param.append(file[i])
    else:
      break
  
  print(param)

  
  # with open("/Users/adithyasunil/.cache/fusesoc/bsg_counter_up_down_0-r1/testing/bsg_misc/bsg_counter_up_down/Makefile","rt") as f:
  #   file = f.readlines()
  # print(file)




  # for root, dirs, files in os.walk(path, topdown=True):
  #   for name in files:
		  # print(os.path.join(root,name))
    # print("check3")
    # print(root+files)
    # if(files.startswith(str(core_name))):
    #   print(os.path.join("~/.cache/fusesoc/", file))

if __name__ == "__main__":
  main()