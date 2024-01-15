#!/usr/bin/env python3

##
# Usage:
# mv_files.py -targ <targ> -kt KT -run1 <run1> -run2 <run2>
# Arguments:
#  -h, --help: Show this help message and exit
#  -targ <targ>: D, C, Fe, Sn, Pb
#  -kt : kt value parp(91)
#  -run1 <run1>: First run
#  -run2 <run2>: Last run

import os
import stat
import argparse
import shutil
import time
import datetime
import socket
import myfuncs

Targets = ["D", "C", "Fe", "Pb"]

now = datetime.datetime.now()
startTime = now.strftime("%d/%m/%Y %H:%M:%S")
print("Start Time: " + startTime)
timeStamp = myfuncs.getTimeStamp()

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-targ", required=True, help="D, C, Fe, Sn, Pb")
ap.add_argument("-kt", required=True, help="kt value")
ap.add_argument("-run1", required=True, help="first run")
ap.add_argument("-run2", required=True, help="last run")
myargs = vars(ap.parse_args())

targ = myargs['targ']
kt = myargs['kt']
run1 = myargs['run1']
run2 = myargs['run2']

##
print("targ: ", targ)
print("kt: ", kt)
print("run1: ", str(run1))
print("run2: ", str(run2))

if targ not in Targets:
  print("bad targ argument. Possible values are: " + str(Targets) + " \n")
  exit(0)

############################################################
############################################################
############################################################

gene = "gibuu"
expt = "clas6"
year = "2021"

hhome = os.environ['HOME']
topIndir = ""
topOudir = ""

#topIndir = "/work/clas12/ahmed/mc/" + gene + "/" + year + "/" + expt + "/lamdecON/" + targ + "/kt_" + kt + "/"
topIndir = hhome + "/mc/" + gene + "/" + year + "/" + expt + "/lamdecON/" + targ + "/kt_" + kt + "/"

if os.path.isdir(topIndir) is False:
  print(topIndir + " does not exists. Quit")
  exit(0)

print ("topIndir:", topIndir)

#loop over runs
for ir in range(int(run1), int(run2) + 1, 1):
  print("")
  srun = myfuncs.getRun(ir)
  run = "run" + srun
  inDir1 = topIndir + "/" + run + "/" + "other_files_" + targ + "_" + run + "/"
  inDir2 = topIndir + "/" + run + "/"

  if os.path.isdir(inDir1) is False:
    print(inDir1 + " does not exists. Quit")
    exit(0)

  print ("inDir1:", inDir1)
  os.chdir(inDir2)
  print("pwd: " + os.getcwd())

  cmd1 = "mv " + inDir1 + "/* " + inDir2
  print("cmd1: " + cmd1)

  cmd2 = "rm -rf " + inDir1
  print("cmd2: " + cmd2)

  os.system(cmd1)
  os.system(cmd2)
