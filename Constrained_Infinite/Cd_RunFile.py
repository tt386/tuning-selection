mport subprocess
from Params import *

for C in CList:
    for d in dList:
        subprocess.call(['python','RunFile.py','-C',str(C),'d',str(d)])
        print("Finished C,d=",C,d)

