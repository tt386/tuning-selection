import numpy as np
import os
import shutil


#Area of the field
A = 25


aspectratio_list = np.logspace(np.log10(3),np.log10(200),21)

#Initial proportion of R
Phi = 1e-5

#Time for which the pesticide is applied
PAP = 0.1

#Timesteps
dt = 1e-3



#Spatial resolution
dx = 0.001#0.01

SaveDirName = ("SaveFiles/"+
            "Mina_%0.5f_Maxa_%0.5f_aNum_%d"%(min(aspectratio_list),max(aspectratio_list),len(aspectratio_list)) +
            "_Area_%0.3f"%(A) +
            "_PAP_" + '{:.1E}'.format(PAP) +
            "_Phi_"+'{:.1E}'.format(Phi) +
            "_dt_" + '{:.1E}'.format(dt) + 
            "_dx_" + '{:.1E}'.format(dx))


if not os.path.isdir("SaveFiles"):
    os.mkdir("SaveFiles")


if not os.path.isdir(SaveDirName):
    os.mkdir(SaveDirName)
    print("Created Directory")

shutil.copyfile("Params.py", SaveDirName+'/Params.py')
shutil.copyfile("Script.py", SaveDirName+"/Script.py")
