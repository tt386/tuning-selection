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
parser.add_argument('-w','--refuge',type=float,required=True,
        help='Length of periodic subunit')
args = parser.parse_args()

w = float(args.refuge)

SubSaveDirName = (SaveDirName +
    "/w_%0.5f"%(w))

if not os.path.isdir(SubSaveDirName):
    os.mkdir(SubSaveDirName)
    print("Created Directory for refuge",w)
#########################################

shutil.copy("Params.py",SaveDirName)

plist = []

for K in KList:
    p=subprocess.Popen(['nice','-n','19','python','Script.py','-K',str(K),'-w',str(w),'-d',str(SubSaveDirName)])
    plist.append(p)

for p in plist:
    p.wait()

endtime = time.time()


print("Total Time taken:",endtime-starttime)
