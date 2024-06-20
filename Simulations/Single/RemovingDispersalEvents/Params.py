import numpy as np
import os
import shutil



#Total width of Selection Region
LList = np.logspace(-6,2,100)

"""
#Number of sub Selection regions
NList = np.arange(1,21,1)

#Separations
d = 0.1#10#dList = np.arange(1,11)
"""

#Make dx 10 times smaller than the smallest L
dx = min(LList)/10

#The uppermost x-bound: make it larger than necessary
xbound  =10

#Initial proportion of R
Phi = 1e-5

#Time for which the pesticide is applied
PAP = 0.1

#Which Dispersal Event to Ignore.
# 0 = ignore none
# 1 = ignore selection phase migration
# 2 = ignore post selection phase migration
# 3 = ignore all migration
DispIgnore = 0




SaveDirName = ("SaveFiles/"+
            "MinL_%0.6f_MaxL_%0.5f_LNum_%d"%(min(LList),max(LList),len(LList)) +
            "_xbound_%d"%(xbound) + 
            "_dx_" + '{:.1E}'.format(dx) +
            "_PAP_" + '{:.1E}'.format(PAP) +
            "_Phi_"+'{:.1E}'.format(Phi))

if DispIgnore == 0:
    SaveDirName += "_AllMigrations"

if DispIgnore == 1:
    SaveDirName += "_OnlyPostSelectionMigration"

if DispIgnore == 2:
    SaveDirName += "_OnlySelectionMigration"

if DispIgnore == 3:
    SaveDirName += "_NoMigration"


if not os.path.isdir("SaveFiles"):
    os.mkdir("SaveFiles")


if not os.path.isdir(SaveDirName):
    os.mkdir(SaveDirName)
    print("Created Directory")

shutil.copyfile("Params.py", SaveDirName+'/Params.py')
shutil.copyfile("Script.py", SaveDirName+"/Script.py")
