#!/bin/bash

python Plotting.py -d SaveFiles/D_1000.000_B_0.500_MinN_1.00000_MaxN_2001.00000_NNum_201_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05 -a 0
python Plotting.py -d SaveFiles/D_1000.000_B_0.800_MinN_1.00000_MaxN_2001.00000_NNum_201_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05 -a 0
python Plotting.py -d SaveFiles/D_100.000_B_0.500_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05 -a 0
python Plotting.py -d SaveFiles/D_100.000_B_0.800_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05 -a 0
python Plotting.py -d SaveFiles/D_10.000_B_0.500_MinN_1.00000_MaxN_20.00000_NNum_20_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05 -a 0
python Plotting.py -d SaveFiles/D_10.000_B_0.800_MinN_1.00000_MaxN_20.00000_NNum_20_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05 -a 0

