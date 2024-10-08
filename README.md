
# Code for "Tuning Selection pressure..."

## Overview

[Publication](#publication)

[Brief description of diffusion](#brief-description-of-diffusion)

[Structure of simulation code](#structure-of-simulation-code)

[Directory structure and exectuing code](#directory-structure-and-executing-code)

[Reproducing figures](#reproducing-figures)


## Publication

Manuscript published in XXX in 2023 by Thomas Tunstall, Philip Madgwick, Ricardo Kanitz, and Wolfram Möbius. The corresponding preprint can be found on arXiv XXX.

We have included all data files and results pertinent to the manuscript (except those larger than 100MB).

## Brief description of diffusion

The migration of susceptible pests is modelled by diffusion. In the thermodynamic limit of a large number of pests, we can approximate the distribution of pests as a continuous distribution of pests, $u_{S}(X,T)$ subject to the diffusion kernel.

The Phases of the simulation:
* $T=0$: The initial conditions: A flat distribution of Susceptible pests with frequency  $u_{S}(X,T)=\Phi$ outside of the Selection regions, and $u_{S}(X,T)=0$ within the Selection region. This is because the Selection regions are intially active, so any Susceptible pests within the Selection region would die.

* $T=P$: While the Selection region is active, any Susceptible pest that would enter the Selection region would be removed from the system. This corresponds to the boundary of the Selection regions ($\partial_\text{Selection}$) being Dirichlet boundary conditions ($u_S(X=\partial_\text{Selection},T)=0$). The distribution of Susceptible pests at $T=P$ is known exactly and defined as $u_S'(X)$: see the main publication.

* $T=1$: For $T>P$, the Selection region is inactive, so Susceptible pests are able to migrate into these regions. This corresponds to convolving the distribution at the end of the Selection period, $u_S'(X)$, by the heat kernel, $K(X)$ for the rest of the time in the simulation (for a time $1-P$): $\frac{1}{\sqrt{4\pi(1-P)}}e^{-\frac{x^2}{4(1-P)} }$.  
The procedure of convolution is achieved quickly with fast fourier transforms and inverse fast fourier transforms. The pre-breeding distribution of Susceptible pests is equal to $u_S''(X) = u_S'(X)*K(X) \equiv \mathcal{F}^{-1}[\mathcal{F}(u_S'(X))\times \mathcal{F}(K(X))]$. This is evaluated quickly with the `numpy.fft` and `numpy.ifft` functions.

## Structure of simulation code

Similar to the description of the diffusion precedure above, we only simulate the Susceptible pest distributions at $T=P$ and $T=1$, using analytical results and convolutions methods, respectively. Following this, breeding is modelled, follwoed by the calculation of the change in Resistant pest number. Below is a snapshot of the code which captures all of this in the case of `Simulations/Single/Global_Minimum`:

```python
#########################################
###Main Process##########################
#########################################

xlist, PAPDist = Core.PAPDist_Single(xbound,L,dx,Phi,PAP)

Kernel = Core.Kernel(PAP,xlist)

EndDist = Core.EndDist_Single(PAPDist,Kernel,xlist,L,dx)

ApproxIntegral = Core.dR(Phi,EndDist,xlist)
```

* The first line produces two 1D numpy arrays: an `xlist` which is simply the x-axis along which diffusion acts on the population distribution, and a `PAPDist`, the distribution of Susceptible pests at $T=P$.

* The second line defines the diffusion dispersal `Kernel` for use later.

* The third line convolves the `PAPDist` and `Kernel`. Note that this uses the `numpy.fft` and `numpy.ifft` in such a way that the convolution is periodic: due to this, the system initially produces is much longer than necessary so the edge effects should have minimal impact on the bulk of the system.

* The fourth line produces a float which is the measure by which the Resistant population has increased: Following breeding, the differences between the final and initial Resistant distributions is integrated over all space.

## Directory structure and exectuing code

Below is a tree respresenting the structure of directories.

```
.
├── RawFigs
└── Simulations
    ├── Constrained_Finite
    ├── Constrained_Infinite
    ├── CoreFunctions
    ├── Periodic
    │   ├── Global_Minimum
    │   └── Vary_w
    └── Single
        ├── Global_Minimum
        ├── RemovingDispersalEvents
        ├── SingleSystemEvolution
        └── UpperBound
            ├── Vary_PAP
            └── Vary_Phi

```

### Directory `RawFigs`

This stores all the figures used in the publication. In order to populate it, execute:

```
$ bash FigureCopying.sh RawFigs/
```

### Simulations

Here are the directories which house the code used to generate figures for the publication.

#### Single

The case of a single Selction region. There are two points of interest: the global minimum itself, and the upper bound (the region of highest curvature which can be predicted analytically). 

##### Global Minimum 

For $P=0.1, \Phi=10^{-5}$ we vary the length of the Selection region and calculate the change in Resistant pests over a domain so large that the periodic effects of the circular convolution have negligible effect. The result is a detailed global minimum of change in Resistance number per Selection region size with changing Selection region size.

![Single Global Minimum](./RawFigs/Fig1b_SingleGlobalMinimum.png)


##### RemovingDispersalEvents

For $P=0.1, \Phi=10^{-5}$ we run the same simulation as above, except with the additional option of restricting migration to only occur during the selection phase, the post-selection phase, both phases, or neither phase. Running once for each possibility with the same 

![Different Dispersal TImes](./RawFigs/Fig2d_DifferentDispersals.png)


##### SingleSystemEvolution

For $P=0.1, \Phi=10^{-5}$ we run an isolated selection region case for a given $L$, for the sake of visualising how the distribution of each subpopulation changes over a generation 

![Initial Distribution](./RawFigs/Fig1a_1Init.png)

##### UpperBound

We once again vary the size of the Selection region size $L$, but for different $P$ or $\Phi$ values in `Vary_PAP` and `Vary_Phi`, respectively. This is in order to measure how the region of highest curvature changes with these values, to validate the analytical theory.

![Single UpperBoundPAP](./RawFigs/Fig2cii_UpperBoundWithPAP.png)

![Single UpperBoundPhi](./RawFigs/Fig2ci_UpperBoundWithPhi.png)

#### Periodic

The case of an infinite sequence of Selection and Refuge regions, effectively meaning there is a comparatively small region of Refuge and Selection regions with periodic boundary conditions. The width of the periodic sub-unit is $K$ and the proportion of the region which is Refuge is $\omega$.

##### Global Minimum

For $P=0.1, \Phi=10^{-5}, \omega=0.1$ we vary the length of the periodic sub-unit, $K$, and calculate the change in Resistant pests over a domain so large that the periodic effects of the circular convolution have negligible effect. The result is a detailed global minimum of change in Resistance number per periodic sub-region size with changing periodic sub-region size.

##### Vary_w

We again vary the periodic sub-region length $K$, but for different $\omega$ values in order to measure how the region of minimum gradient changes with $\omega$ to validate the analytical theory for a lower bound, and how the region of maximum curvature changes with $\omega$ to validate the analytical theory for the upper bound.

![Periodic Allw](./RawFigs/Fig3a_All_Alpha.png)

![Periodic Bounds](./RawFigs/Fig3c_UpperBound_LowerBound_Minimum.png)



#### Constrained Infinite

Consider a total amount of Selection region, of total width $C$. This is split up into $N$ regions of length $L=C/N$, separated by regions of refuge of width $\delta$. For each N value, we calculate the change in Resistant pest number. At the same time, we approximate the domain with:

* $N$ 'single' regions of length $L$. This is valid when the Selection regions are far away enough to be effectively independent.

* $N$ 'periodic' sub-units of width $K= L+\delta$, with $\omega = \delta/K$.

* $1$ 'single' region of length $C+(N-1)\delta$: this is accurate when the Selection regions are so close together that the contribution of the Refuge regions between them are negligible.

![Constrained Infinite](./RawFigs/Fig5_C10_d1.png)

#### Constrained Finite

Consider a total amount of space where it is possible for Selection region to be placed, of width $D$. The proportion of the region which can be Selection Region is defined by $\beta$. The Selection regions are subdivided into $N$ discrete regions of width $L=D\beta/N$, separated by Refuge regions of width $\delta = D(1-\beta)/(N-1)$ . For each N value, we calculate the change in Resistant pest number. At the same time, we approximate the domain with:

* $N$ 'single' regions of length $L$. This is valid when the Selection regions are far away enough to be effectively independent.

* $N$ 'periodic' sub-units of width $K= L+\delta$, with $\omega = \delta/K$.

* $1$ 'single' region of length $D$: this is accurate when the Selection regions are so close together that the contribution of the Refuge regions between them are negligible.

![Constrained Finite](./RawFigs/Fig6_D100_B0.5.png)

## Reproducing figures

To recreate the data, navigate to the `Host Directory` and execute the corresponding commands.

| Figure(s) | Host Directory | Commands for simulation and creating figure |
| -------------| ------------- | ------------- |
| [1a_i](./RawFigs/Fig1a_1Init.png), [1a_ii](./RawFigs/Fig1a_2PAP.png), [1a_iii](./RawFigs/Fig1a_3End.png), [1a_iv](./RawFigs/Fig1a_4PostBreed.png), [2b_i](./RawFigs/Fig2b_L10.png),[2b_ii](./RawFigs/Fig2b_L20.png),[2b_iii](./RawFigs/Fig2b_L40.png) | `Simulations/Single/SingleSystemEvolution` |`cp SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `python Plotting.py -d SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/` |
| [1b](./RawFigs/Fig1b_SingleGlobalMinimum.png), [2a](./RawFigs/Fig2a_SingleGlobalMinimum.png) |`Simulations/Single/Global_Minimum` | `cp SaveFiles/MinL_0.01000_MaxL_100.00000_LNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `python Plotting.py -d SaveFiles/MinL_0.01000_MaxL_100.00000_LNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05` |
| [2ci](./RawFigs/Fig2ci_UpperBoundWithPhi.png) |`Simulations/Single/UpperBound/Vary_Phi` | `cp SaveFiles/MinL_0.10000_MaxL_1000.00000_LNum_100_xbound_1000_minPhi_-12_maxPhi_-1_Phinum_12_PAP_1.0E-01/Params.py .` <br> `python PhiRunFile.py` <br> `python MultiPlotting.py -d SaveFiles/MinL_0.10000_MaxL_1000.00000_LNum_100_xbound_1000_minPhi_-12_maxPhi_-1_Phinum_12_PAP_1.0E-01` |
| [2cii](./RawFigs/Fig2cii_UpperBoundWithPAP.png) |`Simulations/Single/UpperBound/Vary_PAP` | `cp SaveFiles/MinL_0.10000_MaxL_1000.00000_LNum_100_xbound_1000_minPAP_0.100_maxPAP_0.900_PAPnum_9_Phi_1.0E-05/Params.py .` <br> `python PAPRunFile.py` <br> `python MultiPlotting.py -d SaveFiles/MinL_0.10000_MaxL_1000.00000_LNum_100_xbound_1000_minPAP_0.100_maxPAP_0.900_PAPnum_9_Phi_1.0E-05` |
| [2d](./RawFigs/Fig2d_DifferentDispersals.png) |`Simulations/Single/RemovingDispersalEvents` | `cp SaveFiles/MinL_0.000001_MaxL_100.00000_LNum_100_xbound_10_dx_1.0E-07_PAP_1.0E-01_Phi_1.0E-05_AllMigrations/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/MinL_0.000001_MaxL_100.00000_LNum_100_xbound_10_dx_1.0E-07_PAP_1.0E-01_Phi_1.0E-05_NoMigrations/Params.py .` <br> `python RunFile.py` <br>`cp SaveFiles/MinL_0.000001_MaxL_100.00000_LNum_100_xbound_10_dx_1.0E-07_PAP_1.0E-01_Phi_1.0E-05_OnlyPostSelectionMigration/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/MinL_0.000001_MaxL_100.00000_LNum_100_xbound_10_dx_1.0E-07_PAP_1.0E-01_Phi_1.0E-05_OnlySelectionMigration/Params.py .` <br> `python RunFile.py` <br> `python MultiPlotting.py -d SaveFiles` |
| [3a](./RawFigs/Fig3a_All_Alpha.png), [3c](./RawFigs/Fig3c_UpperBound_LowerBound_Minimum.png) | `Simulations/Periodic/Vary_w` | `cp SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_minw_0.100_maxw_0.900_wnum_9_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python wRunFile.py` <br> `python MultiPlotting.py -d SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_minw_0.100_maxw_0.900_wnum_9_PAP_1.0E-01_Phi_1.0E-05` |
| [3b](./RawFigs/Fig3b_PeriodicGlobalMinimum.png) |`Simulations/Periodic/GlobalMinimum` | `cp SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_w_0.100_dx_1.0E-04_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `python Plotting.py -d SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_w_0.100_dx_1.0E-04_PAP_1.0E-01_Phi_1.0E-05` |
| 5 |`Simulations/Constrained_Infinite` | `cp SaveFiles/C_100.000_d_0.100_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_100.000_d_10.000_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_5.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_100.000_d_1.000_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_5.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_10.000_d_0.100_MinN_1.00000_MaxN_100.00000_NNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_10.000_d_10.000_MinN_1.00000_MaxN_100.00000_NNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_10.000_d_1.000_MinN_1.00000_MaxN_100.00000_NNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_1.000_d_0.100_MinN_1.00000_MaxN_1000.00000_NNum_42_xbound_100_dx_1.0E-05_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_1.000_d_10.000_MinN_1.00000_MaxN_1000.00000_NNum_42_xbound_100_dx_1.0E-05_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/C_1.000_d_1.000_MinN_1.00000_MaxN_1000.00000_NNum_42_xbound_100_dx_1.0E-05_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `bash BashPlotting.sh` |
| 6 |`Simulations/Constrained_Finite` | `cp SaveFiles/D_1000.000_B_0.500_MinN_1.00000_MaxN_2001.00000_NNum_201_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/D_1000.000_B_0.800_MinN_1.00000_MaxN_2001.00000_NNum_201_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/D_100.000_B_0.500_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/D_100.000_B_0.800_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/D_10.000_B_0.500_MinN_1.00000_MaxN_20.00000_NNum_20_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `cp SaveFiles/D_10.000_B_0.800_MinN_1.00000_MaxN_20.00000_NNum_20_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/Params.py .` <br> `python RunFile.py` <br> `bash BashPlotting.sh` |
