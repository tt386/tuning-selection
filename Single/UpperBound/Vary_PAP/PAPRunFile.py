import subprocess
from Params import *

for PAP in PAPList:
    subprocess.call(['python','RunFile.py','-P',str(PAP)])
    print("Finished PAP=",PAP)
