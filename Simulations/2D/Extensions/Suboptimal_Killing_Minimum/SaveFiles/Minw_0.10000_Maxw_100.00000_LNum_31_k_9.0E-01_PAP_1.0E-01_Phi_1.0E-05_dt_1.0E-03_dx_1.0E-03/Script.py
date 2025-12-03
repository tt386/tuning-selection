# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 15:47:27 2025

@author: thoma
"""
from Params import *
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
plt.rcParams['text.usetex'] = True
mpl.rcParams.update(mpl.rcParamsDefault)

from scipy.integrate import simps
import time

starttime = time.time()






#########################################
###Argparse##############################
#########################################
from argparse import ArgumentParser
parser = ArgumentParser(description='Number of Regions')
parser.add_argument('-L','--Length',type=float,required=True,
        help='Length of Selection region')
args = parser.parse_args()

field_width = float(args.Length)

NumSaveDirName = (SaveDirName +
    "/width_%0.5f"%(field_width))

if not os.path.isdir(NumSaveDirName):
    os.mkdir(NumSaveDirName)
    print("Created Directory for width",field_width)




# -----------------------------
# FFT split-step phase 1 solver
# -----------------------------
def phase1_fft_absorb(u0, dx, D, PAP, field_mask, dt=0.05):
    """
    Phase 1: periodic diffusion + strong killing in field.
    u0: (ny,nx) array at t=0
    field_mask: boolean array True inside field
    kappa: killing rate inside field (large => u~0 there)
    dt: can be large; method is stable
    """
    ny, nx = u0.shape
    u = u0.copy()

    # wavenumbers for periodic grid
    kx = 2*np.pi*np.fft.fftfreq(nx, d=dx)
    ky = 2*np.pi*np.fft.fftfreq(ny, d=dx)
    KX, KY = np.meshgrid(kx, ky)
    k2 = KX**2 + KY**2

    t = 0.0
    while t < PAP - 1e-12:
        dt_step = min(dt, PAP - t)

        # diffusion substep (exact in Fourier)
        u_hat = np.fft.fft2(u)
        u_hat *= np.exp(-D * k2 * dt_step)
        u = np.real(np.fft.ifft2(u_hat))

        # killing substep (exact pointwise)
        u[field_mask] *= k

        t += dt_step

    return u


##############################################################################
# Parameters
##############################################################################
L = field_width + 10.0   # padding choice

if field_width > 0.5:
    dx = 0.01
#dx = 0.01                # fixed spatial resolution
nx = ny = int(L / dx)


# After nx, ny defined
L_eff = nx * dx

ix0 = nx // 2
iy0 = ny // 2

n_field = int(np.round(field_width / dx))
if n_field % 2 == 0:
    n_field += 1

half_n = n_field // 2
field_mask = np.zeros((ny, nx), dtype=bool)
field_mask[iy0-half_n:iy0+half_n+1, ix0-half_n:ix0+half_n+1] = True

w_eff = n_field * dx
print("desired width =", field_width, "effective width =", w_eff)



D = 1.0
P = PAP
T = 1.0

##############################################################################
# Build numpy grid
# cell centers on [0, L)
##############################################################################
x = (np.arange(nx) + 0.5) * dx
y = (np.arange(ny) + 0.5) * dx
X, Y = np.meshgrid(x, y)

# initial condition
u0 = np.ones((ny, nx), dtype=float)

##############################################################################
# PHASE 1: 0 < t < PAP
# periodic diffusion + absorbing patch via FFT split-step
##############################################################################
print("Start phase 1 for field width:", field_width)

u_at_PAP = phase1_fft_absorb(
    u0=u0,
    dx=dx,
    D=D,
    PAP=PAP,
    field_mask=field_mask,
    dt=dt
)

print("PAP finished")

##############################################################################
# PHASE 2: PAP < t < 1
# free periodic diffusion in one go
##############################################################################
tau = T - PAP

kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(ny, d=dx)
KX, KY = np.meshgrid(kx, ky)

u_hat = np.fft.fft2(u_at_PAP)
propagator = np.exp(-D * (KX**2 + KY**2) * tau)
u_final_fft = np.real(np.fft.ifft2(u_hat * propagator))

print("System Ends")


##############################################################################
# PLOT RESULTS
##############################################################################

# Figure size in mm → inches
fig_width_mm = 150
fig_height_mm = 100
fig_size = (fig_width_mm / 25.4, fig_height_mm / 25.4)

fig, axes = plt.subplots(1, 2, figsize=fig_size)
vmin, vmax = 0.0, 1.0

im1 = axes[0].imshow(u_at_PAP, origin='lower', extent=[0, L, 0, L],
                     vmin=vmin, vmax=vmax)

im2 = axes[1].imshow(u_final_fft, origin='lower', extent=[0, L, 0, L],
                     vmin=vmin, vmax=vmax)

# remove ticks + ensure square
for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# leave room on the right for the colorbar ---
# tweak right=... if you want more/less bar space
fig.subplots_adjust(right=0.86, wspace=0.08)

# finalize layout
fig.canvas.draw()

# position of right plot after adjustment
pos = axes[1].get_position()

# colorbar axis matching plot height
pad = 0.01        # smaller gap, keeps bar more inside
cbar_width = 0.035
cax = fig.add_axes([pos.x1 + pad, pos.y0, cbar_width, pos.height])

cbar = fig.colorbar(im2, cax=cax)

cbar.ax.tick_params(labelsize=30, pad=2)
for t in cbar.ax.get_yticklabels():
    t.set_fontname('Arial')

fig.savefig(
    str(NumSaveDirName) + "/PAP_and_PreMating.png",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.01
)

fig.savefig(
    str(NumSaveDirName) + "/PAP_and_PreMating.eps",
    dpi=300,
    bbox_inches="tight",
    pad_inches=0.01
)





##############################################################################
# Plot Evaluate change and save
##############################################################################


endtime = time.time()
print("time for width:", field_width, ":", endtime - starttime)
timetaken=endtime-starttime
# =====================
# Your resistance calc
# =====================

endstate = u_final_fft * (1 - Phi)
Resistant_Start = np.ones(endstate.shape) * Phi
Resistant_End = Resistant_Start / (endstate + Resistant_Start)

x_int = np.linspace(0, L, nx)
y_int = np.linspace(0, L, ny)
Change = simps(simps(Resistant_End - Resistant_Start, y_int), x_int)


OutputDatafilename = NumSaveDirName + '/datafile.npz'
np.savez(OutputDatafilename,
    #xbound=xbound,
    field_width=field_width,
    PAP=PAP,
    Phi=Phi,
    #C=C,
    dx=dx,
    dt=dt,
    #xlist=xlist,
    #PAPDist=PAPDist,
    #EndDist=EndDist,
    #dR=dR,
    Change=Change,
    #I_PAPSNum=I_PAPSNum,
    #I_ENDSNum=I_ENDSNum,
    #I_dR=I_dR,
    #I_ApproxIntegral=I_ApproxIntegral,
    #I_TOT_PAPSNum=I_TOT_PAPSNum,
    #I_TOT_ENDSNum=I_TOT_ENDSNum,
    #I_TOT_dR=I_TOT_dR,
    #I_TOT_ApproxIntegral=I_TOT_ApproxIntegral,
    #P_xlist = P_xlist,
    #P_PAPSNum=P_PAPSNum,
    #P_ENDSNum=P_ENDSNum,
    #P_dR=P_dR,
    #P_ApproxIntegral=P_ApproxIntegral,
    timetaken=timetaken)


