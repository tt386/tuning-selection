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

import matplotlib.cm as cm
import matplotlib.colors as mcolors



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


AreaList = []
dRListList = []
aListList = []

for d in dirlist:
    Area,aList,dRList = Plotting.Single_Height(d)

    AreaList.append(Area)
    dRListList.append(dRList)
    aListList.append(aList)

AreaList,dRListList,aListList = zip(*sorted(zip(AreaList,dRListList,aListList)))


AreaList = np.asarray(AreaList)
dRListList = np.asarray(dRListList)
aListList = np.asarray(aListList)





# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100
fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)
#########################################################################
# Change in R with changing L
fig = plt.figure(1)
ax = fig.add_subplot(111)

for i in range(len(AreaList)):
    Area = AreaList[i]
    dRList = dRListList[i]
    aList = aListList[i]

    plt.plot(np.log10(aList),np.log10(dRList/(Area)), '-k',linewidth=5,alpha = min(1,(i+1)*0.333))

    """
    symbol = "o"
    if Height == 1: symbol = "s"
    if Height == 10: symbol = "*"

    size = 100
    if Height == 10: size=150

    plt.scatter([np.log10(LList/Height)[-1]],[np.log10(dRList/(LList*Height))[-1]],marker=symbol,s=size,zorder=10,color='red')

    """
    print(Area,np.log10(dRList/(Area))[-1])

#Formatting
plt.xticks([0,1,2])

ax.set_xticks([0,1,2])
ax.set_xticklabels(
    [r'$10^0$',r'$10^1$',r'$10^2$'])

ax.set_yticks([-4.6,-4.4,-4.2])
ax.set_yticklabels(
    ['$10^{-4.6}$',r'$10^{-4.4}$',r'$10^{-4.2}$'])


plt.figure(1).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)

plt.ylim(-4.65,-4.2)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(args.directory) + "/Together.png",bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + "/Together.eps",bbox_inches='tight',dpi=300)
plt.close()
