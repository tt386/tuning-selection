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
parser.add_argument("-a",'--plotall',type=int,help='Do you want all intermediate plots')
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
            L = data["L"]
            print("Region Length:",L)
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
    LList.append(L)
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

    """
    plt.figure()
    plt.plot(xlist,PAPDist)
    plt.plot(xlist,EndDist)
    plt.xlim(-L*5,L*6)
    plt.savefig(str(i) + "/" + "PAPandEnd.png")
    plt.close()
    """
    xlow = -1.5 * L
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
            plt.yticks(fontsize=50)

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

    if args.plotall:
        InitDist = (1-Phi)* np.ones(len(PAPDist))
        InitDist[abs(xlist-L/2)<L/2] = 0
        
        RList = Phi* np.ones(len(PAPDist))


        fig,ax = plt.subplots()
        Setup(plt,ax,xlist,InitDist,RList,0)
        plt.savefig(str(i) + "/1_Init.png",bbox_inches='tight')
        plt.close()

        fig,ax = plt.subplots()
        PAPDist[PAPDist<ylow/10] = ylow/10
        Setup(plt,ax,xlist,PAPDist,RList,0)
        plt.savefig(str(i) + "/2_PAP.png",bbox_inches='tight')
        plt.close()

        fig,ax = plt.subplots()
        Setup(plt,ax,xlist,EndDist,RList,0)
        plt.savefig(str(i) + "/3_End.png",bbox_inches='tight')
        plt.close()

        fig,ax = plt.subplots()
        Setup(plt,ax,xlist,EndDist/(EndDist+RList),RList/(EndDist+RList),0)
        plt.savefig(str(i) + "/4_PostBreed.png",bbox_inches='tight')
        plt.close()


        fig,ax = plt.subplots()
        Setup(plt,ax,xlist,0*np.zeros(len(RList)),RList/(EndDist+RList),1)
        plt.savefig(str(i) + "/5_PostBreedROnly.png",bbox_inches='tight')
        plt.close()

LList,dRList = zip(*sorted(zip(LList,dRList)))

LList = np.asarray(LList)
dRList = np.asarray(dRList)
#I_dRList = np.asarray(I_dRList)
#I_TOT_dRList = np.asarray(I_TOT_dRList)
#P_dRList = np.asarray(P_dRList)


print(repr(LList))

print(repr(dRList))


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
plt.savefig(str(args.directory) + "/dR_Grad.png",bbox_inches='tight')
plt.close()




MindR = LogLList[np.argmin(LogdRList)]
MinCurvature = CurvLogLList[np.argmin(CurvLogdRList)]






# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100
fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)
#########################################################################
# Change in R with changing L
fig = plt.figure(1)
ax = fig.add_subplot(111)
plt.plot(np.log10(LList),np.log10(dRList/LList), '-k',linewidth=5)

#Formatting
plt.xticks([-2,-1,0,1,2])

ax.set_xticks([-2,-1,0,1,2])
ax.set_xticklabels(
    ['$10^{-2}$',r'$10^{-1}$',r'$10^0$',r'$10^1$',r'$10^2$'])

ax.set_yticks([-4,-3,-2,-1,0])
ax.set_yticklabels(
    ['$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^0$'])


plt.figure(1).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(args.directory) + "/dR.png",bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + "/dR.eps",bbox_inches='tight',dpi=300)
plt.close()


#Create the stretched version

# Set the figure size in millimeters
fig_width_mm = 400
fig_height_mm = 90

fig = plt.figure(2)
ax = fig.add_subplot(111)
plt.plot(np.log10(LList),np.log10(dRList/LList), '-k',linewidth=5)

plt.figure(2).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)


#Formatting
plt.xticks([-2,-1,0,1,2])

ax.set_xticks([-2,-1,0,1,2])
ax.set_xticklabels(
    ['$10^{-2}$',r'$10^{-1}$',r'$10^0$',r'$10^1$',r'$10^2$'])

ax.set_yticks([-4,-3,-2,-1,0])
ax.set_yticklabels(
    ['$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^0$'])

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")



#Highlight the linearity
lowerL = np.log10(LList)[0]
lowerR = np.log10(dRList/LList)[0] + 0.5

upperL = lowerL + 0.5
upperR = -upperL + (lowerL + lowerR)
plt.plot([lowerL,upperL],[lowerR,upperR],'--g',linewidth='5',zorder=1)

plt.text(lowerL+0.25,lowerR,r"$w^{-1}$",fontsize=30,fontname="Arial")

#Highlight sub-figures

#Find the element closest to value:
def index_closest_value(array, target):
    absolute_diff = np.abs(array - target)
    index = np.argmin(absolute_diff)
    return index

target = 10
index = index_closest_value(LList,10)
#index = np.argmin(CurvLogdRList)-10
plt.scatter([np.log10(LList[index])],
        [np.log10(dRList/LList)[index]],color='Blue',s=750,
        edgecolors='black')


target = 20
index = index_closest_value(LList,target)
#index = np.argmin(CurvLogdRList)+10
plt.scatter([np.log10(LList[index])],
        [np.log10(dRList/LList)[index]],color='red',s=750,marker="D",
        edgecolors='black')

target = 40
index = index_closest_value(LList,target)
#index = np.argmin(CurvLogdRList)+20
plt.scatter([np.log10(LList[index])],
        [np.log10(dRList/LList)[index]],color='cyan',s=750,marker="s",
        edgecolors='black')


"""
#Dashed line for the location of L^* and LU
index = np.argmin(dRList/LList)
plt.plot([np.log10(LList[index]),np.log10(LList[index])],
        [min(np.log10(dRList/LList)-0.2),np.log10(dRList/LList)[index]],
        '--k',
        linewidth = 5)


index = np.argmin(CurvLogdRList)+1
plt.plot([np.log10(LList[index]),np.log10(LList[index])],
        [min(np.log10(dRList/LList))-0.2,np.log10(dRList/LList)[index]],
        '--k',
        linewidth = 5)
"""
#Formatting
ax.set_xticks([-2,-1,MindR,MinCurvature,2])
ax.set_xticklabels(
    [r'$-2$',r'$-1$',r'$w^{*}$',r'$w_{U}$',r'$2$'])

ax.set_yticks([-4,-2,0])
ax.set_yticklabels(
    ['$-4$',r'$-2$',r'$0$'])


plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

#fig.set_figwidth(20)
ax.tick_params(axis='x', which='major', pad=15)
#fig.tight_layout()

#Saving
plt.savefig(str(args.directory) + '/dR_Stretch.png',bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + '/dR_Stretch.eps',bbox_inches='tight',dpi=300)



plt.close()




print("L at min R: ", 10**MindR)


#########################################################################





