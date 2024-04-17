#!/usr/bin/env python3

##
# Usage:
# run_gibuu.py -mode MODE -ebeam EBEAM -seed SEED -targ TARG -tgzpos TGZPOS -tgzlen TGZLEN -tgrad TGRAD -kt KT -run1 RUN1 -run2 RUN2
# Arguments:
#  -h, --help : show this help message and exit
#  -mode MODE : test, farm
#  -ebeam EBEAM : beam energy
#  -seed SEED : 0: use current_time as seed, 1: use 1 as initial seed to python random function, otherwise whatever value you entered will be used as seed for the generator
#  -targ TARG : "p","D","He","Li","Be","C","N","Al","Ca","Fe","Cu","Ag","Sn","Xe","Au","Pb"
#  -tgzpos TGZPOS : Target z position
#  -tgzlen TGZLEN : Target z length
#  -tgrad TGRAD : Target Radius
#  -kt : KT value parp(91) 0.64 !D=0.44 ! width intrinsic kT
#  -run1 RUN1 : first run
#  -run2 RUN2 : last run
# ex: ./run_gibuu.py -mode test -ebeam 11.0 -seed 0 -targ C -tgzpos -3.0 -tgzlen 0.5 -tgrad 1.0 -kt 0.64 -run1 1 -run2 1
##

import os
import stat
import argparse
import shutil
import time
import datetime
import socket
import random
from pathlib import Path
import myfuncs
from dotenv import load_dotenv

hhome = os.environ['HOME']

now = datetime.datetime.now()
startTime = now.strftime("%d/%m/%Y %H:%M:%S")
print(f"Start Time: {startTime}")
timeStamp = myfuncs.getTimeStamp()

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-mode", required=True, help="test, farm")
ap.add_argument("-ebeam", required=True, help="Beam energy")
ap.add_argument("-seed", required=True, help="0: use current time as seed, 1: use 1 as initial seed to python random function, otherwise whatever value you entered will be used as seed for the generator")
ap.add_argument("-targ", required=True, help="p,D,He,Li,Be,C,N,Al,Ca,Fe,Cu,Ag,Sn,Xe,Au,Pb")
ap.add_argument("-tgzpos", required=True, help="Target z position")
ap.add_argument("-tgzlen", required=True, help="Target z length")
ap.add_argument("-tgrad", required=True, help="Target Radius")
ap.add_argument("-kt", required=True, help="kt value")
ap.add_argument("-run1", required=True, help="first run")
ap.add_argument("-run2", required=True, help="last run")
myargs = vars(ap.parse_args())

mode = myargs['mode']
eBeam = myargs['ebeam']
seed = myargs['seed']
targ = myargs['targ']
tgzpos = myargs['tgzpos']
tgzlen = myargs['tgzlen']
tgrad = myargs['tgrad']
kt = myargs['kt']
run1 = int(myargs['run1'])
run2 = int(myargs['run2'])

print(f"mode: {mode}")
print(f"eBeam: {eBeam}")
print(f"seed: {seed}")
print(f"targ: {targ}")
print(f"tgzpos: {tgzpos}")
print(f"tgzlen: {tgzlen}")
print(f"tgrad: {tgrad}")
print(f"kt: {kt}")
print(f"run1: {run1}")
print(f"run2: {run2}")

##############################################

# nNNPDF10_nlo_as_0118
# {"N1":3100000,"D2":3100300,"He4":3100600,"Li6":3100900,"Be9":3101200,"C12":3101500,"N14":3101800,"Al27":3102100,
# "Ca40":3102400,"Fe56":3102700,"Cu64":3103000,"Ag108":3103300,"Sn119":3103600,"Xe131":3103900,"Au197":3104200,
# "Pb208":3104500
#"zPos":0,#-3.9,"Width":0,#5.0,

targNames = ["p","D","He","Li","Be","C","N","Al","Ca","Fe","Cu","Ag","Sn","Xe","Au","Pb"]

Targets = {
  targNames[0] : {"Name":targNames[0],"A":"1","Z":"1","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3000000","numEnsem":"6000","lenPert":"15"},
  targNames[1] : {"Name":targNames[1],"A":"2","Z":"1","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3000300","numEnsem":"5000","lenPert":"20"},
  targNames[2] : {"Name":targNames[2],"A":"4","Z":"2","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3000600","numEnsem":"4000","lenPert":"40"},
  targNames[3] : {"Name":targNames[3],"A":"6","Z":"3","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3000900","numEnsem":"3000","lenPert":"60"},
  targNames[4] : {"Name":targNames[4],"A":"8","Z":"4","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3001200","numEnsem":"2000","lenPert":"80"},
  targNames[5] : {"Name":targNames[5],"A":"12","Z":"6","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3001500","numEnsem":"1000","lenPert":"120"},
  targNames[6] : {"Name":targNames[6],"A":"14","Z":"7","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3001800","numEnsem":"1000","lenPert":"120"},
  targNames[7] : {"Name":targNames[7],"A":"27","Z":"13","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3002100","numEnsem":"500","lenPert":"250"},
  targNames[8] : {"Name":targNames[8],"A":"40","Z":"20","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3002400","numEnsem":"300","lenPert":"360"},
  targNames[9] : {"Name":targNames[9],"A":"56","Z":"28","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3002700","numEnsem":"100","lenPert":"560"},
  targNames[10] : {"Name":targNames[10],"A":"63","Z":"29","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3003000","numEnsem":"100","lenPert":"560"},
  targNames[11] : {"Name":targNames[11],"A":"108","Z":"47","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3003300","numEnsem":"100","lenPert":"1500"},
  targNames[12] : {"Name":targNames[12],"A":"118","Z":"50","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3003600","numEnsem":"100","lenPert":"2000"},
  targNames[13] : {"Name":targNames[13],"A":"131","Z":"54","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3003900","numEnsem":"100","lenPert":"3000"},
  targNames[14] : {"Name":targNames[14],"A":"200","Z":"79","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3004200","numEnsem":"100","lenPert":"4000"},
  targNames[15] : {"Name":targNames[15],"A":"207","Z":"82","tgzpos":tgzpos,"tgzlen":tgzlen,"tgrad":tgrad,"pdfset":"3004500","numEnsem":"100","lenPert":"4000"}
}

modes = ["test", "farm"]

class myTarget:
	def __init__(self,name="EMPTY",A="-1000",Z="-1000",tgzpos="-3.9",tgzlen="5.0",tgrad="5.0",pdfset="-1000",numEnsem="0",lenPert="0"):
		self.name=name
		self.A=A
		self.Z=Z
		self.tgzpos=tgzpos
		self.tgzlen=tgzlen
		self.tgrad=tgrad
		self.pdfset=pdfset
		self.numEnsem=numEnsem
		self.lenPert=lenPert

	def __str__(self):
		return f"This is a target class for {self.name}"

	def show_target_attributes(self):
		return f"\nTarget Info:\nName:{self.name}\nA:{self.A}\nZ:{self.Z}\nTarget center z position:{self.tgzpos}\nTarget length alpng z axis:{self.tgzlen}\nTarget Radius:{self.tgrad}\npdfset:{self.pdfset}\nnumEnsem:{self.numEnsem}\nlenPert:{self.lenPert}\n"

	def getpdfset(self):
		return f"{self.pdfset}"

	def getA(self):
		return f"{self.A}"

	def getZ(self):
		return f"{self.Z}"

	def getTargZpos(self):
		return f"{self.tgzpos}"

	def getTargLength(self):
		return f"{self.tgzlen}"

	def getTargRadius(self):
		return f"{self.tgrad}"

	def getNumEnsem(self):
		return f"{self.numEnsem}"

	def getLenPert(self):
		return f"{self.lenPert}"

myTarg  = myTarget(name=Targets[targ]["Name"], 
                   A=Targets[targ]["A"],  
				   Z=Targets[targ]["Z"], 
				   tgzpos=Targets[targ]["tgzpos"], 
				   tgzlen=Targets[targ]["tgzlen"], 
				   tgrad=Targets[targ]["tgrad"], 
				   pdfset=Targets[targ]["pdfset"],
                   numEnsem=Targets[targ]["numEnsem"],
                   lenPert=Targets[targ]["lenPert"])

print(myTarg.show_target_attributes())

targAtt = f"{myTarg.getA()} {myTarg.getZ()} {myTarg.getTargZpos()} {myTarg.getTargLength()} {myTarg.getTargRadius()}".strip()
if mode not in modes:
  print(f"Bad mode argument. Possible values are: {modes}\n")
  exit(0)

if targ not in targNames:
  print(f"Bad targ argument. Possible values are: {targNames}\n")
  exit(0)

############################################################
############################################################

#gibVer = "2023_00"
gibVer = "2023_04"

if os.path.isfile("./dot.env") is True:
  os.remove("./dot.env")
cmd0 = f"source ./set_env.sh".strip()
os.system(cmd0)
load_dotenv("./dot.env")
softDir = os.environ['SOFT'] + "/"
user = os.environ['USER']

if os.path.isdir(softDir) is False:
  print(f"{softDir} does not exists. Quit")
  exit(0)

print(f"softDir is set to {softDir}")

topOuDir = f"./test/".strip()

if mode == "test":
  topOuDir = f"{topOuDir}/test/".strip()

scriptDir = f"{softDir}/GiBUU/run_gibuu/".strip()
if os.path.isdir(scriptDir) is False:
  print(f"{scriptDir} does not exists. Quit")
  exit(0)

geneDir = f"{softDir}/GiBUU/".strip()
if os.path.isdir(geneDir) is False:
  print(f"{geneDir} does not exists. Quit")
  exit(0)

logDir = f"gibuu/{gibVer}/{eBeam}GeV/{targ}/kt_{kt}/".strip()

topDir = f"{topOuDir}{logDir}".strip()
if os.path.isdir(topDir) is False:
  os.makedirs(topDir)

buuDir = f"{geneDir}/{gibVer}/buuinput".strip()
if os.path.isdir(buuDir) is False:
  print(f"{buuDir} does not exists. Quit")
  exit(0)

if os.path.isfile(scriptDir + "myfuncs.py") is False:
  print(f"{scriptDir} myfuncs.py does not exists. Quit")
  exit(0)

tempOptFile = f"gibuu_template.opt".strip()
if os.path.isfile(scriptDir + tempOptFile) is False:
  print(f"{scriptDir}{tempOptFile} does not exists. Quit")
  exit(0)

tempSimFile = f"gibuu_template.py".strip()
if os.path.isfile(scriptDir + tempSimFile) is False:
  print(f"{scriptDir}{tempSimFile} does not exists. Quit")
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
	print("\n")
	#run = f"run{str(ir).zfill(len(str(run2)))}".strip()
	run = f"run{str(ir).zfill(4)}".strip()
	btr = f"{targ}_{run}".strip()

	optFile  = f"gibuu_{btr}.opt".strip()
	simFile  = f"gibuu_{btr}.py".strip()
	logFile  = f"gibuu_{btr}.log".strip()
	seedFile = f"gibuu_{btr}.seed".strip()
	rootFile = f"gibuu_{btr}.root".strip()
	lundFile = f"gibuu_{btr}.lund".strip()

	if seed == 0:
		mySeed = myfuncs.getSeed(str(ir))
	elif seed ==1:
		mySeed = random.randint(10000000, 100000000)
	else:
		mySeed = seed

	ouDir = f"{topDir}/{run}/".strip()
	if os.path.isdir(ouDir) is False:
		os.makedirs(ouDir)

	print(f"ouDir: {ouDir}")

	os.chdir(ouDir)
	print(f"pwd: {os.getcwd()}\n")

	fin0 = open(seedFile, "wt")
	fin0.write("\n")
	fin0.write(f"Input Argument seed: {seed}, gibuu seed: {mySeed}\n")
	fin0.write("\n")
	fin0.close()

	print(f"pwd: {os.getcwd()}")

	shutil.copyfile(scriptDir + tempSimFile, ouDir + simFile)
	shutil.copyfile(scriptDir + tempOptFile, ouDir + optFile)
	shutil.copyfile(scriptDir + "myfuncs.py", ouDir + "myfuncs.py")

	os.chmod(simFile, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

  #option file
	myfuncs.sedCmd(optFile, "numEnsembles=", f"numEnsembles={myTarg.getNumEnsem()}") #{numEnsem[targ]}
	myfuncs.sedCmd(optFile, "length_perturbative=", f"length_perturbative={myTarg.getLenPert()}") #{lenPert[targ]}
	myfuncs.sedCmd(optFile, "Z=", f"Z={myTarg.getZ()}")
	myfuncs.sedCmd(optFile, "A=", f"A={myTarg.getA()}")
	myfuncs.sedCmd(optFile, "NNN", targ)
	myfuncs.sedCmd(optFile, "path_To_Input=", "path_To_Input       = \'" + buuDir + "\'")
	myfuncs.sedCmd(optFile, "shadow=", f"shadow={shadow}")
	myfuncs.sedCmd(optFile, "SEED=", f"SEED={mySeed}")
	myfuncs.sedCmd(optFile, "useJetSetVec=", f"useJetSetVec={useJetSetVec}")
	myfuncs.sedCmd(optFile, "NuclearPDFtype=", f"NuclearPDFtype={nuclPDF}")
	myfuncs.sedCmd(optFile, "MSTP(51)=", f"MSTP(51)={myTarg.getpdfset()}")
	myfuncs.sedCmd(optFile, "PARP(91)=", f"PARP(91)={kt}")
	myfuncs.sedCmd(optFile, "PARP(92)=", f"PARP(92)={kt}")
	print(f"PARP(92)={kt}")
	myfuncs.sedCmd(optFile, "Ebeam=", f"Ebeam={eBeam}")

  #simulation  file
	myfuncs.sedCmd(simFile, "gibVer = \"REPLACE\"", "gibVer = " + "\"" + gibVer + "\"")
	myfuncs.sedCmd(simFile, "targAtt = \"REPLACE\"", "targAtt = " + "\"" + targAtt + "\"")
	myfuncs.sedCmd(simFile, "btr = \"REPLACE\"", "btr = " + "\"" + btr + "\"")
	myfuncs.sedCmd(simFile, "softDir = \"REPLACE\"", "softDir = " + "\"" + softDir + "\"")
	myfuncs.sedCmd(simFile, "scriptDir = \"REPLACE\"", "scriptDir = " + "\"" + scriptDir + "\"")
	myfuncs.sedCmd(simFile, "ouDir = \"REPLACE\"", "ouDir = " + "\"" + ouDir + "\"")

	time.sleep(0.2)

	if mode == "test":

		print(f"running job {simFile} in test mode")
		os.system("./"+simFile)

	elif mode == "farm":

		farmOuDir = f"/farm_out/{user}/{logDir}".strip()
		if os.path.isdir(farmOuDir) is False:
			os.makedirs(farmOuDir)

		errFile = f"{farmOuDir}gibuu_{btr}.err".strip()
		outFile = f"{farmOuDir}gibuu_{btr}.out".strip()
		jobFile = f"gibuu_{btr}.sh".strip()

		#email = 
		myTime = "72:00:00"
		diskSpace = "5000M"
		memUsage = "1000M"
		jobName = f"gibuu_{btr}".strip()
		osName = "general"
		queue = "production"
		proj = "clas12"
		machine = "JLAB"

		print(f"jobName: {jobName}")
		fin = open(jobFile, "wt")
		fin.write("#!/usr/bin/env bash\n")
		fin.write(f"#SBATCH --job-name={jobName}\n")
		fin.write(f"#SBATCH --output={outFile}\n")
		fin.write(f"#SBATCH --error={errFile}\n")
		fin.write(f"#SBATCH --partition={queue}\n")
		fin.write(f"#SBATCH --account={proj}\n")
		fin.write(f"#SBATCH --constraint={osName}\n")
		fin.write(f"#SBATCH --time={myTime}\n")
		fin.write(f"#SBATCH --mem={memUsage}\n")
		#fin.write(f"#SBATCH --mail-user={email}\n")
		fin.write("\n")
		fin.write("ulimit -c unlimited\n")
		fin.write("\n")
		fin.write(f"cd {ouDir}\n")
		fin.write("\n")
		fin.write("echo hostname = \`hostname\`\n")
		fin.write("\n")
		fin.write("pwd\n")
		fin.write("\n")
		fin.write("echo \"SLURM_SUBMIT_HOST = ${SLURM_SUBMIT_HOST}\"\n")
		fin.write("\n")
		fin.write(f"chmod 755 ./{simFile}\n")
		fin.write(f"python3 ./{simFile}\n")
		fin.write("\n")
		fin.close()
		print(f"running job {jobFile} in {machine} cluster")
		cmd = f"sbatch {jobFile}".strip()
		os.system(cmd)

	print(f"run   = {ir}/{run2}")
	print(f"seed  = {mySeed}")
	print(f"ouDir = {ouDir}")

now = datetime.datetime.now()
endTime = now.strftime("%d/%m/%Y %H:%M:%S")

print("\n")
print(f"start time = {startTime}")
print(f"end time   = {endTime}")
print(f"geneDir    = {geneDir}")
print(f"target     = {targ}")
print(f"pdfsset    = {targ}")

print(f"run1       = {run1}")
print(f"run2       = {run2}")

print("Done")
