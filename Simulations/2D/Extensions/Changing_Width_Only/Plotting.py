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

if __name__ == "__main__":
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

    directory = str(args.directory)


def Single_Height(directory):
    ###############################
    ##Extract Data#################
    ###############################
    filename = 'datafile.npz'


    #Find list of all the datafiles
    tempdirlist = os.listdir(directory)
    dirlist = []
    for i in tempdirlist:
        if os.path.isdir(os.path.join(directory,i)):
            dirlist.append(os.path.join(directory,i))

    print("Dirlist:",dirlist)

    LList = []
    dRList = []
    #I_dRList = []
    #I_TOT_dRList = []
    #P_dRList = []

    for i in dirlist:
        try:
            with np.load(os.path.join(i,filename)) as data:
                L = data["field_width"]
                print("Region Length:",L)
                PAP = data["PAP"]
                Phi = data["Phi"]
                Change = data["Change"]
                #d = data["d"]
                #dx = data["dx"]
                #dt = data["dt"]
                FIXED_HEIGHT = data["FIXED_HEIGHT"]

                LList.append(L)
                dRList.append(Change)


        except Exception as e: print(e)

        #L = C/N

        #Collect data
        ##LList.append(L)
        ##dRList.append(Change)
        #I_dRList.append(I_ApproxIntegral)
        #I_TOT_dRList.append(I_TOT_ApproxIntegral)
        #P_dRList.append(P_ApproxIntegral)



    LList,dRList = zip(*sorted(zip(LList,dRList)))

    LList = np.asarray(LList)
    dRList = np.asarray(dRList)


    # Set the figure size in millimeters
    fig_width_mm = 150
    fig_height_mm = 100
    fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)  # Convert mm to inches (25.4 mm in an inch)
    #########################################################################
    # Change in R with changing L
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    plt.plot(np.log10(LList/FIXED_HEIGHT),np.log10(dRList/(LList*FIXED_HEIGHT)), '-k',linewidth=5)

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

    plt.savefig(str(directory) + "/dR.png",bbox_inches='tight',dpi=300)
    plt.savefig(str(directory) + "/dR.eps",bbox_inches='tight',dpi=300)
    plt.close()

    return (FIXED_HEIGHT,LList,dRList)

