import numpy as np

from scipy import integrate
from scipy import special

import copy
import sys

import time

def conv_circ( signal, ker ):
    '''
    Simulate diffusion of the pests from the PAP Distribution using
    Fourier Transforms

    ARGS:
    signal: real 1D numpy array:
        The PAPDist
    ker: real 1D numpy array:
        The diffusion kernel
    signal and ker must have same shape

    RETURNS:
    real 1D numpy array:
        The pre-breeding pest distribution
    '''
    return np.real(np.fft.ifft( np.fft.fft(signal)*np.fft.fft(ker) ))


def PAPDist_Single(xbound,L,dx,Phi,PAP):
    """
    Generate the distribution of Susceptibles at the end of Selection
    application for the case of a single region of selection pressure
    in an infinite region of Refuge.

    ARGS:
    xbound: float
        The upper and -lower bound of the xlist
    L: float
        The width of the selection region: 0<x<L
    dx: float
        The width of the spacing in the xlist
    Phi: float
        The initial proportion of resistance
    PAP: float
        The time over which selection pressure applied

    RETURNS
    xlist: 1D numpy array of floats:
        The spatial distribution
    PAPDist: 1D numpy array of floats:
        The distribution of Susceptibles at the end of selection pressure
    """

    xlist = np.arange(-xbound,xbound+L,dx)

    PAPDist = np.zeros(len(xlist))
    PAPDist[xlist>L] = (1-Phi)*special.erf((xlist[xlist>L]-L)/np.sqrt(4*PAP))
    PAPDist[xlist<0] = (1-Phi)*special.erf((-xlist[xlist<0])/np.sqrt(4*PAP))

    return xlist, PAPDist


def PAPDist_Periodic(K,w,dx,Phi,PAP):
    """
    Generate the distribution of Susceptibles at the end of Selection
    application for the case of a single region of selection pressure
    in an infinite region of Refuge.

    ARGS:
    K: float
        The width of the periodic subunit
    w: float
        The proportion of subunit that is Refuge 0<w<1
    dx: float
        The width of the spacing in the xlist
    Phi: float
        The initial proportion of resistance
    PAP: float
        The time over which selection pressure applied

    RETURNS
    xlist: 1D numpy array of floats:
        The spatial distribution
    PAPDist: 1D numpy array of floats:
        The distribution of Susceptibles at the end of selection pressure
    """

    xlist = np.arange(0,K,dx)

    PAPDist = np.zeros(len(xlist))

    for m in range(1000):
        PAPDist[xlist<K*w] += ((4*(1-Phi)/np.pi)
                * (1/(2*m+1)) 
                * np.sin((2*m+1)*np.pi*xlist[xlist<K*w]/(K*w)) 
                * np.exp(-((2*m+1)*np.pi/(K*w))**2 * PAP))

    return xlist, PAPDist




def Kernel(PAP,xlist):
    """
    Generate the diffusion Kernel

    ARGS:
    PAP: float
        The time over which selection pressure applied
    xlist: 1D numpy array of floats:
        The spatial distribution


    RETURNS:
    1D numpy array of floats:
        The Gaussian diffusion kernel
    """

    return 1/np.sqrt(4*np.pi*(1-PAP)) * np.exp(-xlist**2/(4*(1-PAP)))

def Kernel_Periodic(PAP,xlist,K):
    """
    Generate the diffusion Kernel

    ARGS:
    PAP: float
        The time over which selection pressure applied
    xlist: 1D numpy array of floats:
        The spatial distribution
    K: float
        The width of the periodic subunit

    RETURNS:
    1D numpy array of floats:
        The Gaussian diffusion kernel
    """

    return 1/np.sqrt(4*np.pi*(1-PAP)) * np.exp(-(xlist-K/2)**2/(4*(1-PAP)))

def EndDist_Single(PAPDist,Kernel,xlist,L,dx):
    """
    Generate the pre-breeding distribution of susceptibles

    ARGS:
    PAPDist: 1D numpy array of floats:
        The distribution of Susceptibles at the end of selection pressure
    Kernel: 1D numpy array of floats:
        The Gaussian diffusion kernel
    xlist: 1D numpy array of floats:
        The spatial distribution
    L: float
        The width of the selection region: 0<x<L
    dx: float
        The width of the spacing in the xlist

    RETURNS:
    EndDist: 1D numpy array of floats:
        The Distribution of susceptibles before breeding.
    """

    EndDist = conv_circ(PAPDist,Kernel)/sum(Kernel)

    #Roll so centered correctly
    EndDist = np.roll(EndDist,-int((len(xlist)-L/dx)/2))

    return EndDist


def EndDist_Periodic(PAPDist,Kernel,xlist,K,w,dx,PAP):
    """
    Generate the pre-breeding distribution of susceptibles

    ARGS:
    PAPDist: 1D numpy array of floats:
        The distribution of Susceptibles at the end of selection pressure
    Kernel: 1D numpy array of floats:
        The Gaussian diffusion kernel
    xlist: 1D numpy array of floats:
        The spatial distribution
    K: float
        The width of the Periodic sub-region
    w: float
        Proportion of the sub-region which is Refuge
    dx: float
        The width of the spacing in the xlist

    RETURNS:
    EndDist: 1D numpy array of floats:
        The Distribution of susceptibles before breeding.
    """
    """
    EndDist = conv_circ(PAPDist,Kernel)/sum(Kernel)

    #Roll so centered correctly
    EndDist = np.roll(EndDist,-int((len(xlist)-K*w/dx)/2))
    """
    def A0(xlist,PAPDist,K):
        return 1/K * integrate.simps(PAPDist,xlist)

    def Am(xlist,PAPDist,K,m):
        return 2/K * integrate.simps(PAPDist*np.cos(2*np.pi*m*xlist/K),xlist)

    def Bm(xlist,PAPDist,K,m):
        return 2/K * integrate.simps(PAPDist*np.sin(2*np.pi*m*xlist/K),xlist)

    EndDist = A0(xlist,PAPDist,K)

    for m in range(1,1000):
        EndDist += ((Am(xlist,PAPDist,K,m) * np.cos(2*np.pi*m*xlist/K) +
                Bm(xlist,PAPDist,K,m) * np.sin(2*np.pi*m*xlist/K)) * 
                np.exp(-(1-PAP) * (2*m*np.pi/K)**2))



    return EndDist


def dR(Phi,EndDist,xlist):
    """
    Calculate the change in Resistance across the year

    ARGS:
    Phi: float
        The initial proportion of resistance
    EndDist: 1D numpy array of floats:
        The Distribution of susceptibles before breeding.
    xlist: 1D numpy array of floats:
        The spatial distribution

    RETURNS:
    ApproxIntegral: float
        The total change in resistants across a year
    """

    #Number of Resistants:
    RNum = Phi/(EndDist + Phi)

    #Change
    dR = RNum - Phi

    ApproxIntegral = integrate.simps(dR,xlist)

    return ApproxIntegral


