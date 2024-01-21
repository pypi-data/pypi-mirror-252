#load a python script as a module
import os
import sys
import platform

if platform.system()!='Linux':
    print("Current version is not supported on "+platform.system()+". Consider checking for updates.")
    exit()

module_path = os.path.abspath(__file__)
module_root = os.path.dirname(module_path)
sys.path.append(module_root)
sys.path.append(module_root+'/'+'rootfold')
os.chdir(module_root)

import main
