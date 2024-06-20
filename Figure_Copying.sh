#!/bin/bash

path_dst=$1

Sources=(
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_10.00000/1_Init.png
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_10.00000/2_PAP.png
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_10.00000/3_End.png
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_10.00000/4_PostBreed.png
	Simulations/Single/Global_Minimum/SaveFiles/MinL_0.01000_MaxL_100.00000_LNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png

	Simulations/Single/Global_Minimum/SaveFiles/MinL_0.01000_MaxL_100.00000_LNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR_Stretch.png
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_40.00000/5_PostBreedROnly.png
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_20.00000/5_PostBreedROnly.png
	Simulations/Single/SingleSystemEvolution/SaveFiles/MinL_10.00000_MaxL_40.00000_LNum_3_xbound_1000_dx_1.0E-01_PAP_1.0E-01_Phi_1.0E-05/L_10.00000/5_PostBreedROnly.png
	Simulations/Single/UpperBound/Vary_Phi/SaveFiles/MinL_0.10000_MaxL_1000.00000_LNum_100_xbound_1000_minPhi_-12_maxPhi_-1_Phinum_12_PAP_1.0E-01/LU.png
	Simulations/Single/UpperBound/Vary_PAP/SaveFiles/MinL_0.10000_MaxL_1000.00000_LNum_100_xbound_1000_minPAP_0.100_maxPAP_0.900_PAPnum_9_Phi_1.0E-05/LU.png

	Simulations/Periodic/Global_Minimum/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_w_0.100_dx_1.0E-04_PAP_1.0E-01_Phi_1.0E-05/K_2.59502/PAP_And_End.png
	Simulations/Periodic/Global_Minimum/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_w_0.100_dx_1.0E-04_PAP_1.0E-01_Phi_1.0E-05/K_97.70100/PAP_And_End.png
	Simulations/Periodic/Global_Minimum/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_w_0.100_dx_1.0E-04_PAP_1.0E-01_Phi_1.0E-05/dR_Detail.png
	Simulations/Periodic/Vary_w/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_minw_0.100_maxw_0.900_wnum_9_PAP_1.0E-01_Phi_1.0E-05/LL.png
	Simulations/Periodic/Vary_w/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_minw_0.100_maxw_0.900_wnum_9_PAP_1.0E-01_Phi_1.0E-05/LU.png
	Simulations/Periodic/Vary_w/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_minw_0.100_maxw_0.900_wnum_9_PAP_1.0E-01_Phi_1.0E-05/Both.png
	Simulations/Periodic/Vary_w/SaveFiles/MinK_0.10000_MaxK_1000.00000_KNum_100_minw_0.100_maxw_0.900_wnum_9_PAP_1.0E-01_Phi_1.0E-05/AllMinPlots.png

	Simulations/Constrained_Infinite/SaveFiles/C_100.000_d_0.100_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_100.000_d_10.000_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_5.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_100.000_d_1.000_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_5.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_10.000_d_0.100_MinN_1.00000_MaxN_100.00000_NNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_10.000_d_10.000_MinN_1.00000_MaxN_100.00000_NNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_10.000_d_1.000_MinN_1.00000_MaxN_100.00000_NNum_100_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_1.000_d_0.100_MinN_1.00000_MaxN_1000.00000_NNum_42_xbound_100_dx_1.0E-05_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_1.000_d_10.000_MinN_1.00000_MaxN_1000.00000_NNum_42_xbound_100_dx_1.0E-05_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Infinite/SaveFiles/C_1.000_d_1.000_MinN_1.00000_MaxN_1000.00000_NNum_42_xbound_100_dx_1.0E-05_PAP_1.0E-01_Phi_1.0E-05/dR.png

	Simulations/Constrained_Finite/SaveFiles/D_10.000_B_0.500_MinN_1.00000_MaxN_20.00000_NNum_20_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Finite/SaveFiles/D_10.000_B_0.800_MinN_1.00000_MaxN_20.00000_NNum_20_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Finite/SaveFiles/D_100.000_B_0.500_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Finite/SaveFiles/D_100.000_B_0.800_MinN_1.00000_MaxN_200.00000_NNum_200_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Finite/SaveFiles/D_1000.000_B_0.500_MinN_1.00000_MaxN_2001.00000_NNum_201_xbound_1000_dx_2.5E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png
	Simulations/Constrained_Finite/SaveFiles/D_1000.000_B_0.800_MinN_1.00000_MaxN_2001.00000_NNum_201_xbound_1000_dx_1.0E-03_PAP_1.0E-01_Phi_1.0E-05/dR.png

	Simulations/Single/Global_Minimum/SaveFiles/dR.png

	Simulations/Single/RemovingDispersalEvents/SaveFiles/dR.png

	)

Names=(
	Fig1a_1Init.png
	Fig1a_2PAP.png
	Fig1a_3End.png
	Fig1a_4PostBreed.png
	Fig1b_SingleGlobalMinimum.png

	Fig2a_SingleGlobalMinimum.png
	Fig2b_L40.png
	Fig2b_L20.png
	Fig2b_L10.png
	Fig2ci_UpperBoundWithPhi.png
	Fig2cii_UpperBoundWithPAP.png

	Fig3ai_Smallk.png
	Fig3aii_Largek.png
	Fig3a_PeriodicGlobalMinimum.png
	Fig3bi_LowerBoundWithw.png
	Fig3bii_UpperBoundWithw.png
	Fig3b_UpperBound_LowerBound_Minimum.png
	Supplement_All_alpha.png

	Fig5_C100_d0.1.png
	Fig5_C100_d10.png
	Fig5_C100_d1.png
	Fig5_C10_d0.1.png
        Fig5_C10_d10.png
        Fig5_C10_d1.png
	Fig5_C1_d0.1.png
        Fig5_C1_d10.png
        Fig5_C1_d1.png

	Fig6_D10_B0.5.png
	Fig6_D10_B0.8.png
	Fig6_D100_B0.5.png
        Fig6_D100_B0.8.png
	Fig6_D1000_B0.5.png
        Fig6_D1000_B0.8.png

	SuppFig_p_0_0.1_1.png
	SuppFig_DifferentMigrations.png
	)

for i in "${!Sources[@]}"; do
    basename "${Sources[$i]}"
    f="${Names[$i]}"
    echo $filename
    file_dst="${path_dst}/${f}"

    echo $file_dst

    cp "${Sources[$i]}" "$file_dst"
    echo cp "${Sources[$i]}" "$file_dst"
done
