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

for d in dirlist:
    w,MinGrad,MindR,MinCurv,Phi,PAP = Plotting.Single_w_Plot(d)

    wList.append(w)
    MinGradList.append(MinGrad)
    MindRList.append(MindR)
    MinCurvList.append(MinCurv)
    print("Finished",d)


wList,MinGradList,MindRList,MinCurvList = zip(*sorted(zip(wList,MinGradList,MindRList,MinCurvList)))

wList = np.asarray(wList)
MinGradList = np.asarray(MinGradList)
MindRList = np.asarray(MindRList)
MinCurvList = np.asarray(MinCurvList)


MinGradTheory = np.sqrt(PAP)*np.pi/(wList * np.sqrt(np.log(8*wList*(1-Phi)/(Phi*np.pi**2))))
fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(np.log10(wList),MinGradList,c='k',s=200)
plt.plot(np.log10(wList),np.log10(MinGradTheory),'--g',linewidth=5)

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



MinCurvTheory = 4 * np.sqrt(1-PAP)/(1-wList) * special.erfinv(1-Phi/(1-Phi))
fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(np.log10(1-wList),MinCurvList,c='k',s=200)
plt.plot(np.log10(1-wList),np.log10(MinCurvTheory),'--g',linewidth=5)

#Formatting
ax.set_xticks([-1,0])
ax.set_xticklabels(
    [r'$10^{-1}$',r'$10^{0}$'])

ax.set_yticks([1,2])
ax.set_yticklabels(
    [r'$10^{1}$',r'$10^{2}$'])

plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

plt.savefig(str(directory)+ "/LU.png",bbox_inches='tight')
plt.close()
