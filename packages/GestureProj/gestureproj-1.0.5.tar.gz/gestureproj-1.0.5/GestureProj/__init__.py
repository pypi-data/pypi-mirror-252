#load a python script as a module
import os
import sys

module_path = os.path.abspath(__file__)
module_root = os.path.dirname(module_path)
sys.path.append(module_root)
sys.path.append(module_root+'/'+'rootfold')
os.chdir(module_root)

import main
