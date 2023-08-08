import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt

plt.rcParams['text.usetex'] = True
mpl.rcParams.update(mpl.rcParamsDefault)

import numpy as np
import time

from scipy.stats import linregress

from scipy.optimize import curve_fit

import sys

import scipy.integrate as integrate
import scipy.special as special

from scipy.signal import argrelextrema

import os

starttime = time.time()
################################
##ArgParse######################
################################
import os.path

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The Directory %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

from argparse import ArgumentParser

parser = ArgumentParser(description='Plotting')
parser.add_argument('-d','--directory',help='The directory of the data')
args = parser.parse_args()

###############################
##Extract Data#################
###############################
filename = 'datafile.npz'


#Find list of all the datafiles
tempdirlist = os.listdir(args.directory)
dirlist = []
for i in tempdirlist:
    if os.path.isdir(os.path.join(args.directory,i)):
        dirlist.append(os.path.join(args.directory,i))

print("Dirlist:",dirlist)

LList = []
dRList = []
#I_dRList = []
#I_TOT_dRList = []
#P_dRList = []

for i in dirlist:
    try:
        with np.load(os.path.join(i,filename)) as data:
            K = data["K"]
            w = data["w"]
            print("Subregion Length:",K)
            PAP = data["PAP"]
            Phi = data["Phi"]
            #C = data["C"]
            #d = data["d"]
            dx = data["dx"]
            #dt = data["dt"]

            
            PAPDist = data["PAPDist"]
            EndDist = data["EndDist"]
            xlist = data["xlist"]
            #dR = data["dR"]
            ApproxIntegral = data["ApproxIntegral"]

            #I_PAPSNum = data["I_PAPSNum"]
            #I_ENDSNum = data["I_ENDSNum"]
            #I_dR = data["I_dR"]
            #I_ApproxIntegral = data["I_ApproxIntegral"]

            #I_TOT_PAPSNum = data["I_TOT_PAPSNum"]
            #I_TOT_ENDSNum = data["I_TOT_ENDSNum"]
            #I_TOT_dR = data["I_TOT_dR"]
            #I_TOT_ApproxIntegral = data["I_TOT_ApproxIntegral"]

            #P_PAPSNum = data["P_PAPSNum"]
            #P_ENDSNum = data["P_ENDSNum"]
            #P_dR = data["P_dR"]
            #P_ApproxIntegral = data["P_ApproxIntegral"]
            #P_xlist = data["P_xlist"]

            timetaken = data["timetaken"]
            print("dir found")

    except Exception as e: print(e)

    #L = C/N

    #Collect data
    LList.append(K)
    dRList.append(ApproxIntegral)
    #I_dRList.append(I_ApproxIntegral)
    #I_TOT_dRList.append(I_TOT_ApproxIntegral)
    #P_dRList.append(P_ApproxIntegral)


    #PAP Dists
    def Plot(xlist,Dist,xlim,ylim,name):
        plt.figure()
        plt.semilogy(xlist,Dist,label='S')
        plt.semilogy(xlist,np.ones(len(Dist))*Phi, label='R')

        plt.xlim(0,xlim)
        plt.ylim(Phi/10,1.1)
        plt.xlabel("Space")
        plt.ylabel("Number")
        plt.title(name)
        plt.savefig(str(i) + "/" + str(name) + ".png")
        plt.close()


    plt.figure()
    plt.plot(xlist,PAPDist)
    plt.plot(xlist,EndDist)
    plt.xlim(0,K)
    plt.savefig(str(i) + "/" + "PAPandEnd.png")
    plt.close()

    """
    # Multiple
    Plot(xlist,PAPSNum,C+N*d,1.1,"Multiple_PAP")
    Plot(xlist,ENDSNum,C+N*d,1.1,"Multiple_END")
    Plot(xlist,Phi/(Phi+ENDSNum),C+N*d,max(Phi/(Phi+ENDSNum)),"Multiple_dR")
    
    # Isolated
    Plot(xlist,I_PAPSNum,C+N*d,1.1,"Isolated_PAP")
    Plot(xlist,I_ENDSNum,C+N*d,1.1,"Isolated_END")
    Plot(xlist,Phi/(Phi+I_ENDSNum),C+N*d,max(Phi/(Phi+I_ENDSNum)),"Isolated_dR")

    # Tot Isolated
    Plot(xlist,I_TOT_PAPSNum,C+N*d,1.1,"IsolatedTOT_PAP")
    Plot(xlist,I_TOT_ENDSNum,C+N*d,1.1,"IsolatedTOT_END")
    Plot(xlist,Phi/(Phi+I_TOT_ENDSNum),C+N*d,max(Phi/(Phi+I_TOT_ENDSNum)),"IsolatedTOT_dR")

    # Periodic
    Plot(P_xlist,P_PAPSNum,L+d,1.1,"Periodic_PAP")
    Plot(P_xlist,P_ENDSNum,L+d,1.1,"Periodic_END")
    Plot(P_xlist,Phi/(Phi+P_ENDSNum),L+d,max(Phi/(Phi+P_ENDSNum)),"Periodic_dR")
    """
    """

    plt.figure()
    plt.plot(xlist,PAPSNum)

    plt.xlim(0,C+N*d)

    plt.xlabel("Space")
    plt.ylabel("Number")
    plt.title("PAP Dist")
    plt.savefig(str(i) + "/PAP.png")
    plt.close()

    #########

    plt.figure()
    plt.plot(xlist,ENDSNum)

    plt.xlim(0,C+N*d)

    plt.xlabel("Space")
    plt.ylabel("Number")
    plt.title("End Dist")
    plt.savefig(str(i) + "/End.png")
    plt.close()

    ##########

    plt.figure()
    plt.plot(xlist,Phi/(Phi+ENDSNum))

    plt.xlim(0,C+N*d)

    plt.xlabel("Space")
    plt.ylabel("Number")
    plt.title("Changing R")
    plt.savefig(str(i) + "/DR.png")
    plt.close()
    
    ##########
    """
    
LList,dRList = zip(*sorted(zip(LList,dRList)))

LList = np.asarray(LList)
dRList = np.asarray(dRList)

#########################################################################
###Create Gradient and Curvature Plots
#Gradient
GradientLogLList = []
GradientLogdRList = []

LogLList = np.log10(LList)
LogdRList= np.log10(dRList/LList)

dLogL = LogLList[1]-LogLList[0]

for i in range(1,len(LList)):
    GradientLogLList.append(LogLList[i]-dLogL/2)
    GradientLogdRList.append((LogdRList[i]-LogdRList[i-1])/dLogL)

plt.figure()
plt.plot(GradientLogLList,GradientLogdRList)
plt.savefig(str(args.directory) + "/dR_Grad.png",bbox_inches='tight')
plt.close()



#Curvature
CurvLogLList = []
CurvLogdRList = []


for i in range(1,len(GradientLogLList)):
    CurvLogLList.append(GradientLogLList[i]-dLogL/2)
    CurvLogdRList.append(
            (GradientLogdRList[i]-GradientLogdRList[i-1])/dLogL)

plt.figure()
plt.plot(CurvLogLList,CurvLogdRList)
plt.savefig(str(args.directory) + "/dR_Curv.png",bbox_inches='tight')
plt.close()




MindR = LogLList[np.argmin(LogdRList)]
MinGradient = GradientLogLList[np.argmin(GradientLogdRList)]
MinCurvature = CurvLogLList[np.argmin(CurvLogdRList)]







#########################################################################
# Change in R with changing L
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.log10(LList),np.log10(dRList/LList), '-k',linewidth=5)

#Formatting
ax.set_xticks([0,1,2])
ax.set_xticklabels(
    [r'$10^{0}$',r'$10^{1}$',r'$10^2$'])

ax.set_yticks([-2,-1,0])
ax.set_yticklabels(
    [r'$10^{-2}$',r'$10^{-1}$',r'$10^0$'])

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(args.directory) + "/dR.png",bbox_inches='tight')
plt.savefig(str(args.directory) + "/dR.eps",bbox_inches='tight')
plt.close()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.log10(LList),np.log10(dRList/LList), '-k',linewidth=5)
#Create the stretched version

plt.xticks(fontsize=50,fontname = "Arial")
plt.yticks(fontsize=50,fontname = "Arial")

"""
#Highlight the linearity
lowerL = np.log10(LList)[0]
lowerR = np.log10(dRList/LList)[0] + 0.5

upperL = lowerL + 0.5
upperR = -upperL + (lowerL + lowerR)
plt.plot([lowerL,upperL],[lowerR,upperR],'g',linewidth='5',zorder=1)

plt.text(lowerL+0.25,lowerR,r"$L^{-1}$",fontsize=50,fontname="Arial")
"""
"""
#Highlight sub-figures
index = np.argmin(CurvLogdRList)-10
plt.scatter([np.log10(LList[index])],
        [np.log10(dRList/LList)[index]],color='Blue',s=750)

index = np.argmin(CurvLogdRList)+10
plt.scatter([np.log10(LList[index])],
        [np.log10(dRList/LList)[index]],color='red',s=750)

index = np.argmin(CurvLogdRList)+20
plt.scatter([np.log10(LList[index])],
        [np.log10(dRList/LList)[index]],color='yellow',s=750)
"""


#Dashed line for the location of L^* and LU
index = np.argmin(dRList/LList)
plt.plot([np.log10(LList[index]),np.log10(LList[index])],
        [min(np.log10(dRList/LList)-0.2),np.log10(dRList/LList)[index]],
        '--k',
        linewidth = 5)


index = np.argmin(GradientLogdRList)
plt.plot([np.log10(LList[index]),np.log10(LList[index])],
        [min(np.log10(dRList/LList))-0.2,np.log10(dRList/LList)[index]],
        '--k',
        linewidth = 5)


CurvLogdRList = np.asarray(CurvLogdRList)
print(CurvLogdRList)
CurvMinima = argrelextrema(CurvLogdRList, np.less)
index = CurvMinima[0][-1]
print(index)
#LastMin = CurvLogdRList[index]
#index = np.where(CurvLogdRList == LastMin)[0]
#index = np.argmin(CurvLogdRList)
plt.plot([CurvLogLList[index],CurvLogLList[index]],
        [min(np.log10(dRList/LList))-0.2,np.log10(dRList/LList)[index]],
        '--k',
        linewidth = 5)

MinCurvature = CurvLogLList[index]

plt.text(1.5,-1,r"$\omega=%0.1f$"%(w),fontsize=50,fontname="Arial")


#Formatting
ax.set_xticks([0,MinGradient,MindR,MinCurvature,2])
ax.set_xticklabels(
    [r'$10^0$',r'$K_{L}$',r'$K^{*}$',r'$K_{U}$',r'$10^2$'])

ax.set_yticks([-2,0])
ax.set_yticklabels(
    [r'$-2$',r'$0$'])

plt.xlim(0,2)

fig.set_figwidth(15)
ax.tick_params(axis='x', which='major', pad=15)
fig.tight_layout()

#Saving
plt.savefig(str(args.directory) + '/dR_Detail.png',bbox_inches='tight')
plt.savefig(str(args.directory) + '/dR_Detail.eps',bbox_inches='tight')


plt.close()




print("L at min R: ", 10**MindR)


#########################################################################





"""
# Change in R with changing L
plt.figure()
plt.semilogy(C/NList,dRList,'-ko', label = 'Multiple')
plt.semilogy(C/NList,I_dRList*NList,'-bx', label = 'Isolated',alpha=0.5)
plt.semilogy(C/NList,I_TOT_dRList,'-r+',label = 'Total Isolated',alpha=0.5)
plt.semilogy(C/NList,P_dRList*NList, '-gD', label = 'Periodic',alpha=0.5)

plt.legend(loc = 'upper right')

plt.xlabel("Length of sub-patches")
plt.ylabel("Change in R")
plt.savefig(str(args.directory) + "/dR_L.png")
plt.close()
"""
"""
#Gradient
GradientLogLList = []
GradientLogdRList = []

LogLList = np.log10(LList)
LogdRList= np.log10(dRList/LList)

dLogL = LogLList[1]-LogLList[0]

for i in range(1,len(LList)):
    GradientLogLList.append(LogLList[i]-dLogL/2)
    GradientLogdRList.append((LogdRList[i]-LogdRList[i-1])/dLogL)

plt.figure()
plt.plot(GradientLogLList,GradientLogdRList)
plt.savefig(str(args.directory) + "/dR_Grad.png",bbox_inches='tight')
plt.close()



#Curvature
CurvLogLList = []
CurvLogdRList = []


for i in range(1,len(GradientLogLList)):
    CurvLogLList.append(GradientLogLList[i]-dLogL/2)
    CurvLogdRList.append((GradientLogdRList[i]-GradientLogdRList[i-1])/dLogL)

plt.figure()
plt.plot(CurvLogLList,CurvLogdRList)
plt.savefig(str(args.directory) + "/dR_Grad.png",bbox_inches='tight')
plt.close()






"""
