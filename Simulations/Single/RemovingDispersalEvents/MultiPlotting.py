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


#List all directories
DirList = os.listdir(args.directory)

#Ensure only have list of directories
SaveFileDirList = [item for item in DirList if os.path.isdir(os.path.join(args.directory, item))]


print(SaveFileDirList)
DispIgnoreList = []
LListList = []
dRListList = []



for directory in SaveFileDirList:



    ###############################
    ##Extract Data#################
    ###############################
    filename = 'datafile.npz'


    #Find list of all the datafiles
    tempdirlist = os.listdir(os.path.join(args.directory,directory))
    dirlist = []
    for i in tempdirlist:
        if os.path.isdir(os.path.join(args.directory,directory,i)):
            dirlist.append(os.path.join(args.directory,directory,i))

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
                DispIgnore = data["DispIgnore"]

                
                #PAPDist = data["PAPDist"]
                #EndDist = data["EndDist"]
                #xlist = data["xlist"]
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


    LList,dRList = zip(*sorted(zip(LList,dRList)))

    LList = np.asarray(LList)
    dRList = np.asarray(dRList)

    LListList.append(LList)
    dRListList.append(dRList)
    DispIgnoreList.append(DispIgnore)
    #I_dRList = np.asarray(I_dRList)
    #I_TOT_dRList = np.asarray(I_TOT_dRList)
    #P_dRList = np.asarray(P_dRList)


print(repr(LList))

print(repr(dRList))
# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100
fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)
#########################################################################
# Change in R with changing L
fig = plt.figure(1)
ax = fig.add_subplot(111)


for i in range(len(DispIgnoreList)):
    DispIgnore = DispIgnoreList[i]
    LList = LListList[i]
    dRList = dRListList[i]

    if DispIgnore == 0:
        linestyle = 'solid'
        color = 'k'
        zorder = 1
    elif DispIgnore == 1:
        linestyle = 'dotted'
        color = 'dimgray'
        zorder = 3
    elif DispIgnore == 2:
        linestyle = 'dashed'
        color = 'gray'
        zorder = 2
    elif DispIgnore == 3:
        linestyle = 'dashdot'
        color = 'lightgray'
        zorder = 0


    plt.plot(np.log10(LList),np.log10(dRList/LList), color=color,linestyle=linestyle,linewidth=5,zorder=zorder)

#Formatting
#Formatting
plt.xticks([-2,-1,0,1,2])

ax.set_xticks([-6,-4,-2,0,2])
ax.set_xticklabels(
    ['$-6$',r'$-4$',r'$-2$',r'$0$',r'$2$'])

ax.set_yticks([-6,-4,-2,0,2])
ax.set_yticklabels(
    ['$-6$','$-4$',r'$-2$',r'$0$',r'$2$'])

plt.figure(1).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(args.directory) + "/dR.png",bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + "/dR.eps",bbox_inches='tight',dpi=300)
plt.close()

