from Params import *


import subprocess
import time

import os,shutil

starttime = time.time()


#########################################
###Argparse##############################
#########################################
from argparse import ArgumentParser
parser = ArgumentParser(description='Number of Regions')
parser.add_argument('-P','--PAP',type=float,required=True,
        help='Length of periodic subunit')
args = parser.parse_args()

PAP = float(args.PAP)

SubSaveDirName = (SaveDirName +
    "/PAP_%0.5f"%(PAP))

if not os.path.isdir(SubSaveDirName):
    os.mkdir(SubSaveDirName)
    print("Created Directory for refuge",PAP)
#########################################

shutil.copy("Params.py",SaveDirName)

plist = []

for L in LList:
    p=subprocess.Popen(['nice','-n','19','python','Script.py','-L',str(L),'-P',str(PAP),'-d',str(SubSaveDirName)])
    plist.append(p)

for p in plist:
    p.wait()

endtime = time.time()


print("Total Time taken:",endtime-starttime)
