#load a python script as a module
import sys
sys.path.append('./rootfold/')
import os
import global_main

#set the working directory
os.chdir('./rootfold/')
global_main.mainpage()
