from Params import *

import sys
sys.path.insert(0,'../../../CoreFunctions')

import Core

import numpy as np

import copy

import time






starttime = time.time()

#########################################
###Argparse##############################
#########################################
from argparse import ArgumentParser
parser = ArgumentParser(description='Number of Regions')
parser.add_argument('-L','--Length',type=float,required=True,
        help='Length of periodic subunit')
parser.add_argument('-P','--PAP',type=float,required=True,
        help='Proportion of system refuge')
parser.add_argument('-d','--dir',type=str,required=True,
        help='Name of sub save directory')
args = parser.parse_args()

L = float(args.Length)
PAP = float(args.PAP)
SaveDirName = str(args.dir)

NumSaveDirName = (SaveDirName +
    "/L_%0.5f"%(L))

if not os.path.isdir(NumSaveDirName):
    os.mkdir(NumSaveDirName)
    print("Created Directory for width",L)


#########################################
###Main Process##########################
#########################################

xlist, PAPDist = Core.PAPDist_Single(xbound,L,dx,Phi,PAP)

Kernel = Core.Kernel_Periodic(PAP,xlist,L)

EndDist = Core.EndDist_Single(PAPDist,Kernel,xlist,L,dx)

ApproxIntegral = Core.dR(Phi,EndDist,xlist)

########################################
###Time and Saving######################
########################################

endtime = time.time()
timetaken = endtime-starttime
print("Time Taken:",timetaken)


OutputDatafilename = NumSaveDirName + '/datafile.npz'
np.savez(OutputDatafilename,
    L=L,
    xbound=xbound,
    PAP=PAP,
    Phi=Phi,
    #C=C,
    #d=d,
    dx=dx,
    xlist=xlist,
    PAPDist=PAPDist,
    EndDist=EndDist,
    #dR=dR,
    ApproxIntegral=ApproxIntegral,
    #I_PAPSNum=I_PAPSNum,
    #I_ENDSNum=I_ENDSNum,
    #I_dR=I_dR,
    #I_ApproxIntegral=I_ApproxIntegral,
    #I_TOT_PAPSNum=I_TOT_PAPSNum,
    #I_TOT_ENDSNum=I_TOT_ENDSNum,
    #I_TOT_dR=I_TOT_dR,
    #I_TOT_ApproxIntegral=I_TOT_ApproxIntegral,
    #P_xlist = P_xlist,
    #P_PAPSNum=P_PAPSNum,
    #P_ENDSNum=P_ENDSNum,
    #P_dR=P_dR,
    #P_ApproxIntegral=P_ApproxIntegral,
    timetaken=timetaken)
