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

import subprocess
import Plotting

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

directory = str(args.directory)


#Find list of all the datafiles
tempdirlist = os.listdir(directory)
dirlist = []
for i in tempdirlist:
    if os.path.isdir(os.path.join(directory,i)):
        dirlist.append(os.path.join(directory,i))


wList = []
MinGradList = []
MindRList = []
MinCurvList = []

dRListList = []

for d in dirlist:
    w,MinGrad,MindR,MinCurv,Phi,PAP,dRList,LList = Plotting.Single_w_Plot(d)

    wList.append(w)
    MinGradList.append(MinGrad)
    MindRList.append(MindR)
    MinCurvList.append(MinCurv)
    print("Finished",d)

    dRListList.append(dRList)




wList,MinGradList,MindRList,MinCurvList,dRListList = zip(*sorted(zip(wList,MinGradList,MindRList,MinCurvList,dRListList)))

wList = np.asarray(wList)
MinGradList = np.asarray(MinGradList)
MindRList = np.asarray(MindRList)
MinCurvList = np.asarray(MinCurvList)



# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100
fig = plt.figure(5)
ax = fig.add_subplot(111)

for i in range(len(wList)):
    plt.plot(np.log10(LList),np.log10(dRListList[i]/LList), '-k')

#Formatting
ax.set_xticks([0,1,2])
ax.set_xticklabels(
    [r'$10^{0}$',r'$10^{1}$',r'$10^2$'])

ax.set_yticks([-5,-4,-3,-2,-1,0])
ax.set_yticklabels(
    [r'$-5$',r'$-4$',r'$-3$',r'$-2$',r'$-1$',r'$0$'])


plt.figure(5).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)

ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(directory) + "/AllMinPlots.png",bbox_inches='tight',dpi=300)

plt.close()









MinGradTheory = np.sqrt(PAP)*np.pi/(wList * np.sqrt(np.log(8*wList*(1-Phi)/(Phi*np.pi**2))))


# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100

fig = plt.figure(1)
ax = fig.add_subplot(111)
plt.scatter(np.log10(wList),MinGradList,c='k',s=200)
plt.plot(np.log10(wList),np.log10(MinGradTheory),'--g',linewidth=5)

plt.scatter(np.log10(wList),MindRList,c='b',s=200)


#Formatting
ax.set_xticks([-1,0])
ax.set_xticklabels(
    [r'$-1$',r'$0$'])

ax.set_yticks([-0.6,0,0.6])
ax.set_yticklabels(
    [r'$-0.6$',r'$0$',r'$0.6$'])

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")


plt.figure(1).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

plt.savefig(str(directory)+ "/LL.png",bbox_inches='tight',dpi=300)
plt.close()



MinCurvTheory = 4 * np.sqrt(1-PAP)/(1-wList) * special.erfinv(1-Phi/(1-Phi))
fig = plt.figure(2)
ax = fig.add_subplot(111)
plt.scatter(np.log10(1-wList),MinCurvList,c='k',s=200)
plt.plot(np.log10(1-wList),np.log10(MinCurvTheory),'--g',linewidth=5)

plt.scatter(np.log10(1-wList),MindRList,c='b',s=200)


#Formatting
ax.set_xticks([-1,0])
ax.set_xticklabels(
    [r'$-1$',r'$0$'])

ax.set_yticks([1,2])
ax.set_yticklabels(
    [r'$1$',r'$2$'])

plt.figure(2).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)


plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(directory)+ "/LU.png",bbox_inches='tight',dpi=300)
plt.close()






fig = plt.figure(3)
ax = fig.add_subplot(111)

#Lower
plt.scatter((wList),MinGradList,c='r',edgecolors='k',s=200,zorder=1)
plt.plot((wList),np.log10(MinGradTheory),'--r',linewidth=5,zorder=0)

#Upper
plt.scatter((wList),MinCurvList,c='b',edgecolors='k',s=200,zorder=1)
plt.plot((wList),np.log10(MinCurvTheory),'--b',linewidth=5,zorder=0)

#Minimum
plt.scatter((wList),MindRList,c='k',s=200,zorder=1)


#Formatting
ax.set_xticks([0,1])
ax.set_xticklabels(
    [r'$0$',r'$1$'])

ax.set_yticks([-1,0,1,2])
ax.set_yticklabels(
    [r'$-1$',r'$0$',r'$1$',r'$2$'])

plt.figure(3).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)


plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

#fig.set_figwidth(20)
#ax.tick_params(axis='x', which='major', pad=15)
#fig.tight_layout()


plt.savefig(str(directory)+ "/Both.png",bbox_inches='tight',dpi=300)
plt.close()

