import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------------
# Liste an CSV-Dateien
# --------------------------------------------------------
#3D Pipe big - changed coefh
CSV_FILES = [
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out_dp_0.001_activated_aoutofill_and_advanced_Draw_mode_coefh_1/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out_dp_0.001_activated_aoutofill_and_advanced_Draw_mode_coefh_0.95/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out_dp_0.001_activated_aoutofill_and_advanced_Draw_mode_coefh_1.1/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out_dp_0.001_activated_aoutofill_and_advanced_Draw_mode_coefh_1.4/measuretool/_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Analytical/_PointsVelocity_Vel.z_clean.csv",
    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_FreeCadPosieulle_X/Poisuelle/Poisuelle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",

]

#3D Pipe big - changed db
CSV_FILES = [
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.008_CPU/measuretool/_PointsVelocity_Vel.z.csv",    
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.004_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_out_dp_0.002/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_0_25.csv",
]

##3D Pipe big - changed db
#CSV_FILES = [
##"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_out_dp_0.002/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
CSV_FILES = [
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe<</AnalyticalTransientProfile_t_All.csv",
]
CSV_FILES = [
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesDpsmallMeasurementRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",
]

CSV_FILES = [
  #  "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesDpsmallMeasurementRe<</_PointsVelocity_Vel.z.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesDpsmallMeasurementRe<</AnalyticalTransientProfile_t_All.csv",
    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/setDRWMode/smallPipe_FreeCAD/_PointsVelocity_Vel.z.csv"
]

#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
#
#]
#
###3D Pipe big - changed db
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]
#
###3D Pipe big - changed db SCHEUERLEIN
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_0_25.csv",
#]
#
#####3D Pipe Small
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Posieulle_mDBC_out_dp_0.00025/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Posieulle_mDBC_out_dp_0.000125/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Posieulle_mDBC_out_dp_0.0000625/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
##"/nishome/PaulS/Downloads/_PointsVelocity_Vel.z.csv",
#]
#
####3D Pipe Small compare GPU CPU
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_outdp=0.000125_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Posieulle_mDBC_out_dp_0.000125/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Posieulle_mDBC_out_dp_0.00025/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Poiseulle_mDBC_outdp=0.00025_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#]

##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_viscoBoundFactor_1/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_viscoBoundFactor_1.5/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]


##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_slipMode_1/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_slipMode_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]

##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_penetration_0/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_penetration_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]

##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_kernel_1/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_kernel_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]

##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_0/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_densityDT_3/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]

##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_5/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_10/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_20/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_30/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_coefhsound_40/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]
#
###3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_1/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]
#
##3D Pipe big - ParameterStudy
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_00001/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_0001/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_001/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_01/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_visco_value_0_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#]
#
###3D Pipe big - ParameterStudy
##CSV_FILES = [
##"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_3/measuretool/_PointsVelocity_Vel.z.csv",    
##"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_2/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_1/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_0/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
##]
##
#
#
######3D Pipe Small compare GPU CPU
##CSV_FILES = [
##"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_AnalyticalT.csv",
##"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
##"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_5_FreeCadSmallEample/Posieulle/Posieulle_mDBC_out_dp_0.00025/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Poiseulle_mDBC_outdp=0.00025_GPU/measuretool/_PointsVelocity_Vel.z.csv",
##]
##
#
###3D Pipe big - changed db
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPU/1/2/Posieulle_mDBC_out_16s/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_8s_GPU/measuretool/_PointsVelocity_Vel.z.csv"
#]
#
###3D Pipe big - changed db
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_boundary_2_GPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv",
#]
#
#
##3D Pipe big - changed db
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.008/measuretool/_PointsVelocity_Vel.z.csv",    
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.004_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_4_FreeCadPosieulleBigExample/Posiuelle/Posiuelle_out_dp_0.002_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
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
#]
#
###3D Pipe big - Shifting
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_0/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_1/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_2/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/Posieulle_mDBC_out_shifting_3/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/_PointsVelocity_Vel.z_clean_3D_Analytical.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/FirstResultsSimulation/Posieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
###2D
##CSV_FILES = [
##  "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/github/2D/CasePoiseuille_FS_LR_dp_0_04_mDBC_out/measuretool/_PointsVelocity_Vel.x.csv"
##]
#
##3D Zentral - GPU vs CPU
#
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_firstOkay/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
##3D - CPU own vs GBU own - UnterschiedGPUundCPU
#CSV_FILES = [
##"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.002_GPU_H_Dp=2.07846_KernelH_0.004157/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.003_GPU_H_Dp=2.07846_KernelH_0.006235/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.002/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.003/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
##3D Zentral - GPU vs CPU
#
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_CPU_dp_0.0075/measuretool/_PointsVelocity_Vel.z.csv",
#    "/run/user/1257/gvfs/sftp:host=tinygpu/home/hpc/iwsp/iwsp110h/Programms/DualSPHysicsImplementationV2/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0075/measuretool/_PointsVelocity_Vel.z.csv", 
#    "/run/user/1257/gvfs/sftp:host=tinygpu/home/hpc/iwsp/iwsp110h/Programms/DualSPHysicsImplementationV2/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.00375/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_CPU_dp0.00375/measuretool/_PointsVelocity_Vel.z.csv",
#   # "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentral/ZentralPosieulle/ZentralPosieulle_mDBC_out_CPU_dp0.00375_single?/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
##3D - CPU own vs GBU own - UnterschiedGPUundCPU
#CSV_FILES = [
#"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.002_GPU_H_Dp=2.07846_KernelH_0.004157/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/mycode/3D/Posieulle_mDBC_out_dp_0.003_GPU_H_Dp=2.07846_KernelH_0.006235/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.002/measuretool/_PointsVelocity_Vel.z.csv",
##"/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/CPU/myCode/3D/Posiuelle_mDBC_out_0.003/measuretool/_PointsVelocity_Vel.z.csv",
#]
#
###3D Pipe big - changed db
#CSV_FILES = [
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Poisuelle_mDBC_out_dp_0.001_CPU/measuretool/_PointsVelocity_Vel.z.csv",
#"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/02_3_2_FreeCadMeasurmentAndValidation/Analytical/Analytical/Analytical/AnalyticalTransientProfile_t_1_0.csv",
#]

#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#]

#####Test Scheuerlein
####
##CSV_FILES = [
##    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
##    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.005/measuretool/_PointsVelocity_Vel.z.csv",
##    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
##    "/nishome/PaulS/Desktop/ParameterStudie/GPUvsCPU/GPU/ZentrischesBeispiel/ZentralPosieulle_mDBC_out_dp_0.01_GPU/measuretool/_PointsVelocity_Vel.z.csv",
##    "analytical/analytical/AnalyticalTransientProfile_t_25sekunde.csv",
##    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.005/measuretool/_PointsVelocity_Vel.z.csv",
##]
##

###Test
##
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
#    #"/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#]

#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.005/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsbeta/DualSPHysics_v6.0_BETA/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.01/measuretool/_PointsVelocity_Vel.z_gekürzt.csv",
#]
#
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.005/measuretool/_PointsVelocity_Vel.z_gekürzt.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsbeta/DualSPHysics_v6.0_BETA/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPoiseuille_mDBC_out/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.01/measuretool/_PointsVelocity_Vel.z_gekürzt.csv",
#    "analytical/analytical/AnalyticalTransientProfile_t_3_9sekunde.csv",
#]
#
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.005/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/Analytical_t_0_25/Analytical/AnalyticalTransientProfile_t_50sekundeFinalRe<.csv",
#]
#
#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/Analytical_t_0_25/Analytical/AnalyticalTransientProfile_t_50sekundeFinalRe<.csv",
#]
#
#CSV_FILES = [
#   "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesRe</_PointsVelocity_Vel.z.csv",
#    #"/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe</AnalyticalTransientProfile_t_30sekundeFinalRe<<_SmallerMessDPRes.csv",
#    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe</AnalyticalTransientProfile_t_All.csv"
#]
#
#CSV_FILES = [
#   "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/simulationvaluesNewmeasurmentRe</_PointsVelocity_Vel.z.csv",
#    #"/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesRe</AnalyticalTransientProfile_t_30sekundeFinalRe<<_SmallerMessDPRes.csv",
#    "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesNewMeasurmentRe</AnalyticalTransientProfile_t_All.csv"
#]

#CSV_FILES = [
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
#    "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.01/measuretool/_PointsVelocity_Vel.z.csv",
#]

CSV_FILES = [
   # "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_dp_0.0025/measuretool/_PointsVelocity_Vel.z.csv",
       "/nishome/PaulS/Desktop/FinaleAuswertung/Posieulle/thereotecialvaluesNewMeasurmentRe</AnalyticalTransientProfile_t_All.csv",
       "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/ZentralPosieulle_mDBC_out_setrwdraw_true_dp_0.0025/measuretoolnewDP/_PointsVelocity_Vel.z.csv",
   # "/nishome/PaulS/Programms/DualSPHysicsImplementation/DualSPHysics/examples/mdbc/xx_PosieulleVeryBigZentralV2/ZentralPosieulle/Analytical_t_0_25/Analytical/AnalyticalTransientProfile_t_50sekundeFinalRe<.csv",

]
#

#
##PARTS = [ 50]  # gewünschte Part IDs
#PARTS = [12, 25, 50, 100 ,150, 500]
##PARTS = [150]
#PARTS = [10,20,25,30,300]
#
PARTS = [10,25,50,100,200,250,300]
PARTS = [300]
## --------------------------------------------------------
## Eine gemeinsame Figure
# --------------------------------------------------------
plt.figure(figsize=(12, 7))
plt.title("Vel.z over pipe diameter — comparison of different particle distances")

for CSV_FILE in CSV_FILES:

    # Read base data
    raw = pd.read_csv(CSV_FILE, sep=";", header=None)
    z_values = raw.iloc[0, 2:].astype(float).values

    data = pd.read_csv(CSV_FILE, sep=";", skiprows=3)
    vel_cols = [c for c in data.columns if c.startswith("Vel.z_")]

    # Dateiname ohne Pfad
    file_label = CSV_FILE.split("/")[-3]  # Ordnername, besser als der File-Name

    for part_id in PARTS:
        row = data.loc[data["Part"] == part_id]
        if row.empty:
            print(f"⚠️ Part {part_id} nicht gefunden in {CSV_FILE}")
            continue

        vel_values = row.iloc[0][vel_cols].values.astype(float)

        time = part_id*0.01

        # Label: <Folder> — Part <id>
        label = f"{file_label} — Zeitpunkt {time}s"

        plt.plot(z_values, vel_values, marker="o", linewidth=2, label=label)
        #plt.plot(z_values, vel_values, linestyle="None",  marker="o", markersize=5, label=label)

plt.xlabel("X-Koordinate [m]")
plt.ylabel("Vel.z [m/s]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.savefig("test")

plt.figure(figsize=(12, 7))
plt.title("Vel.z over pipe diameter — Simulation vs. Analytik")

legend_added_analytical = False
legend_added_sim = False

for CSV_FILE in CSV_FILES:

    raw = pd.read_csv(CSV_FILE, sep=";", header=None)
    z_values = raw.iloc[0, 2:].astype(float).values

    data = pd.read_csv(CSV_FILE, sep=";", skiprows=3)
    vel_cols = [c for c in data.columns if c.startswith("Vel.z_")]

    is_analytical = "Analytical" in CSV_FILE

    for part_id in PARTS:
        row = data.loc[data["Part"] == part_id]
        if row.empty:
            continue

        vel_values = row.iloc[0][vel_cols].values.astype(float)

        if is_analytical:
            # 🔴 analytisch: rote Linie, nur EIN Legenden-Eintrag
            plt.plot(
                z_values,
                vel_values,
                color="red",
                linewidth=2.5,
                zorder = 3,
                label="Analytical solution" if not legend_added_analytical else None
            )
            legend_added_analytical = True
        else:
            # ⚫ Simulation: schwarze Punkte, KEINE Linie, KEINE Legende
            plt.plot(
                z_values,
                vel_values,
                linestyle="None",
                marker="o",
                markersize=5,
                color="black",
                alpha=0.9,
                zorder = 5,
                label="Simulation solution" if not legend_added_sim else None
            )
            legend_added_sim = True

# --------------------------------------------------------
# Styling
# --------------------------------------------------------
plt.xlabel("X-Koordinate [m]")
plt.ylabel("Vel.z [m/s]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
