import numpy as np
import os
import shutil



#Total width of Selection Region
KList = np.logspace(-1,3,100)

w = 0.1

"""
#Number of sub Selection regions
NList = np.arange(1,21,1)

#Separations
d = 0.1#10#dList = np.arange(1,11)
"""

#Make dx 10 times smaller than the smallest L
dx = min(KList)*w/100

#The uppermost x-bound: make it larger than necessary
xbound  =1000

#Initial proportion of R
Phi = 1e-5

#Time for which the pesticide is applied
PAP = 0.1


SaveDirName = ("SaveFiles/"+
            "MinK_%0.5f_MaxK_%0.5f_KNum_%d"%(min(KList),max(KList),len(KList)) +
            "_w_%0.3f"%(w) + 
            "_dx_" + '{:.1E}'.format(dx) +
            "_PAP_" + '{:.1E}'.format(PAP) +
            "_Phi_"+'{:.1E}'.format(Phi))


if not os.path.isdir("SaveFiles"):
    os.mkdir("SaveFiles")


if not os.path.isdir(SaveDirName):
    os.mkdir(SaveDirName)
    print("Created Directory")

shutil.copyfile("Params.py", SaveDirName+'/Params.py')
shutil.copyfile("Script.py", SaveDirName+"/Script.py")
