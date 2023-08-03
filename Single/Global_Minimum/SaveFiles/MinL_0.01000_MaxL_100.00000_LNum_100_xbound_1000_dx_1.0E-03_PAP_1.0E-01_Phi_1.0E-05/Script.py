from Params import *

import sys
sys.path.insert(0,'../../CoreFunctions')

import Core

import numpy as np

import copy

import time






starttime = time.time()

#################################
###Argparse
#################################
from argparse import ArgumentParser
parser = ArgumentParser(description='Number of Regions')
parser.add_argument('-L','--Length',type=float,required=True,help='Length of Selection region')
args = parser.parse_args()

L = float(args.Length)

NumSaveDirName = (SaveDirName +
    "/L_%0.5f"%(L))

if not os.path.isdir(NumSaveDirName):
    os.mkdir(NumSaveDirName)
    print("Created Directory for width",L)


#########################################
###Main Process##########################
#########################################

xlist, PAPDist = Core.PAPDist_Single(xbound,L,dx,Phi,PAP)

Kernel = Core.Kernel(PAP,xlist)

EndDist = Core.EndDist_Single(PAPDist,Kernel,xlist,L,dx)

ApproxIntegral = Core.dR(Phi,EndDist,xlist)

"""
xlist = np.arange(-1000,1000+L,dx)

PAPSNum = np.zeros(len(xlist))
PAPSNum[xlist>L] = (1-Phi)*special.erf((xlist[xlist>L]-L)/np.sqrt(4*PAP))
PAPSNum[xlist<0] = (1-Phi)*special.erf((-xlist[xlist<0])/np.sqrt(4*PAP))

Kernel = 1/np.sqrt(4*np.pi*(1-PAP)) * np.exp(-xlist**2/(4*(1-PAP)))


EndSNum = conv_circ(PAPSNum, Kernel)/sum(Kernel)

EndSNum = np.roll(EndSNum,-int((len(xlist) - L/dx)/2))


#Breeding
RNum = Phi/(EndSNum + Phi)
#Change
dR = RNum - Phi


ApproxIntegral = integrate.simps(dR,xlist)
"""


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
