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


PAPList = []
MinGradList = []
MindRList = []
MinCurvList = []

for d in dirlist:
    MinGrad,MindR,MinCurv,Phi,PAP = Plotting.Single_w_Plot(d)

    PAPList.append(PAP)
    MinGradList.append(MinGrad)
    MindRList.append(MindR)
    MinCurvList.append(MinCurv)
    print("Finished",d)


PAPList,MinGradList,MindRList,MinCurvList = zip(*sorted(zip(PAPList,MinGradList,MindRList,MinCurvList)))

PAPList = np.asarray(PAPList)
MinGradList = np.asarray(MinGradList)
MindRList = np.asarray(MindRList)
MinCurvList = np.asarray(MinCurvList)

"""
MinGradTheory = np.sqrt(PAP)*np.pi/(PAPList * np.sqrt(np.log(8*PAPList*(1-Phi)/(Phi*np.pi**2))))
fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(np.log10(PAPList),MinGradList,c='k',s=200)
plt.plot(np.log10(PAPList),np.log10(MinGradTheory),'--g',linewidth=5)

#Formatting
ax.set_xticks([-1,0])
ax.set_xticklabels(
    [r'$10^{-1}$',r'$10^{0}$'])

ax.set_yticks([-0.6,0,0.6])
ax.set_yticklabels(
    [r'$10^{-0.6}$',r'$10^{0}$',r'$10^{0.6}$'])

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(directory)+ "/LL.png",bbox_inches='tight')
plt.close()
"""


MinCurvTheory = 4 * np.sqrt(1-PAPList) *  special.erfinv(1-Phi/(1-Phi))

# Set the figure size in millimeters
fig_width_mm = 150
fig_height_mm = 100
fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)

fig = plt.figure(figsize=fig_size)
ax = fig.add_subplot(111)
plt.scatter(np.log10(1-PAPList),MinCurvList,c='k',s=200)
plt.plot(np.log10(1-PAPList),np.log10(MinCurvTheory),'--g',linewidth=5)

#Formatting
ax.set_xticks([-1,0])
ax.set_xticklabels(
    [r'$-1$',r'$0$'])

ax.set_yticks([0.5,1])
ax.set_yticklabels(
    [r'$0.5$',r'$1$'])

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(directory)+ "/LU.png",bbox_inches='tight',dpi=300)
plt.close()
