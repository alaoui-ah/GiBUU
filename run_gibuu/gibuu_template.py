#!/usr/bin/env python3

import os
import argparse
import socket
import shutil
import re
import myfuncs

hhome = os.environ['HOME']

gibVer = "REPLACE"
targAtt = "REPLACE"
btr = "REPLACE"
softDir = "REPLACE"
scriptDir = "REPLACE"
ouDir = "REPLACE"

optFile  = "gibuu_" + btr + ".opt"
gibLogFile  = "gibuu_" + btr + ".log"
rootFile = "gibuu_" + btr + ".root"
outFile  = "gibuu_" + btr + ".out"
g2lLogFile  =  "g2l_" + btr + ".log"
lundFile = "gibuu_" + btr + ".lund"

os.chdir(ouDir)

#geneExe = f"{softDir}/GiBUU/{gibVer}/release/testRun/GiBUU.x".strip()
geneExe = f"{softDir}/GiBUU/GiBUU_{gibVer}".strip()
geneCmd = f"source {scriptDir}/set_env.sh; {geneExe} < {optFile} 2>&1 | tee {gibLogFile}".strip()
print(geneCmd)
os.system(geneCmd)


## convert root file to lund file
g2lExe = f"{softDir}/GiBUU/gibuu2lund/gibuu2lund.exe".strip()
g2lCmd = f"source {scriptDir}/set_env.sh; {g2lExe} {targAtt} 2>&1 | tee {g2lLogFile}".strip()
print(g2lCmd)
os.system(g2lCmd)

origRootFile = "EventOutput.Pert.00000001.root"
if os.path.isfile(origRootFile) is True:
  os.rename(origRootFile, rootFile)

origLundFile = "lund.lund"
if os.path.isfile(origLundFile) is True:
  os.rename(origLundFile, lundFile)

if os.path.isfile("fort.12") is True:
  os.rename("fort.12", outFile)

print("\n")
