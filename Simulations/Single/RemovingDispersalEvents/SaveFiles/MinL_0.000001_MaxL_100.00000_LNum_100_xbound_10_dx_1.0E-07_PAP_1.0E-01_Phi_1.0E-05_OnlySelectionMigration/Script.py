from Params import *

import sys
sys.path.insert(0,'../../CoreFunctions')

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
        help='Length of Selection region')
args = parser.parse_args()

L = float(args.Length)

NumSaveDirName = (SaveDirName +
    "/L_" + '{:.3E}'.format(L))

if not os.path.isdir(NumSaveDirName):
    os.mkdir(NumSaveDirName)
    print("Created Directory for width",L)


#########################################
###Main Process##########################
#########################################

#Because of how low we go, set dx dynamically

#The smallest resolution of diffusion effects is of order magnitude 1, so smallest value should be 1/100

#But when L is smaller than this, shoudl default to 100 times smaller than that.

dx = min(L/100,1/100)

#If we DO consider initial migration during selection period
if DispIgnore in [0,2]:
    xlist, PAPDist = Core.PAPDist_Single(xbound,L,dx,Phi,PAP)

#Correspondingly if we ignore initial selection migration
else:
    xlist = np.arange(-xbound,xbound+L,dx)

    PAPDist = np.zeros(len(xlist))
    PAPDist[xlist>L] = (1-Phi)
    PAPDist[xlist<0] = (1-Phi)

#If we do consider migration during the post selection
if DispIgnore in [0,1]:
    Kernel = Core.Kernel(PAP,xlist)
    EndDist = Core.EndDist_Single(PAPDist,Kernel,xlist,L,dx)

#If ignore selection during post migration.
else:
    EndDist = PAPDist

ApproxIntegral = Core.dR(Phi,EndDist,xlist)

########################################
###Time and Saving######################
########################################

endtime = time.time()
timetaken = endtime-starttime
print("Time Taken:",timetaken)


OutputDatafilename = NumSaveDirName + '/datafile.npz'
np.savez(OutputDatafilename,
    xbound=xbound,
    L=L,
    PAP=PAP,
    Phi=Phi,
    #C=C,
    #d=d,
    dx=dx,
    #xlist=xlist,
    #PAPDist=PAPDist,
    #EndDist=EndDist,
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
    DispIgnore = DispIgnore,
    timetaken=timetaken)
