########################################################
# Georgiou Windfield Model
# History: 2019.07.25  V1.0
#          2019.08.28  V1.1  add deltaT argument.
# Author : gaoyuanyong 1471376165@qq.com
#######################################################

import numpy as np
import scipy.stats as st
import pandas as pd
import math
import Shapiro

shapiro = Shapiro.Shapiro()

class Georgiou:
    def __int__(self):
        pass

    def GeorgiouWindFieldModel(self,DeltaP0,VT0,Rmax0,Theta0,iL_ST0,iAlpha_ST0,deltaT=20):
        ### typhoon key parameter 台风关键参数
        DeltaP = DeltaP0*100    # Pa  中心气压差
        VT     = VT0/3.6    # m/s 移动速度
        Rmax   = Rmax0*1000 # m   最大风速半径
        Theta  = Theta0        # dergee 移动方向
        iL_ST  = iL_ST0*1000
        iAlpha_ST = iAlpha_ST0
        #print("DeltaP = ",DeltaP)
        #print("VT = ",VT)
        #print("Rmax = ",Rmax)
        #print("Theta = ",Theta)
        #print("iL_ST = ",iL_ST)
        #print("iAlpha_ST = ",iAlpha_ST)
        # parameter
        K     = 5*10000                             # m^2/s
        omega = 7.292*pow(10,-5)
        f     = 2 * omega *np.sin(30/180.0*np.pi)   # 科氏参数
        h     = 1000                                # m
        B     = 1.5 + (980-1010+DeltaP/100)/120     # Hoolland B指数
        DensityAir = 1.15 #空气密度1.15kg/m^3
       
        # 700hPa(2.5km)高度在(iL_ST,iAlpha_ST)处的梯度风(未用到)
        #iAlpha_ST0 = iAlpha_ST*np.pi/180.0
        #arg0_Vg = 0.5*(VT*math.sin(iAlpha_ST0)-f) # part1
        #arg1_Vg = B*DeltaP/DensityAir*pow(Rmax/iL_ST,B)
        #arg2_Vg = pow(np.exp(-1.0*(Rmax/iL_ST)),B)
        #arg3_Vg = 0.25*(VT*math.sin(iAlpha_ST0)-f)**2
        #arg4_Vg = math.sqrt(arg1_Vg*arg2_Vg + arg3_Vg)  # part2
        #Vgrdiant = arg0_Vg + arg4_Vg
        
        # 700hPa(2.5km)高度在Rmax平均梯度风
        Angle  = np.linspace(0,350,36)
        Angle0 = Angle*np.pi/180.0
        allVgRmax = []
        for i in range(len(Angle)):
            arg0_Vg = 0.5*(VT*math.sin(Angle0[i])-f) # part1
            arg1_Vg = B*DeltaP/DensityAir*pow(Rmax/Rmax,B)
            arg2_Vg = pow(np.exp(-1.0*(Rmax/Rmax)),B)
            arg3_Vg = 0.25*(VT*math.sin(Angle0[i])-f)**2
            arg4_Vg = math.sqrt(arg1_Vg*arg2_Vg + arg3_Vg) # part2
            iVgRmax = arg0_Vg + arg4_Vg
            allVgRmax.append(iVgRmax)
        allVgRmax = np.array(allVgRmax)
        VgrdiantRmax = np.sum(allVgRmax)/len(allVgRmax)
        
        # Shpiro在(iL_ST,iAlpha_ST)处风速,风向
        V_SHBL_Spd, V_SHLB_Dir = shapiro.ShapiroWindFieldModel(DeltaP0,VT0,Rmax0,Theta0,iL_ST0,iAlpha_ST0,deltaT) 
        
        # Shpiro在Rmax处平均风速(角度平均)
        Angle  = np.linspace(0,350,36)
        allV_SHBL_Spd_Rmax = []
        for i in range(len(Angle)): 
            iV_SHBL_Spd, Dir = shapiro.ShapiroWindFieldModel(DeltaP0,VT0,Rmax0,Theta0,Rmax0,Angle[i],deltaT)
            allV_SHBL_Spd_Rmax.append(iV_SHBL_Spd)
        allV_SHBL_Spd_Rmax = np.array(allV_SHBL_Spd_Rmax)
        V_SHBL_Spd_Rmax = np.sum(allV_SHBL_Spd_Rmax)/len(allV_SHBL_Spd_Rmax)
        
        # 500m高度(iL_ST,iAlpha_ST)处的风速
        V500 = V_SHBL_Spd*VgrdiantRmax/V_SHBL_Spd_Rmax
        #print("V_SHBL_Spd = ",V_SHBL_Spd) 
        #print("VgrdiantRmax = ",VgrdiantRmax) 
        #print("V_SHBL_Spd_Rmax = ",V_SHBL_Spd_Rmax) 
        
        # 10m高度(iL_ST,iAlpha_ST)处的风速，风向
        arg_phi = iL_ST/Rmax
        # Phi衰减系数
        if arg_phi >= 0.5 and arg_phi <= 2.0 :
            Phi = 0.825
        elif arg_phi < 0.5 :
            Phi = 1.0 + (0.828-1.0)*arg_phi
        elif arg_phi >= 2.0 and arg_phi <= 5.0 :
            Phi = 0.825 + (0.75-0.825)*(arg_phi - 2.0)/3.0  
        else: # >5.0
            Phi = 0.75
    
        V10_Spd = Phi*V500 
        V10_Dir = V_SHLB_Dir 
     
        return (V10_Spd,V10_Dir)
   

if __name__ == '__main__':
    print("I am GeorgiouWindFieldModel")


 
