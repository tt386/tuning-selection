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

width_list = []
height_list = []
dRList = []
#I_dRList = []
#I_TOT_dRList = []
#P_dRList = []

for i in dirlist:
    try:
        with np.load(os.path.join(i,filename)) as data:
            width = data["field_width"]
            height = data["field_height"]
            PAP = data["PAP"]
            Phi = data["Phi"]
            Change = data["Change"]
            #d = data["d"]
            #dx = data["dx"]
            #dt = data["dt"]

            width_list.append(width)
            height_list.append(height)
            dRList.append(Change/(height*width))


    except Exception as e: print(e)

    #L = C/N

    #Collect data
    ##LList.append(L)
    ##dRList.append(Change)
    #I_dRList.append(I_ApproxIntegral)
    #I_TOT_dRList.append(I_TOT_ApproxIntegral)
    #P_dRList.append(P_ApproxIntegral)
"""
# Convert to arrays
width_arr  = np.array(width_list)
height_arr = np.array(height_list)
dR_arr     = np.array(dRList)

# Unique sorted coordinates along each axis
width_vals  = np.unique(width_arr)
height_vals = np.unique(height_arr)

# Map each width/height value to an index in the grid
w_idx = {w: i for i, w in enumerate(width_vals)}
h_idx = {h: j for j, h in enumerate(height_vals)}

# Initialise grid with NaNs
Z = np.full((len(height_vals), len(width_vals)), np.nan)

# Fill the grid with your dR values
for w, h, z in zip(width_arr, height_arr, dR_arr):
    Z[h_idx[h], w_idx[w]] = z

# Build coordinate mesh for plotting
W, H = np.meshgrid(width_vals, height_vals)

# Mask out the part you *don’t* want (e.g. keep only width ≥ height)
mask = W > H          # True = masked (hidden)
Z_masked = np.ma.array(Z, mask=mask)

fig, ax = plt.subplots()

"""
"""
pc = ax.pcolormesh(
    width_vals,
    height_vals,
    Z_masked,
    shading='auto'
)
"""
"""
from matplotlib.colors import LogNorm

Z_masked = np.ma.masked_where(Z_masked <= 0, Z_masked)
"""
"""
pc = ax.pcolormesh(
    width_vals, height_vals, Z_masked,
    norm=LogNorm(), shading='auto'
)
"""
"""
# Assume Z_masked is your masked dR grid
vals = Z_masked[Z_masked > 0]

# Focus the colour range where most values live
vmin = np.percentile(vals, 1)    # or 5
vmax = np.percentile(vals, 99) #4e-5#np.percentile(vals, 99)   # or 95

norm = LogNorm(vmin=vmin, vmax=vmax)

pc = ax.pcolormesh(
    width_vals,
    height_vals,
    Z_masked,
    norm=norm,
    cmap='plasma',      # try 'magma', 'inferno', or 'turbo' too
    shading='auto'
)

cbar = fig.colorbar(pc, ax=ax)
cbar.set_label("dR")


ax.set_xlabel("Width")
ax.set_ylabel("Height")
#fig.colorbar(pc, ax=ax, label="dR")

ax.set_aspect("equal")  # optional, makes triangles look nicer

ax.set_xscale("log")
ax.set_yscale("log")

plt.savefig(str(args.directory) + "/dR.png",bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + "/dR.eps",bbox_inches='tight',dpi=300)



# Remove old colorbar
cbar.remove()

# Apply truncated scale

# Focus the colour range where most values live
vmin = 2e-5#np.percentile(vals, 1)    # or 5
vmax = 3e-5#np.percentile(vals, 99)   # or 95

norm = LogNorm(vmin=vmin, vmax=vmax)

pc.set_norm(norm)

# New colorbar
cbar = fig.colorbar(pc, ax=ax, extend='max')
cbar.set_label("dR (truncated)")

plt.savefig(str(args.directory) + "/dR_Truncated.png",bbox_inches='tight',dpi=300)
plt.savefig(str(args.directory) + "/dR_Truncated.eps",bbox_inches='tight',dpi=300)
"""

# Convert to arrays
width_arr  = np.array(width_list)
height_arr = np.array(height_list)
dR_arr     = np.array(dRList)

# Unique sorted coordinates along each axis
width_vals  = np.unique(width_arr)
height_vals = np.unique(height_arr)

# Map each width/height value to an index in the grid
w_idx = {w: i for i, w in enumerate(width_vals)}
h_idx = {h: j for j, h in enumerate(height_vals)}

# Initialise grid with NaNs
Z = np.full((len(height_vals), len(width_vals)), np.nan)

# Fill the grid with your dR values
for w, h, z in zip(width_arr, height_arr, dR_arr):
    Z[h_idx[h], w_idx[w]] = z

# Build coordinate mesh for plotting
W, H = np.meshgrid(width_vals, height_vals)

# -----------------------------
# New: build alpha transparency mask
# -----------------------------

alpha = np.ones_like(Z, dtype=float)

# Fade the redundant half (edit sign if you want the opposite triangle)
alpha[W > H] = 0.5     # 25% opacity for mirrored half

# -----------------------------
# Log-scale colour normalisation
# -----------------------------

from matplotlib.colors import LogNorm

Z = np.ma.masked_where(Z <= 0, Z)   # LogNorm safety

vals = np.log10(Z)#Z[Z > 0]
#vmin = np.percentile(vals, 1)
#vmax = np.percentile(vals, 99)

print(np.min(vals))

norm = LogNorm(np.min(vals),np.max(vals))#(vmin=vmin, vmax=vmax)

# -----------------------------
# Plot FULL square, with transparency
# -----------------------------

fig, ax = plt.subplots()

pc = ax.pcolormesh(
    width_vals,
    height_vals,
    np.log10(Z),
    #norm=norm,
    cmap='plasma',
    shading='auto',
    alpha=alpha
)

# -----------------------------
# Diagonal divider
# -----------------------------

diag_min = max(width_vals.min(), height_vals.min())
diag_max = min(width_vals.max(), height_vals.max())
x = np.logspace(np.log10(diag_min), np.log10(diag_max), 200)

ax.plot(x, x, 'k--', lw=3)   # white dashed diagonal

# -----------------------------
# Axes + colorbar
# -----------------------------

cbar = fig.colorbar(pc, ax=ax)
#cbar.set_label("dR")

#ax.set_xlabel("Width")
#ax.set_ylabel("Height")
ax.set_aspect("equal")

ax.set_xscale("log")
ax.set_yscale("log")




ax.set_xticks([1,10])
ax.set_xticklabels(
    [r'$10^0$',r'$10^1$'])

ax.set_yticks([1,10])
ax.set_yticklabels(
    ['$10^{0}$',r'$10^{1}$'])


plt.xticks(fontsize=30,fontname = "Arial")
plt.yticks(fontsize=30,fontname = "Arial")

cbar.ax.tick_params(labelsize=30)

for label in cbar.ax.get_yticklabels():
    label.set_fontname("Arial")

plt.savefig(str(args.directory) + "/dR.png", bbox_inches='tight', dpi=300)
plt.savefig(str(args.directory) + "/dR.eps", bbox_inches='tight', dpi=300)


# -----------------------------
# TRUNCATED VERSION
# -----------------------------

cbar.remove()

vmin = -4.7#2e-5
vmax = -4.5#3e-5

#pc.set_norm(LogNorm(vmin=vmin, vmax=vmax))

truncation = np.log10(Z)
truncation = np.ma.masked_invalid(truncation)
truncation = np.clip(truncation, vmin, vmax)

pc = ax.pcolormesh(
    width_vals,
    height_vals,
    truncation,
    #norm=norm,
    vmin=vmin,
    vmax=vmax,
    cmap='plasma',
    shading='auto',
    alpha=alpha
)


fig.canvas.draw()

cbar = fig.colorbar(pc, ax=ax, extend='both')


# Tick positions in real data units
ticks = [vmin,vmax]#[2e-5, 3e-5]

# Apply ticks
cbar.set_ticks(ticks)

# LaTeX-style labels (what is displayed)
cbar.set_ticklabels([r'$10^{-4.7}$', r'$10^{-4.5}$'])


cbar.ax.tick_params(labelsize=30)

for label in cbar.ax.get_yticklabels():
    label.set_fontname("Arial")

#cbar.set_label("dR (truncated)")






plt.savefig(str(args.directory) + "/dR_Truncated.png", bbox_inches='tight', dpi=300)
plt.savefig(str(args.directory) + "/dR_Truncated.eps", bbox_inches='tight', dpi=300)

plt.close()


"""
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
plt.plot(np.log10(LList),np.log10(dRList/LList**2), '-k',linewidth=5)


#1D Data
LList_1D = np.asarray([1.00000000e-02, 1.09749877e-02, 1.20450354e-02, 1.32194115e-02,
       1.45082878e-02, 1.59228279e-02, 1.74752840e-02, 1.91791026e-02,
       2.10490414e-02, 2.31012970e-02, 2.53536449e-02, 2.78255940e-02,
       3.05385551e-02, 3.35160265e-02, 3.67837977e-02, 4.03701726e-02,
       4.43062146e-02, 4.86260158e-02, 5.33669923e-02, 5.85702082e-02,
       6.42807312e-02, 7.05480231e-02, 7.74263683e-02, 8.49753436e-02,
       9.32603347e-02, 1.02353102e-01, 1.12332403e-01, 1.23284674e-01,
       1.35304777e-01, 1.48496826e-01, 1.62975083e-01, 1.78864953e-01,
       1.96304065e-01, 2.15443469e-01, 2.36448941e-01, 2.59502421e-01,
       2.84803587e-01, 3.12571585e-01, 3.43046929e-01, 3.76493581e-01,
       4.13201240e-01, 4.53487851e-01, 4.97702356e-01, 5.46227722e-01,
       5.99484250e-01, 6.57933225e-01, 7.22080902e-01, 7.92482898e-01,
       8.69749003e-01, 9.54548457e-01, 1.04761575e+00, 1.14975700e+00,
       1.26185688e+00, 1.38488637e+00, 1.51991108e+00, 1.66810054e+00,
       1.83073828e+00, 2.00923300e+00, 2.20513074e+00, 2.42012826e+00,
       2.65608778e+00, 2.91505306e+00, 3.19926714e+00, 3.51119173e+00,
       3.85352859e+00, 4.22924287e+00, 4.64158883e+00, 5.09413801e+00,
       5.59081018e+00, 6.13590727e+00, 6.73415066e+00, 7.39072203e+00,
       8.11130831e+00, 8.90215085e+00, 9.77009957e+00, 1.07226722e+01,
       1.17681195e+01, 1.29154967e+01, 1.41747416e+01, 1.55567614e+01,
       1.70735265e+01, 1.87381742e+01, 2.05651231e+01, 2.25701972e+01,
       2.47707636e+01, 2.71858824e+01, 2.98364724e+01, 3.27454916e+01,
       3.59381366e+01, 3.94420606e+01, 4.32876128e+01, 4.75081016e+01,
       5.21400829e+01, 5.72236766e+01, 6.28029144e+01, 6.89261210e+01,
       7.56463328e+01, 8.30217568e+01, 9.11162756e+01, 1.00000000e+02])

dRList_1D = np.asarray([8.51868199e-06, 8.53221486e-06, 8.54707474e-06, 8.56339112e-06,
       8.58130996e-06, 8.60099229e-06, 8.62260473e-06, 8.64634715e-06,
       8.67242724e-06, 8.70107588e-06, 8.73255003e-06, 8.76713615e-06,
       8.80514054e-06, 8.84691044e-06, 8.89282475e-06, 8.94329926e-06,
       8.99879942e-06, 9.05983496e-06, 9.12697244e-06, 9.20083768e-06,
       9.28212559e-06, 9.37160403e-06, 9.47012929e-06, 9.57865326e-06,
       9.69822485e-06, 9.83002823e-06, 9.97537593e-06, 1.01357356e-05,
       1.03127499e-05, 1.05082615e-05, 1.07243450e-05, 1.09633241e-05,
       1.12278349e-05, 1.15208566e-05, 1.18457683e-05, 1.22064165e-05,
       1.26071950e-05, 1.30531336e-05, 1.35500295e-05, 1.41045605e-05,
       1.47244965e-05, 1.54188759e-05, 1.61983027e-05, 1.70752634e-05,
       1.80645588e-05, 1.91838530e-05, 2.04543470e-05, 2.19017036e-05,
       2.35572289e-05, 2.54594147e-05, 2.76560560e-05, 3.02070681e-05,
       3.31883728e-05, 3.66972934e-05, 4.08601675e-05, 4.58432567e-05,
       5.18686746e-05, 5.92381109e-05, 6.83688766e-05, 7.98500911e-05,
       9.45325533e-05, 1.13676724e-04, 1.39204568e-04, 1.74144149e-04,
       2.23446856e-04, 2.95561324e-04, 4.05625241e-04, 5.82333933e-04,
       8.83747726e-04, 1.43658987e-03, 2.54296911e-03, 5.00115401e-03,
       1.11869822e-02, 2.91757233e-02, 9.00708085e-02, 3.14270665e-01,
       9.73602601e-01, 2.05922386e+00, 3.31628471e+00, 4.69827016e+00,
       6.21501983e+00, 7.87965116e+00, 9.70658182e+00, 1.17116358e+01,
       1.39121801e+01, 1.63272750e+01, 1.89778381e+01, 2.18868283e+01,
       2.50794416e+01, 2.85833307e+01, 3.24288440e+01, 3.66492910e+01,
       4.12812259e+01, 4.63647685e+01, 5.19439508e+01, 5.80670962e+01,
       6.47872404e+01, 7.21625908e+01, 8.02570286e+01, 8.91406646e+01])

plt.plot(np.log10(LList_1D[LList_1D>0.1]),np.log10(dRList_1D[LList_1D>0.1]/LList_1D[LList_1D>0.1]), '-k',alpha=0.5,linewidth=5)

plt.scatter(np.log10(0.1),-4.036291805290577,marker = 'o',color='red',s=100,zorder=10)
plt.scatter(np.log10(1),-4.593865661116883,marker = 's',color='red',s=100,zorder=10)
plt.scatter(np.log10(10),-1.9406449928450782,marker = '*',color='red',s=150,zorder=10)


#Formatting
plt.xticks([-1,0,1,2])

ax.set_xticks([-1,0,1,2])
ax.set_xticklabels(
    [r'$10^{-1}$',r'$10^0$',r'$10^1$',r'$10^2$'])

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
"""
