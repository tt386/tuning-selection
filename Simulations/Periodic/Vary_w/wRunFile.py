import subprocess
from Params import *

for w in wList:
    subprocess.call(['python','RunFile.py','-w',str(w)])
    print("Finished w=",w)
