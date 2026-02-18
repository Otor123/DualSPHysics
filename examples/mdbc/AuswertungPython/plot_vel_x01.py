#!/usr/bin/env python3
"""
Plot of DualSPHysics _PointsVelocity_Vel.z.csv:
Velocity in z-Richtung an Position x = 0.1 über die Zeit.
"""

import sys
import math
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==== Einstellungen ====
CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001/measuretool/_PointsVelocity_Vel.z.csv"   # Dateiname anpassen, falls nötig
#CSV_FILE= "/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s/measuretool/_PointsVelocity_Vel.z.csv"
#CSV_FILE="/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2/measuretool/_PointsVelocity_Vel.z.csv"
#CSV_FILE = "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv"


# ==== Einstellungen ====
CSV_FILES = [
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
     "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.004_CPU/measuretool/_PointsVelocity_Vel.z.csv",
     "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_out_dp_0.002_CPU/measuretool/_PointsVelocity_Vel.z.csv",
     "/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv",
     "/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",
     #"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.004_TimeMax_4/measuretool/_PointsVelocity_Vel.z.csv",
     "/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_20_GPU/measuretool/_PointsVelocity_Vel.z.csv",
     "/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
]

#3D Pipe big - changed db
CSV_FILES = [
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_20_GPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
"/nishome/PaulS/Programms/DualSPHysicsValidation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_mssrv10_2_3_2_dp_0_002/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_out_dp_0.002_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_1_5s_dp_0.002_rtx3080/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsValidation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_mDBC_out_dp_0.002_msspc23/measuretool/_PointsVelocity_Vel.z.csv",
]


#3D Pipe big - GPU Compare differente Times
CSV_FILES = [
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
]

#3D Pipe big - GPU Compare differente Times + CPU
CSV_FILES = [
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.004_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsValidation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_mDBC_out_dp_0.001_msspc36/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsValidation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_msssrv10_2_3_2_dp_0.001/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsValidation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_mssrv10_2_3_2_dp_0_002/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsValidation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_mDBC_out_dp_0.002_msspc23/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_8s_dp_0.004/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_dp_0.0005_T_8s/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_dp_0.04_V2/measuretool/_PointsVelocity_Vel.z.csv",
]
#
##3D Pipe big - changed db - GPU
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_dp_0.0005_T_8s/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_8s_dp_0.004/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv",
#
#]
#
##3D Pipe big - changed db - GPU
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_dp_0.0005_T_8s/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_1_5s_dp_0.002_rtx3080/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/FirstResultsSimulation/Posieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
#

##3D Pipe big - changed db - GPU
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",]


##3D Pipe big - boundary
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#]

##3D Pipe big - coefhsound
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_5/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_10/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_20_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_30/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_40/measuretool/_PointsVelocity_Vel.z.csv",
#]

##3D Pipe big - denistyDT
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_0/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_3/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
##3D Pipe big - Kernel
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_kernel_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_kernel_2/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
##3D Pipe big - Penetration
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_penetration_0/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_penetration_1/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
###3D Pipe big - Shifting
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_0/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_3/measuretool/_PointsVelocity_Vel.z.csv",
#]

##3D Pipe big - slipMode
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_slipMode_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_slipMode_2/measuretool/_PointsVelocity_Vel.z.csv",
#]

##3D Pipe big - viscoBoundFacor
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_viscoBoundFactor_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_viscoBoundFactor_1.5/measuretool/_PointsVelocity_Vel.z.csv",
#]

##3D Pipe big - viscoValue
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_01/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_001/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_0001/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_00001/measuretool/_PointsVelocity_Vel.z.csv",
#]

#CPU vs GPU

CSV_FILES = [
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/3D/Posiuelle_mDBC_out_0.003_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/3D/Posiuelle_mDBC_out_0.002_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/3D/Posiuelle_mDBC_out_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.003_GPU_H_Dp=2.07846_KernelH_0.006235/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.002_GPU_H_Dp=2.07846_KernelH_0.004157/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.001_GPUH_Dp=2.07846_KernelH_0.002078/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_2_0.csv",
]
#
##2D - CPU own vs git & vs GPU - kein Unterschied
CSV_FILES = [
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/2D/CasePoiseuille_NS_LR_dp_0_02_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/2D/CasePoiseuille_NS_LR_dp_0_04_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/2D/CasePoiseuille_NS_LR_dp_0_02_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/2D/CasePoiseuille_NS_LR_dp_0_04_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv",    
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/2D/CasePoiseuille_NS_LR_dp_0_02_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/2D/CasePoiseuille_NS_LR_dp_0_04_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv",
]

#3D - CPU own vs git - kein Unterschied

CSV_FILES = [
    "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.002/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.003/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/3D/Posiuelle_mDBC_out_0.002_CPU/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/3D/Posiuelle_mDBC_out_0.003_CPU/measuretool/_PointsVelocity_Vel.z.csv",
]

#3D - CPU own vs GBU own - UnterschiedGPUundCPU
CSV_FILES = [
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.002_GPU_H_Dp=2.07846_KernelH_0.004157/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.003_GPU_H_Dp=2.07846_KernelH_0.006235/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.002/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.003/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_2_0.csv",
]

####3D Zentral - GPU vs CPU
###
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_CPU_dp_0.0075/measuretool/_PointsVelocity_Vel.z.csv",
#    "/run/user/1257/gvfs/sftp:host=tinygpu/home/hpc/iwsp/iwsp110h/Programms/DualSPHysicsImplementationV2/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0075/measuretool/_PointsVelocity_Vel.z.csv", 
#    "/run/user/1257/gvfs/sftp:host=tinygpu/home/hpc/iwsp/iwsp110h/Programms/DualSPHysicsImplementationV2/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.00375/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_CPU_dp0.00375/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
###Test
##
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_grob/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/ZentrischesBeispiel/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#]
#

CSV_FILES = [
        "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",

]

CSV_FILES = [
   "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesRe</_PointsVelocity_Vel.z.csv",
    #"/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe</AnalyticalTransientProfile_t_30sekundeFinalRe<<_SmallerMessDPRes.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe</AnalyticalTransientProfile_t_All.csv"
]

CSV_FILES = [
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesDpsmallMeasurementRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",
]

#
#für X position
DESIRED_X = 0.1
#für Z position
#DESIRED_X = 0.0
# 0 PosX, 2 PosZ
rowindex = 0
TOL = 1e-6


def find_x_column(df, desired_x, tol=1e-6):
    """
    Sucht in der ersten Zeile (PosX [m]:) die Spalte, deren Wert ~ desired_x ist.
    Gibt den Spaltenindex (Spaltennummer) zurück oder None.
    """
    # Erste Zeile enthält oft: [nan/leer, 'PosX [m]:', '0.13', '0.125', ...]
    x_row = df.iloc[rowindex, :]

    # Konvertiere alles zu numeric, nicht-numeric -> NaN
    x_vals = pd.to_numeric(x_row, errors="coerce")

    for col_idx, val in x_vals.items():
        if not math.isnan(val) and abs(val - desired_x) <= tol:
            return col_idx

    return None


def load_time_and_vel(csv_file, desired_x, tol):
    """
    Lädt CSV (DualSPHysics Format) und gibt time, vel_z zurück.
    """
    csv_file = str(csv_file)
    try:
        df = pd.read_csv(csv_file, sep=";", header=None, engine="python")
    except FileNotFoundError:
        raise FileNotFoundError(f"Datei nicht gefunden: {csv_file}")

    col_idx = find_x_column(df, desired_x, tol)
    if col_idx is None:
        x_row = pd.to_numeric(df.iloc[rowindex, :], errors="coerce").dropna().tolist()
        raise ValueError(
            f"Keine Spalte mit x ≈ {desired_x} (tol={tol}) in {csv_file} gefunden.\n"
            f"Beispiel gefundener x-Werte: {x_row[:20]}"
        )

    # Daten beginnen ab Zeile 4 (wie in deinem Script)
    time = pd.to_numeric(df.iloc[4:, 1], errors="coerce")
    vel_z = pd.to_numeric(df.iloc[4:, col_idx], errors="coerce")

    mask = (~time.isna()) & (~vel_z.isna())
    return time[mask], vel_z[mask]


def main():
    if not CSV_FILES:
        print("CSV_FILES ist leer.")
        sys.exit(1)

    plt.figure()

    for csv in CSV_FILES:
        try:
            time, vel = load_time_and_vel(csv, DESIRED_X, TOL)
        except Exception as e:
            print(f"[WARN] Überspringe {csv}: {e}")
            continue

        label = Path(csv).parent.parent.name  # z.B. Ordnername über measuretool
        # Alternative: label = Path(csv).stem
        plt.plot(time, vel, label=label)

    plt.xlabel("Time [s]")
    plt.ylabel(f"Vel.z [m/s] at x = {DESIRED_X} m")
    plt.title(f"Velocity over time at x = {DESIRED_X}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()