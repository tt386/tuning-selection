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


HeightList = []
dRListList = []
LListList = []

for d in dirlist:
    FIXED_HEIGHT,LList,dRList = Plotting.Single_Height(d)

    HeightList.append(FIXED_HEIGHT)
    dRListList.append(dRList)
    LListList.append(LList)


HeightList,dRListList,LListList = zip(*sorted(zip(HeightList,dRListList,LListList)))


HeightList = np.asarray(HeightList)
dRListList = np.asarray(dRListList)
LListList = np.asarray(LListList)





# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100
fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)
#########################################################################
# Change in R with changing L
fig = plt.figure(1)
ax = fig.add_subplot(111)

for i in range(len(HeightList)):
    Height = HeightList[i]
    dRList = dRListList[i]
    LList = LListList[i]

    plt.plot(np.log10(LList/Height),np.log10(dRList/(LList*Height)), '-k',linewidth=5)

    symbol = "o"
    if i == 1: symbol = "s"
    if i == 2: symbol = "*"

    plt.scatter([np.log10(LList/Height)[-1]],[np.log10(dRList/(LList*Height))[-1]],marker=symbol,s=100,zorder=10,color='red')


    print(Height,np.log10(dRList/(LList*Height))[-1])

#Formatting
plt.xticks([0,1,2])

ax.set_xticks([0,1,2])
ax.set_xticklabels(
    [r'$10^0$',r'$10^1$',r'$10^2$'])

ax.set_yticks([-5,-4,-3,-2])
ax.set_yticklabels(
    ['$10^{-5}$',r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$'])


plt.figure(1).set_size_inches(fig_width_mm/25.4,fig_height_mm/25.4,forward=True)


ax.xaxis.set_tick_params(width=2)
ax.yaxis.set_tick_params(width=2)

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(args.directory) + "/Together.png",bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + "/Together.eps",bbox_inches='tight',dpi=300)
plt.close()
