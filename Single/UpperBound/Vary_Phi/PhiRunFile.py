import subprocess
from Params import *

for Phi in PhiList:
    subprocess.call(['python','RunFile.py','-P',str(Phi)])
    print("Finished Phi=",Phi)
