#!/usr/bin/env python3

##
# Purpose:
##

import os
import tarfile
import datetime
import zipfile

####
def zipFileFunc(fileName):
  zipFileName = fileName + ".gz"
  with zipfile.ZipFile(zipFileName, 'w') as zp:
    zp.write(zipFileName)

# Extract all the contents of zip_file in dist_dir
def unzipFileFunc(fileName):
  with zipfile.ZipFile(fileName, 'r') as zp:
    zp.extractall()

####
def tarFileFunc(sourceDir):
  fileName = sourceDir + ".tar"
  with tarfile.open(fileName, "w:tar") as tar:
    tar.add(sourceDir, arcname=os.path.basename(sourceDir))

####
def untarFileFunc(fileName):
  with tarfile.open(fileName, 'r') as tar:
    tar.extractall()

####
def diffList(li1, li2):
  return (list(set(li1) - set(li2)))

####
def getRun(ir):
  rr = str(ir)
  if ir < 10:
    rr = "000" + str(ir)
  elif ir < 100:
    rr = "00" + str(ir)
  elif ir < 1000:
    rr = "0" + str(ir)
  return rr

####
def sedCmd(file, oldstr, newstr):
  fin = open(file, "rt")
  data = fin.read()
  data = data.replace(oldstr, newstr)
  fin.close()
  fin = open(file, "wt")
  fin.write(data)
  fin.close()

####
def getSeed(run):
  now = datetime.datetime.now()
  year = now.strftime("%Y")
  month = now.strftime("%m")
  day = now.strftime("%d")
  hour = now.strftime("%H")
  minu = now.strftime("%M")
  sec = now.strftime("%S")
  isd = run + year + month + day + hour + minu + sec
  a2 = 2147483647
  iseed = (int(isd) % a2)
  return iseed

####
def getTimeStamp():
  now = datetime.datetime.now()
  startTime = now.strftime("%d/%m/%Y %H:%M:%S")
  year = now.strftime("%Y")
  month = now.strftime("%m")
  day = now.strftime("%d")
  hour = now.strftime("%H")
  minute = now.strftime("%M")
  second = now.strftime("%S")
  timeStamp = year + "_" + month + "_" + day + "_" + hour + "h_" + minute + "m_" + second + "s"
  return timeStamp

####
def listToString(s, sep):
  str1 = ""
  for ele in s:
    str1 += ele + sep
  return str1

####
def checkExpTarg(expt, targ):
  listOfExpts = ["clas6", "clas12", "hermes", "eic"]
  clas6Targs = ["D", "C", "Fe", "Pb"]
  clas12Targs = ["D", "C", "Cu", "Pb"]
  hermesTargs = ["D", "N", "Kr", "Xe"]
  eicTargs = ["D", "Au"]
  listOfTargs = clas6Targs + clas12Targs + hermesTargs + eicTargs

  ir = True
  if expt not in listOfExpts:
    print(expt + " NOT found in List of experiments: " + str(listOfExpts) + ". Quit")
    ir = False
    return ir

  if targ not in listOfTargs:
    print(targ + " NOT found in List of targets: " + str(listOfTargs) + ". Quit")
    ir = False
    return ir

  if expt == "clas6":
    if targ not in clas6Targs:
      ir = False
  if expt == "clas12":
    if targ not in clas12Targs:
      ir = False
  if expt == "hermes":
    if targ not in hermesTargs:
      ir = False
  if expt == "eic":
    if targ not in eicTargs:
      ir = False

  if ir is False:
    print("")
    print("Experiment " + expt + " and target " + targ + " do not match. Quit")
    print("Possible Experiment/Target combinations are:")
    print("CLAS6: " + str(clas6Targs))
    print("CLAS12:" + str(clas12Targs))
    print("HERMES:" + str(hermesTargs))
    print("EIC:   " + str(eicTargs))
    print("Quit")

  return ir
