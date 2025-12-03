import numpy as np
import os
import shutil


width_list = np.logspace(-1,2,31)

#Initial proportion of R
Phi = 1e-5

#Time for which the pesticide is applied
PAP = 0.1

#Timesteps
dt = 1e-3

#killing parameter
k = 0.99

#Spatial resolution
dx = 0.001#0.01

SaveDirName = ("SaveFiles/"+
            "Minw_%0.5f_Maxw_%0.5f_LNum_%d"%(min(width_list),max(width_list),len(width_list)) +
            "_k_" + '{:.1E}'.format(k) +
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
