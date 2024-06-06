import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.patches as patches


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

import copy


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




    #Set the figure size in millimeters
    fig_width_mm = 85
    fig_height_mm = 50
    fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)
    fig,ax = plt.subplots(figsize = fig_size)


    #Demands the first and last points of PAPDist are small enough
    MassagedPAPDist = copy.copy(PAPDist)

    MassagedPAPDist[MassagedPAPDist == 0] = Phi**3

    plt.plot(xlist,np.log10(MassagedPAPDist),'c',linewidth=10,zorder=0)
    plt.plot(xlist,np.log10(EndDist),'b',linewidth=10,zorder=0)
    
    plt.plot(xlist,np.log10(np.ones(len(xlist))*Phi),linewidth=10,color='orange',zorder=0)

    ax.axes.yaxis.set_visible(False)
    ax.axes.xaxis.set_visible(False)

    ylow = Phi**2
    yupp = 10**0.5


    plt.xlim(0,K)
    plt.ylim(np.log10(ylow),np.log10(yupp))


    ylow = Phi**2

    #Left Rect
    rect = patches.Rectangle((0,np.log10(ylow)),width=K*w,height=np.log10(10),linewidth=3, edgecolor='k', facecolor='white',zorder=1)
    ax.add_patch(rect)

    #Right Rect
    rect = patches.Rectangle((K*w,np.log10(ylow)),width=K*(1-w),height=np.log10(10),linewidth=3, edgecolor='k', facecolor='#808080',zorder=1)
    ax.add_patch(rect)


    plt.tight_layout()

    plt.savefig(str(i) + "/PAP_And_End.png",bbox_inches='tight',dpi=300)
    plt.close()

    """

    L = K*(1-w)

    xlow = 0-1.5 * L
    xupp = 2.5 *L

    yupp = 10**0.5
    ylow = Phi**2

    xticks = []
    for x in np.arange(int(xlow),int(xupp)+1):
        if x%10 == 0:
            xticks.append(x)

    def AddRects(ax,ylow):
        #Left Rect
        # Create a Rectangle patch
        rect = patches.Rectangle((xlow, np.log10(ylow)), abs(xlow), np.log10(10), linewidth=3, edgecolor='k', facecolor='white',zorder=1)
        # Add the patch to the Axes
        ax.add_patch(rect)

        #Right Rect
        #Left Rect
        # Create a Rectangle patch
        rect = patches.Rectangle((L, np.log10(ylow)), abs(xlow), np.log10(10), linewidth=3, edgecolor='k', facecolor='white',zorder=1)
        # Add the patch to the Axes
        ax.add_patch(rect)

        #Middle Ret
        # Create a Rectangle patch
        rect = patches.Rectangle((0, np.log10(ylow)), L, np.log10(10), linewidth=1, edgecolor='k', facecolor='#808080',zorder=1)
        # Add the patch to the Axes
        ax.add_patch(rect)

    def Setup(plt,ax,xlist,S,R,axisbool):
        ylow = Phi**2


        plt.plot(xlist,np.log10(S),linewidth=10,color='blue',zorder=0)
        plt.plot(xlist,np.log10(R),linewidth=10,color='orange',zorder=0)

        plt.xlim(xlow,xupp)


        if axisbool:
            plt.yticks(fontsize=30)

            ax.set_yticks([0,-2,-4,-6])
            ax.set_yticklabels(
                [r'$0$',r'$-2$',r'$-4$',r'$-6$'])

            ylow = Phi/10

        else:
            ax.axes.yaxis.set_visible(False)

        plt.ylim(np.log10(ylow),np.log10(yupp))

        AddRects(ax,ylow)

        ax.axes.xaxis.set_visible(False)
        plt.tight_layout()



    # Set the figure size in millimeters
    fig_width_mm = 125
    fig_height_mm = 80
    fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)

    InitDist = (1-Phi)* np.ones(len(PAPDist))
    InitDist[abs(xlist-L/2)<L/2] = 0

    RList = Phi* np.ones(len(PAPDist))

    cm = 1/2.54

    fig,ax = plt.subplots(figsize = fig_size)
    Setup(plt,ax,xlist,InitDist,RList,0)
    plt.savefig(str(i) + "/1_Init.png",bbox_inches='tight',dpi=300)
    plt.close()

    fig,ax = plt.subplots(figsize = fig_size)
    PAPDist[PAPDist<ylow/10] = ylow/10
    Setup(plt,ax,xlist,PAPDist,RList,0)
    plt.savefig(str(i) + "/2_PAP.png",bbox_inches='tight',dpi=300)
    plt.close()

    fig,ax = plt.subplots(figsize = fig_size)
    Setup(plt,ax,xlist,EndDist,RList,0)
    plt.savefig(str(i) + "/3_End.png",bbox_inches='tight',dpi=300)
    plt.close()

    fig,ax = plt.subplots(figsize = fig_size)
    Setup(plt,ax,xlist,EndDist/(EndDist+RList),RList/(EndDist+RList),0)
    plt.savefig(str(i) + "/4_PostBreed.png",bbox_inches='tight',dpi=300)
    plt.close()


    fig,ax = plt.subplots(figsize = fig_size)
    Setup(plt,ax,xlist,0*np.zeros(len(RList)),RList/(EndDist+RList),1)
    plt.savefig(str(i) + "/5_PostBreedROnly.png",bbox_inches='tight',dpi=300)
    plt.close()


    """




















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
#########################################################################
#Extract Isolated Data

IsolatedLList = np.asarray([1.00000000e-02, 1.09749877e-02, 1.20450354e-02, 1.32194115e-02,
       1.45082878e-02, 1.59228279e-02, 1.74752840e-02, 1.91791026e-02,
       2.10490414e-02, 2.31012970e-02, 2.53536449e-02, 2.78255940e-02,
       3.05385551e-02, 3.35160265e-02, 3.67837977e-02, 4.03701726e-02,
       4.43062146e-02, 4.86260158e-02, 5.33669923e-02, 5.85702082e-02,
       6.42807312e-02, 7.05480231e-02, 7.74263683e-02, 8.49753436e-02,
       9.32603347e-02, 1.02353102e-01, 1.12332403e-01, 1.23284674e-01,
       1.35304777e-01, 1.48496826e-01, 1.62975083e-01, 1.78864953e-01,
       1.96304065e-01, 2.15443469e-01, 2.36448941e-01, 2.59502421e-01,
       2.84803587e-01, 3.12571585e-01, 3.43046929e-01, 3.76493581e-01,
       4.13201240e-01, 4.53487851e-01, 4.97702356e-01, 5.46227722e-01,
       5.99484250e-01, 6.57933225e-01, 7.22080902e-01, 7.92482898e-01,
       8.69749003e-01, 9.54548457e-01, 1.04761575e+00, 1.14975700e+00,
       1.26185688e+00, 1.38488637e+00, 1.51991108e+00, 1.66810054e+00,
       1.83073828e+00, 2.00923300e+00, 2.20513074e+00, 2.42012826e+00,
       2.65608778e+00, 2.91505306e+00, 3.19926714e+00, 3.51119173e+00,
       3.85352859e+00, 4.22924287e+00, 4.64158883e+00, 5.09413801e+00,
       5.59081018e+00, 6.13590727e+00, 6.73415066e+00, 7.39072203e+00,
       8.11130831e+00, 8.90215085e+00, 9.77009957e+00, 1.07226722e+01,
       1.17681195e+01, 1.29154967e+01, 1.41747416e+01, 1.55567614e+01,
       1.70735265e+01, 1.87381742e+01, 2.05651231e+01, 2.25701972e+01,
       2.47707636e+01, 2.71858824e+01, 2.98364724e+01, 3.27454916e+01,
       3.59381366e+01, 3.94420606e+01, 4.32876128e+01, 4.75081016e+01,
       5.21400829e+01, 5.72236766e+01, 6.28029144e+01, 6.89261210e+01,
       7.56463328e+01, 8.30217568e+01, 9.11162756e+01, 1.00000000e+02])
IsolateddRList = np.asarray([8.51868199e-06, 8.53221486e-06, 8.54707474e-06, 8.56339112e-06,
       8.58130996e-06, 8.60099229e-06, 8.62260473e-06, 8.64634715e-06,
       8.67242724e-06, 8.70107588e-06, 8.73255003e-06, 8.76713615e-06,
       8.80514054e-06, 8.84691044e-06, 8.89282475e-06, 8.94329926e-06,
       8.99879942e-06, 9.05983496e-06, 9.12697244e-06, 9.20083768e-06,
       9.28212559e-06, 9.37160403e-06, 9.47012929e-06, 9.57865326e-06,
       9.69822485e-06, 9.83002823e-06, 9.97537593e-06, 1.01357356e-05,
       1.03127499e-05, 1.05082615e-05, 1.07243450e-05, 1.09633241e-05,
       1.12278349e-05, 1.15208566e-05, 1.18457683e-05, 1.22064165e-05,
       1.26071950e-05, 1.30531336e-05, 1.35500295e-05, 1.41045605e-05,
       1.47244965e-05, 1.54188759e-05, 1.61983027e-05, 1.70752634e-05,
       1.80645588e-05, 1.91838530e-05, 2.04543470e-05, 2.19017036e-05,
       2.35572289e-05, 2.54594147e-05, 2.76560560e-05, 3.02070681e-05,
       3.31883728e-05, 3.66972934e-05, 4.08601675e-05, 4.58432567e-05,
       5.18686746e-05, 5.92381109e-05, 6.83688766e-05, 7.98500911e-05,
       9.45325533e-05, 1.13676724e-04, 1.39204568e-04, 1.74144149e-04,
       2.23446856e-04, 2.95561324e-04, 4.05625241e-04, 5.82333933e-04,
       8.83747726e-04, 1.43658987e-03, 2.54296911e-03, 5.00115401e-03,
       1.11869822e-02, 2.91757233e-02, 9.00708085e-02, 3.14270665e-01,
       9.73602601e-01, 2.05922386e+00, 3.31628471e+00, 4.69827016e+00,
       6.21501983e+00, 7.87965116e+00, 9.70658182e+00, 1.17116358e+01,
       1.39121801e+01, 1.63272750e+01, 1.89778381e+01, 2.18868283e+01,
       2.50794416e+01, 2.85833307e+01, 3.24288440e+01, 3.66492910e+01,
       4.12812259e+01, 4.63647685e+01, 5.19439508e+01, 5.80670962e+01,
       6.47872404e+01, 7.21625908e+01, 8.02570286e+01, 8.91406646e+01])

#########################################################################
# Change in R with changing L
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.log10(LList),np.log10(dRList/(LList* (1-w))), '-k',linewidth=5)

plt.plot(np.log10(IsolatedLList/(1-w)),np.log10(IsolateddRList/IsolatedLList),color='gray',linewidth = 5)

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



# Set the figure size in millimeters
fig_width_mm = 400
fig_height_mm = 90


fig = plt.figure(2)
ax = fig.add_subplot(111)
plt.plot(np.log10(LList),np.log10(dRList/(LList*(1-w))), '-k',linewidth=5)

plt.plot(np.log10(IsolatedLList/(1-w)),np.log10(IsolateddRList/IsolatedLList),'gray',linestyle='dashed',linewidth = 5)


#Create the stretched version

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")



plt.figure(2).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)



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
#plt.plot([np.log10(LList[index]),np.log10(LList[index])],
#        [min(np.log10(dRList/LList)-0.2),np.log10(dRList/LList)[index]],
#        '--k',
#        linewidth = 5)

GradientLogdRList = np.asarray(GradientLogdRList)
index = np.argmin(GradientLogdRList)

#plt.plot([GradientLogLList[index],GradientLogLList[index]],
#        [min(np.log10(dRList/LList))-0.2,np.log10(dRList/LList)[index]],
#        '--k',
#        linewidth = 5)

MinGradient = GradientLogLList[index]



CurvLogdRList = np.asarray(CurvLogdRList)
print(CurvLogdRList)
CurvMinima = argrelextrema(CurvLogdRList, np.less)
index = CurvMinima[0][-1]
print(index)

#plt.plot([CurvLogLList[index],CurvLogLList[index]],
#        [min(np.log10(dRList/LList))-0.2,np.log10(dRList/LList)[index]],
#        '--k',
#        linewidth = 5)

MinCurvature = CurvLogLList[index]

plt.text(1.5,-1,r"$\alpha=%0.1f$"%(w),fontsize=30,fontname="Arial")


#Formatting
ax.set_xticks([0,MinGradient,MindR,MinCurvature,2])
ax.set_xticklabels(
    [r'$10^0$',r'$k_{L}$',r'$k^{*}$',r'$k_{U}$',r'$10^2$'])

ax.set_yticks([-4,-2,0])
ax.set_yticklabels(
    [r'$-4$',r'$-2$',r'$0$'])

plt.xlim(0,2)

#fig.set_figwidth(15)
ax.tick_params(axis='x', which='major', pad=15)
#fig.tight_layout()

#Saving
plt.savefig(str(args.directory) + '/dR_Detail.png',bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + '/dR_Detail.eps',bbox_inches='tight',dpi=300)


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
