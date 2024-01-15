#!/usr/bin/env python3

##
# Usage:
# run_gibuu.py -mode MODE -ebeam EBEAM -seed SEED -targ TARG -run1 RUN1 -run2 RUN2 -pdf PDF -expt EXPT
# Arguments:
#  -h, --help : show this help message and exit
#  -mode MODE : test, farm, hpc
#  -ebeam EBEAM : beam energy
#  -seed SEED : 0: use current_time as seed, 1: use 1 as initial seed to python random function, otherwise whatever value you entered will be used as seed for the generator
#  -targ TARG : D, C, N, Al, Fe, Cu, Sn, Pb
#  -run1 RUN1 : first run
#  -run2 RUN2 : last run
#  -lambdadec LAMBDADEC : undergo lambda decay
#  -expt EXPT : clas6,clas12,noExp
# ex: ./run_gibuu.py -mode test -ebeam 22 -seed 0 -targ D -run1 1 -run2 50 -lambdadec 1 -expt clas6
##

import os
hhome = os.environ['HOME']

import stat
import argparse
import shutil
import time
import datetime
import socket
import random
import myfuncs
from dotenv import load_dotenv

modes = ["test", "farm", "hpc"]
targets = ["D", "C", "N", "Al", "Fe", "Cu", "Sn", "Pb"]
targZ = {"D":1, "C":6, "N":7, "Al":13, "Fe":28, "Cu":29, "Sn":50, "Pb":82}
targA = {"D":2, "C":12, "N":14, "Al":27, "Fe":56, "Cu":63, "Sn":118, "Pb":208}
numEnsem = {"D":5000, "C":1000, "N":1000, "Al":500, "Fe":50, "Cu":50, "Sn":30, "Pb":20}
lenPert = {"D":20, "C":120, "N":120, "Al":250, "Fe":560, "Cu":560, "Sn":2000, "Pb":4000}
experiments = ["clas6", "clas12", "noExp"]
expID = {"clas6":5, "clas12":4, "noExp":17}
targPdfSet = {"D":102000, "C":102300, "N":102350, "Al":102450, "Fe":102600, "Cu":102650, "Sn":102800, "Pb":103100}
##targPdfSet = {"D":3000300, "C":3001500, "N":3001800, "Al":3002100, "Fe":3002700, "Cu":3003000, "Sn":3003600, "Pb":3004500}

now = datetime.datetime.now()
startTime = now.strftime("%d/%m/%Y %H:%M:%S")
print("Start Time: " + startTime)
timeStamp = myfuncs.getTimeStamp()

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-mode", required=True, help="test, farm, hpc")
ap.add_argument("-ebeam", required=True, help="Beam energy")
ap.add_argument("-seed", required=True, help="0: use current time as seed, 1: use 1 as initial seed to python random function, otherwise whatever value you entered will be used as seed for the generator")
ap.add_argument("-targ", required=True, help="D, C, N, Al, Fe, Cu, Sn, Pb")
ap.add_argument("-run1", required=True, help="first run")
ap.add_argument("-run2", required=True, help="last run")
ap.add_argument("-lambdadec", required=True, help="Lambda decay: 0, 1")
ap.add_argument("-expt", required=True, help="clas6, clas12")
myargs = vars(ap.parse_args())

mode = myargs['mode']
eBeam = float(myargs['ebeam'])
seed = int(myargs['seed'])
targ = myargs['targ']
run1 = int(myargs['run1'])
run2 = int(myargs['run2'])
lambdaDec = myargs['lambdadec']
expt = myargs['expt']

print("mode: ", mode)
print("eBeam: ", str(eBeam))
print("seed: ", str(seed))
print("targ: ", targ)
print("run1: ", str(run1))
print("run2: ", str(run2))
print("lambdaDec: ", str(lambdaDec))
print("experiment: ", expt)

if mode not in modes:
  print("bad mode argument. Possible values are: " + str(modes) + "\n")
  exit(0)

if targ not in targets:
  print("bad targ argument. Possible values are: " + str(targets) + " \n")
  exit(0)

if lambdaDec != "0" and lambdaDec != "1":
  print("bad lambdadec argument. Possible values are: 0, 1\n")
  exit(0)

if expt not in experiments:
  print("bad experiment argument. Possible values are: " + str(experiments) + "\n")
  exit(0)

############################################################
############################################################
############################################################

gene = "gibuu"
#gibVer = "2021"
gibVer = "2023"

lamDec = "lamdecON"
if lambdaDec == "0":
  lamDec = "lamdecOFF"

if os.path.isfile("./dot.env") is True:
  os.remove("./dot.env")
cmd0 = "source " + hhome + "/software_" + gene + "/env_scripts/set_env.sh"
os.system(cmd0)
load_dotenv("./dot.env")
softDir = os.environ['SOFT'] + "/"
print("softDir ===== ", softDir)
if os.path.isdir(softDir) is False:
  print(softDir + " does not exists. Quit")
  exit(0)
print("softDir is set to ", softDir)

topOuDir = ""

hst = socket.gethostname()[0:3]
if hst == "ifa":
  topOuDir = "/work/clas12/ahmed/mc/"
elif hst == "ui0":
  topOuDir = "/eos/user/a/alaoui/mc/"
elif hst == "cct":
  topOuDir = "/home/ahmed/mc/"
elif hst == "Mac":
  topOuDir = "/Users/ahmed/mc/"

if mode == "test":
  topOuDir = topOuDir + "/test/"

scriptDir = softDir + "/run_" + gene + "/"
if os.path.isdir(scriptDir) is False:
  print(scriptDir + " does not exists. Quit")
  exit(0)

geneDir = softDir + "/GiBUU/"
if os.path.isdir(geneDir) is False:
  print(geneDir + " does not exists. Quit")
  exit(0)

logDir = gene + "/" + gibVer + "/" + expt + "/" + str(eBeam) + "GeV/" + lamDec + "/" + targ + "/"

topDir = topOuDir + "/" + logDir
if os.path.isdir(topDir) is False:
  os.makedirs(topDir)

buuDir = geneDir + "/" + gibVer + "/buuinput"

if os.path.isfile(scriptDir + "myfuncs.py") is False:
  print(scriptDir + "myfuncs.py does not exists. Quit")
  exit(0)

tempOptFile = gene + "_template.opt"
if os.path.isfile(scriptDir + tempOptFile) is False:
  print(scriptDir + tempOptFile + " does not exists. Quit")
  exit(0)

tempSimFile = gene + "_template.py"
if os.path.isfile(scriptDir + tempSimFile) is False:
  print(scriptDir + tempSimFile + " does not exists. Quit")
  exit(0)

useJetSetVec = "T"
shadow = "T"
nuclPDF = "1"
if targ == "D":
  useJetSetVec = "F"
  shadow = "F"
  nuclPDF = "0"

random.seed(seed)

#loop over runs
for ir in range(int(run1), int(run2) + 1, 1):
  print("")
  srun = myfuncs.getRun(ir)
  run = "run" + srun
  btr = targ + "_" + run

  optFile = gene + "_" + btr + ".opt"
  simFile = gene + "_" + btr + ".py"
  logFile = gene + "_" + btr + ".log"
  rootFile = gene + "_" + btr + ".root"
  seedFile = gene + "_" + btr + ".seed"
  ##

  if seed == 0:
    mySeed = myfuncs.getSeed(str(ir))
  elif seed ==1:
    mySeed = random.randint(10000000, 100000000)
  else:
    mySeed = seed

  ouDir = topDir + "/" + run + "/"
  if os.path.isdir(ouDir) is False:
    os.makedirs(ouDir)

  print("ouDir: " + ouDir)

  ## create directory to hold python and script files.
  newScriptDir = hhome + "/" + logDir + "/"
  if os.path.isdir(newScriptDir) is False:
    os.makedirs(newScriptDir)

  os.chdir(ouDir)
  print("pwd: " + os.getcwd())

  fin0 = open(seedFile, "wt")
  fin0.write("\n")
  fin0.write("Input Argument seed: " + str(seed) + ", " + gene + " seed: " + str(mySeed) + "\n")
  fin0.write("\n")
  fin0.close()

  os.chdir(newScriptDir)
  print("pwd: " + os.getcwd())

  shutil.copyfile(scriptDir + tempSimFile, newScriptDir + simFile)
  shutil.copyfile(scriptDir + tempOptFile, newScriptDir + optFile)
  shutil.copyfile(scriptDir + "myfuncs.py", newScriptDir + "myfuncs.py")

  os.chmod(simFile, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

  #option file
  myfuncs.sedCmd(optFile, "numEnsembles=", "numEnsembles=" + str(numEnsem[targ]))
  myfuncs.sedCmd(optFile, "length_perturbative=", "length_perturbative=" + str(lenPert[targ]))
  myfuncs.sedCmd(optFile, "target_Z=", "target_Z=" + str(targZ[targ]))
  myfuncs.sedCmd(optFile, "target_A=", "target_A=" + str(targA[targ]))
  myfuncs.sedCmd(optFile, "iExperiment=", "iExperiment=" + str(expID[expt]))
  myfuncs.sedCmd(optFile, "EXPT", expt.upper())
  myfuncs.sedCmd(optFile, "NNN", targ)
  myfuncs.sedCmd(optFile, "path_To_Input=", "path_To_Input       = \'" + buuDir + "\'")
  myfuncs.sedCmd(optFile, "shadow=", "shadow=" + shadow)
  myfuncs.sedCmd(optFile, "SEED=", "SEED=" + str(mySeed))
  myfuncs.sedCmd(optFile, "useJetSetVec=", "useJetSetVec=" + useJetSetVec)
  myfuncs.sedCmd(optFile, "NuclearPDFtype=", "NuclearPDFtype=" + nuclPDF)
#  myfuncs.sedCmd(optFile, "MSTP(51)=", "MSTP(51)=" + str(targPdfSet[targ]))
  if expt == "noExp":
      myfuncs.sedCmd(optFile, "Ebeam=", "Ebeam=" + str(eBeam))
  else:
      myfuncs.sedCmd(optFile, "Ebeam=", "!Ebeam=")

  shutil.copyfile(newScriptDir + optFile, ouDir + optFile)

  #simulation  file
  myfuncs.sedCmd(simFile, "gene = \"REPLACE\"", "gene = " + "\"" + gene + "\"")
  myfuncs.sedCmd(simFile, "gibVer = \"REPLACE\"", "gibVer = " + "\"" + gibVer + "\"")
  myfuncs.sedCmd(simFile, "btr = \"REPLACE\"", "btr = " + "\"" + btr + "\"")
  myfuncs.sedCmd(simFile, "softDir = \"REPLACE\"", "softDir = " + "\"" + softDir + "\"")
  myfuncs.sedCmd(simFile, "geneDir = \"REPLACE\"", "geneDir = " + "\"" + geneDir + "\"")
  myfuncs.sedCmd(simFile, "ouDir = \"REPLACE\"", "ouDir = " + "\"" + ouDir + "\"")

  time.sleep(0.2)

  if mode == "test":

    print("running job " + simFile + " in test mode")
    os.system("./"+simFile)

  elif mode == "farm":

    farmOuDir = "/farm_out/ahmede/" + logDir
    if os.path.isdir(farmOuDir) is False:
      os.makedirs(farmOuDir)

    errFile = farmOuDir + gene + "_" + btr + ".err"
    outFile = farmOuDir + gene + "_" + btr + ".out"
    jobFile = gene + "_" + btr + ".sh"

    email = "myahmed.elalaoui@usm.cl"
    myTime = "72:00:00"
    diskSpace = "5000M"
    memUsage = "1000M"
    jobName = gene + "_" + btr
    osName = "general"
    queue = "production"
    proj = "clas12"
    #proj = "eg2a"
    machine = "JLAB"

    print("jobName: ", jobName)
    fin = open(jobFile, "wt")
    fin.write("#!/usr/bin/env bash\n")
    fin.write("#SBATCH --job-name=" + jobName + "\n")
    fin.write("#SBATCH --output=" + outFile + "\n")
    fin.write("#SBATCH --error=" + errFile + "\n")
    fin.write("#SBATCH --partition=" + queue + "\n")
    fin.write("#SBATCH --account=" + proj + "\n")
    fin.write("#SBATCH --constraint=" + osName + "\n")
    fin.write("#SBATCH --time=" + myTime + "\n")
    fin.write("#SBATCH --mem=" + memUsage + "\n")
    fin.write("#SBATCH --mail-user=" + email + "\n")
    fin.write("\n")
    fin.write("ulimit -c unlimited\n")
    fin.write("\n")
    fin.write("cd " + newScriptDir + "\n")
    fin.write("\n")
    fin.write("echo hostname = \`hostname\`\n")
    fin.write("\n")
    fin.write("pwd\n")
    fin.write("\n")
    fin.write("echo \"SLURM_SUBMIT_HOST = ${SLURM_SUBMIT_HOST}\"\n")
    fin.write("\n")
    fin.write("chmod 755 " + "./" + simFile + "\n")
    fin.write("python3 ./" + simFile + "\n")
    fin.write("\n")
    fin.close()
    print("running job " + jobFile + " in " + machine + " cluster")
    cmd = "sbatch " + jobFile
    os.system(cmd)

  elif mode == "hpc":

    farmOuDir = ouDir + "/hpc_out/" + logDir
    if os.path.isdir(farmOuDir) is False:
      os.makedirs(farmOuDir)

    errFile = farmOuDir + gene + "_" + btr + ".err"
    outFile = farmOuDir + gene + "_" + btr + ".out"
    jobFile = gene + "_" + btr + ".sh"

    email = "myahmed.elalaoui@usm.cl"
    queue = "batch"
    myTime = "72:00:00"
    diskSpace = "5000M"
    memUsage = "1000M"

    jobName = gene + "_" + btr
    print("jobName: ", jobName)
    fin = open(jobFile, "wt")
    fin.write("#!/usr/bin/env bash\n")
    fin.write("#SBATCH -J " + jobName + "\n")
    fin.write("#SBATCH -o " + outFile + "\n")
    fin.write("#SBATCH -e " + errFile + "\n")
    fin.write("#SBATCH --partition=" + queue + "\n")
    fin.write("#SBATCH --time=" + myTime + "\n")
    fin.write("#SBATCH --mem=" + memUsage + "\n")
    #fin.write("#SBATCH -m ae\n")
    fin.write("#SBATCH --mail-user=" + email + "\n")
    fin.write("\n")
    fin.write("ulimit -c unlimited\n")
    fin.write("\n")
    fin.write("cd " + ouDir + "\n")
    fin.write("\n")
    fin.write("chmod 755 " + "./" + simFile + "\n")
    fin.write("python3 ./" + simFile + "\n")
    fin.write("\n")
    fin.close()

    print("running job " + jobFile + " in USM cluster")
    cmd = "sbatch " + jobFile
    os.system(cmd)

  print("run   = ", ir, "/", run2)
  print("seed  = ", mySeed)
  print("ouDir = ", ouDir)

now = datetime.datetime.now()
endTime = now.strftime("%d/%m/%Y %H:%M:%S")

print("\n")
print("start time          = ", startTime)
print("end time            = ", endTime)
print("generator directory = ", geneDir)
print("target              = ", targ)
print("run1                = ", run1)
print("run2                = ", run2)

print("Done")
