import numpy as np
import os
import shutil



#Total width of Selection Region
LList = np.logspace(0.5,1.5,200)#(-1,3,100)

minlogphi = -12
maxlogphi = -1
phinum = 12
PhiList = np.logspace(minlogphi,maxlogphi,phinum)

"""
#Number of sub Selection regions
NList = np.arange(1,21,1)

#Separations
d = 0.1#10#dList = np.arange(1,11)
"""

#Make dx 10 times smaller than the smallest L
dx = min(LList)/100

#The uppermost x-bound: make it larger than necessary
xbound  =1000

#Initial proportion of R
#Phi = 1e-5

#Time for which the pesticide is applied
PAP = 0.1


SaveDirName = ("SaveFiles/"+
            "MinL_%0.5f_MaxL_%0.5f_LNum_%d"%(min(LList),max(LList),len(LList)) +
            "_xbound_%d"%(xbound) +
            "_minPhi_%d_maxPhi_%d_Phinum_%d"%(minlogphi,maxlogphi,phinum) + 
            "_PAP_"+'{:.1E}'.format(PAP))


if not os.path.isdir("SaveFiles"):
    os.mkdir("SaveFiles")


if not os.path.isdir(SaveDirName):
    os.mkdir(SaveDirName)
    print("Created Directory")

shutil.copyfile("Params.py", SaveDirName+'/Params.py')
shutil.copyfile("Script.py", SaveDirName+"/Script.py")
