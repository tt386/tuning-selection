from Params import *

import sys
sys.path.insert(0,'../CoreFunctions')

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
parser.add_argument('-N','--N',type=float,required=True,
        help='Number Selection regions')
args = parser.parse_args()

N = int(args.N)

NumSaveDirName = (SaveDirName +
    "/N_%d"%(N))

if not os.path.isdir(NumSaveDirName):
    os.mkdir(NumSaveDirName)
    print("Created Directory for Number",N)


#########################################
###Main Process##########################
#########################################

#Multiple
M_xlist, M_PAPDist = Core.PAPDist_Multiple_ConstrainedInfinite(C,N,xbound,d,dx,Phi,PAP)#Core.PAPDist_Single(xbound,L,dx,Phi,PAP)
Kernel = Core.Kernel(PAP,M_xlist)
M_EndDist = Core.EndDist_Single(M_PAPDist,Kernel,M_xlist,(N-1)*d+C,dx)
M_ApproxIntegral = Core.dR(Phi,M_EndDist,M_xlist)
print(N,"Finished Multiple")

#Isolated Approx
I_xlist,I_PAPDist = Core.PAPDist_Single(xbound,C/N,dx,Phi,PAP)
Kernel = Core.Kernel(PAP,I_xlist)
I_EndDist = Core.EndDist_Single(I_PAPDist,Kernel,I_xlist,C/N,dx)
I_ApproxIntegral = N*Core.dR(Phi,I_EndDist,I_xlist)
print(N,"Finished Isolated")

#Large Single Approx
I_TOT_xlist,I_TOT_PAPDist = Core.PAPDist_Single(xbound,C+(N-1)*d,dx,Phi,PAP)
Kernel = Core.Kernel(PAP,I_TOT_xlist)
I_TOT_EndDist = Core.EndDist_Single(I_TOT_PAPDist,Kernel,I_TOT_xlist,C+(N-1)*d,dx)
I_TOT_ApproxIntegral = Core.dR(Phi,I_TOT_EndDist,I_TOT_xlist)
print(N,"Finished Isolated Total")


#Periodic Approx
K = d+C/N
w = d/K
P_xlist,P_PAPDist = Core.PAPDist_Periodic(K,w,dx,Phi,PAP)
Kernel = Core.Kernel_Periodic(PAP,P_xlist,K)
P_EndDist = Core.EndDist_Periodic(P_PAPDist,Kernel,P_xlist,K,w,dx,PAP)
P_ApproxIntegral = N*Core.dR(Phi,P_EndDist,P_xlist)
print(N,"Finished Periodic")

########################################
###Time and Saving######################
########################################

endtime = time.time()
timetaken = endtime-starttime
print("Time Taken:",timetaken)


OutputDatafilename = NumSaveDirName + '/datafile.npz'
np.savez(OutputDatafilename,
    xbound=xbound,
    C=C,
    N=N,
    PAP=PAP,
    Phi=Phi,
    K=K,
    w=w,
    #C=C,
    d=d,
    dx=dx,
    #M_xlist=M_xlist,
    #M_PAPDist=M_PAPDist,
    #M_EndDist=M_EndDist,
    M_ApproxIntegral=M_ApproxIntegral,
    #I_xlist=I_xlist,
    #I_PAPDist=I_PAPDist,
    #I_EndDist=I_EndDist,
    I_ApproxIntegral=I_ApproxIntegral,
    #I_TOT_xlist=I_TOT_xlist,
    #I_TOT_PAPDist=I_TOT_PAPDist,
    #I_TOT_EndDist=I_TOT_EndDist,
    I_TOT_ApproxIntegral=I_TOT_ApproxIntegral,
    #P_xlist = P_xlist,
    #P_PAPDist=P_PAPDist,
    #P_EndDist=P_EndDist,
    P_ApproxIntegral=P_ApproxIntegral,
    timetaken=timetaken)
