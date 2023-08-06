from Params import *


import subprocess
import time

import os,shutil

starttime = time.time()

if not os.path.isdir(SaveDirName):
    os.mkdir(SaveDirName)
    print("Created Directory")

shutil.copy("Params.py",SaveDirName)

plist = []

for K in KList:
    p=subprocess.Popen(['nice','-n','19','python','Script.py','-K',str(K)])
    plist.append(p)

for p in plist:
    p.wait()

endtime = time.time()


print("Total Time taken:",endtime-starttime)
