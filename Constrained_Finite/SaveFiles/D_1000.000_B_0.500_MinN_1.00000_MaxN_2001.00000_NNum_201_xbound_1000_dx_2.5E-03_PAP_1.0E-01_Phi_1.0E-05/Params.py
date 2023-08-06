import numpy as np
import os
import shutil



#Total width of Avaiable space
D = 1000#[1,10,100]

#LList = np.logspace(-2,2,100)


#Number of sub Selection regions
NList = np.arange(1,2002,10)

#Proportion that is Selection
B = 0.5#[0.1,1,10]#10#dList = np.arange(1,11)

#Make dx 10 times smaller than the smallest L
dx = min(min(B,1-B)*D/NList)/100

#The uppermost x-bound: make it larger than necessary
xbound  =1000

#Initial proportion of R
Phi = 1e-5

#Time for which the pesticide is applied
PAP = 0.1


SaveDirName = ("SaveFiles/"+
            "D_%0.3f"%(D) +
            "_B_%0.3f"%(B) + 
            "_MinN_%0.5f_MaxN_%0.5f_NNum_%d"%(min(NList),max(NList),len(NList)) +
            "_xbound_%d"%(xbound) + 
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
