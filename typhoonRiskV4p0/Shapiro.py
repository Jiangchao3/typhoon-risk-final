#############################################################
# Shapiro Windfield model
# History : 2019.07.25  v1.0
#           2019.08.13  v1.1, revised wind direction output
#           2019.09.28  v1.2, (1)add loop of smooth;
#                             (2)add deltaT argument.
#                             (3)set eps = 0.0001, and the max loop is 2000.
# Author  : gaoyy  1471376165@qq.com
#############################################################
import numpy as np
import scipy.stats as st
import pandas as pd
import math

class Shapiro:
    def __int__(self):
        pass

    def ShapiroWindFieldModel(self,DeltaP0,VT0,Rmax0,Theta0,iL_ST,iAlpha_ST,deltaT=10):
        ### Shapiro windfiled model(average of 0-500m)
        ### typhoon key parameter 台风关键参数
        DeltaP = DeltaP0*100    # Pa  中心气压差
        VT     = VT0/3.6    # m/s 移动速度
        Rmax   = Rmax0*1000 # m   最大风速半径
        Theta  = Theta0        # dergee 移动方向
        iL_ST  = iL_ST*1000
        iAlpha_ST = iAlpha_ST
        # parameter
        K     = 5*10000                             # m^2/s
        omega = 7.292*pow(10,-5)
        f     = 2 * omega *np.sin(30/180.0*np.pi)   # 科氏参数
        h     = 1000                                # m
        B     = 1.5 + (980-1010+DeltaP/100)/120     # Hoolland B指数
        #print("K = ",K)
        #print("f = ",f)
        #print("h = ",h)
        #print("B = ",B)
     
        # generate grid 以台风中心为原点，按极坐标系剖分网格
        X1      = np.linspace(0,200,41) # 0-200km范围的dx为5km
        X2      = []                    # 200-1300km,dx线性增加
        X2Temp1 = 200
        ideltaX = 5.0
        while True:
            #ideltaX = ideltaX + 0.1     # 按0.1km线性增加
            ideltaX = ideltaX + 0.5     # 按0.5km线性增加
            X2Temp2 = X2Temp1 + ideltaX
            if X2Temp2 >= 1300:
                break
            X2.append(X2Temp2)
            X2Temp1 = X2Temp2
        X2 = np.array(X2)
        X1List = list(X1)
        X2List = list(X2)
        X1List.extend(X2List)       # 0-200km与200-1300km拼接为一个数>组
        X = np.array(X1List)        # 0-1300km
        X = X*1000
        Y = np.linspace(0,360,73)   # lambda 0-360 deg,dy=5 deg
        Nx = len(X)                 # number of X grids 
        Ny = len(Y)                 # number of Y grids
        #print("Nx and Ny :",Nx,Ny)
        
        # mesh 网格二维化 
        XX = np.zeros((Nx,Ny))
        YY = np.zeros((Nx,Ny))
        for i in range(Ny):
            XX[:,i] = X[:]
    
        for i in range(Nx):
            YY[i,:] = Y[:]
        # dt, dx, dy
        #deltaT = 20 # second 积分时间步长,已添加至传入参数，默认20
        deltaY = 5  # degree y轴方向步长 
        deltaX = np.zeros((Nx,Ny)) # meter x轴方向步长
        for i in range(1,Nx):
            deltaX[i,:] = XX[i,:] - XX[i-1,:]
        #print("dt = ",deltaT)
        #print("dy = ",deltaY)
        #print("dx = ",deltaX[:,1])
        
        # 确定模拟点的坐标(ix,iy)
        ixL_ST     = iL_ST
        iyAlpha_ST = iAlpha_ST + Theta
        if iyAlpha_ST < 0.0 :
            iyAlpha_ST = iyAlpha_ST+360.0
        ixDist = np.abs(X-ixL_ST)
        iyDist = np.abs(Y-iyAlpha_ST)
        ixMinDist = np.min(ixDist)
        iyMinDist = np.min(iyDist)
        ixAll = np.where(ixDist == ixMinDist)
        iyAll = np.where(iyDist == iyMinDist)
        ix = ixAll[0][0]
        iy = iyAll[0][0]
        #print(np.shape(iyAll))
        # Uc and Vc, Uc为台风径向移动速度，Vc为切向移动速度
        Theta1 = YY - Theta
        Theta1 = Theta1*np.pi/180.0
        Uc     = VT*np.cos(Theta1)
        Vc     = VT*np.sin(Theta1)
    
        # Holland pressure field
        deltaPP = np.zeros((Nx,Ny))  # 气压梯度
        arg0 = DeltaP*B/XX[1:Nx,:]
        arg1_temp = Rmax/XX[1:Nx,:]
        arg1 = pow(arg1_temp,B)
        arg2 = np.exp( -1.0*pow((Rmax/XX[1:Nx,:]),B) )
        arg3 = np.multiply(arg0,arg1)
        deltaPP[1:Nx,:] = np.multiply(arg2,arg3)
        deltaPP[0,:] = 0.0 # 内侧边界气压梯度为0
        deltaPP[:,Ny-1] = deltaPP[:,0] # 周期边界
    
        A = np.array([0.125, 0.125, 0.5, 0.125, 0.125]) # 五点平滑系数,上下左右和本身共五点，本身权重0.5 
        deltaPP[1:Nx-1,1:Ny-1] = A[0]*deltaPP[0:Nx-2,1:Ny-1] + A[1]*deltaPP[2:Nx,1:Ny-1] + A[2]*deltaPP[1:Nx-1,1:Ny-1] + \
                                 A[3]*deltaPP[1:Nx-1,0:Ny-2] + A[4]*deltaPP[1:Nx-1,2:Ny]
        deltaPP[1:Nx-1,0]      = A[0]*deltaPP[0:Nx-2,0] + A[1]*deltaPP[2:Nx,0] + A[2]*deltaPP[1:Nx-1,0] + \
                                 A[3]*deltaPP[1:Nx-1,Ny-2] + A[4]*deltaPP[1:Nx-1,1]
    
        # initial condition(IC) 初始条件
        U_IC = np.zeros((Nx,Ny))
        V_IC = np.zeros((Nx,Ny))
        U_IC[:,:] = 0.0
        V_IC = deltaPP/f
        #print("max and min of V_IC :",np.max(V_IC),np.min(V_IC))
    
        # smooth IC (i-1,j),(i+1,j),(i,j),(i,j-1),(i,j+1)
        for iSmooth in range(1): # 平滑次数 add by gyy 20190928
            U_IC[1:Nx-1,1:Ny-1] = A[0]*U_IC[0:Nx-2,1:Ny-1] + A[1]*U_IC[2:Nx,1:Ny-1] + A[2]*U_IC[1:Nx-1,1:Ny-1] + \
                                  A[3]*U_IC[1:Nx-1,0:Ny-2] + A[4]*U_IC[1:Nx-1,2:Ny]
            U_IC[1:Nx-1,0]      = A[0]*U_IC[0:Nx-2,0] + A[1]*U_IC[2:Nx,0] + A[2]*U_IC[1:Nx-1,0] + \
                                  A[3]*U_IC[1:Nx-1,Ny-2] + A[4]*U_IC[1:Nx-1,1]
            U_IC[1:Nx-1,Ny-1]   = U_IC[1:Nx-1,0]
    
            V_IC[1:Nx-1,1:Ny-1] = A[0]*V_IC[0:Nx-2,1:Ny-1] + A[1]*V_IC[2:Nx,1:Ny-1] + A[2]*V_IC[1:Nx-1,1:Ny-1] + \
                                  A[3]*V_IC[1:Nx-1,0:Ny-2] + A[4]*V_IC[1:Nx-1,2:Ny]
            V_IC[1:Nx-1,0]      = A[0]*V_IC[0:Nx-2,0] + A[1]*V_IC[2:Nx,0] + A[2]*V_IC[1:Nx-1,0] + \
                                  A[3]*V_IC[1:Nx-1,Ny-2] + A[4]*V_IC[1:Nx-1,1]
            V_IC[1:Nx-1,Ny-1]   = V_IC[1:Nx-1,0]
        #print("max and min of V_IC :",np.max(V_IC),np.min(V_IC))
       
        # boundary condition(BC) 边界条件
        U_BC_Inner = np.zeros(Ny)
        V_BC_Inner = np.zeros(Ny)
        U_BC_Outer = np.zeros(Ny)
        V_BC_Outer = np.zeros(Ny)
        U_BC_Inner[:] = 0.0
        V_BC_Inner[:] = 0.0
        U_BC_Outer[:] = 0.0
        V_BC_Outer = V_IC[Nx-1,:]
    
        # n时刻和n+1时刻定义
        U0 = U_IC
        V0 = V_IC
        U0[:,Ny-1] = U0[:,0]
        V0[:,Ny-1] = V0[:,0]
        U1 = np.zeros((Nx,Ny))
        V1 = np.zeros((Nx,Ny))
    
        #eps = 0.001
        eps = 0.0001
        UV0 = np.sqrt(U0[ix,iy]*U0[ix,iy]+V0[ix,iy]*V0[ix,iy]) # u and v total wind speed 
        #for it in range(1000):
        for it in range(2000):
            Cx = f*V0[1:Nx-1,1:Ny-1]
            Cy = -1.0*f*U0[1:Nx-1,1:Ny-1]
    
            Px = deltaPP[1:Nx-1,1:Ny-1]
            Py = 0
    
            Ex0 = (U0[0:Nx-2,1:Ny-1]-U0[2:Nx,1:Ny-1])/XX[1:Nx-1,1:Ny-1]/2.0/deltaX[1:Nx-1,1:Ny-1] # 中央差
            Ex1 = (U0[0:Nx-2,1:Ny-1]-2*U0[1:Nx-1,1:Ny-1]+U0[2:Nx,1:Ny-1])/deltaX[1:Nx-1,1:Ny-1]/deltaX[1:Nx-1,1:Ny-1] # 中央差
            Ex2 = (U0[1:Nx-1,0:Ny-2]-2*U0[1:Nx-1,1:Ny-1]+U0[1:Nx-1,2:Ny])/deltaY/deltaY/XX[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1] #中央差
            Ex3 = -1.0*U0[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1]
            Ex4 = -2.0*(V0[1:Nx-1,0:Ny-2]-V0[1:Nx-1,2:Ny])/2.0/deltaY/XX[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1]
            Ex  = -1.0*K*(Ex0+Ex1+Ex2+Ex3+Ex4)
    
            Ey0 = (V0[0:Nx-2,1:Ny-1]-V0[2:Nx,1:Ny-1])/XX[1:Nx-1,1:Ny-1]/2.0/deltaX[1:Nx-1,1:Ny-1] # 中央差
            Ey1 = (V0[0:Nx-2,1:Ny-1]-2*V0[1:Nx-1,1:Ny-1]+V0[2:Nx,1:Ny-1])/deltaX[1:Nx-1,1:Ny-1]/deltaX[1:Nx-1,1:Ny-1] # 中央差
            Ey2 = (V0[1:Nx-1,0:Ny-2]-2*V0[1:Nx-1,1:Ny-1]+V0[1:Nx-1,2:Ny])/deltaY/deltaY/XX[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1]
            Ey3 = -1.0*V0[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1]
            Ey4 = 2.0*(U0[1:Nx-1,0:Ny-2]-U0[1:Nx-1,2:Ny])/2.0/deltaY/XX[1:Nx-1,1:Ny-1]/XX[1:Nx-1,1:Ny-1] # 中央差
            Ey  = -1.0*K*(Ey0+Ey1+Ey2+Ey3+Ey4)
    
            CD  = (1.1+ 0.04*np.abs(U0[1:Nx-1,1:Ny-1]+VT))/1000.0
            UUc = U0[1:Nx-1,1:Ny-1]+ Uc[1:Nx-1,1:Ny-1]
            VVc = V0[1:Nx-1,1:Ny-1]+ Vc[1:Nx-1,1:Ny-1]
            UUc2 = np.multiply(UUc,UUc)
            VVc2 = np.multiply(VVc,VVc)
            UUc2VVc2 = UUc2+VVc2
            Fxy0 = np.sqrt(UUc2VVc2)
            Fx1 = np.multiply(Fxy0,UUc)
            Fx  = -1.0*np.multiply(CD,Fx1)/h
            Fy1 = np.multiply(Fxy0,VVc)
            Fy  = -1.0*np.multiply(CD,Fy1)/h
    
            Ax = -1.0*np.multiply(V0[1:Nx-1,1:Ny-1],V0[1:Nx-1,1:Ny-1])/XX[1:Nx-1,1:Ny-1]
            Ay = np.multiply(U0[1:Nx-1,1:Ny-1],V0[1:Nx-1,1:Ny-1])/XX[1:Nx-1,1:Ny-1]
    
            #B0x = U0[1:Nx-1,1:Ny-1]*(U0[2:Nx,1:Ny-1]- U0[1:Nx-1,1:Ny-1])/deltaX[1:Nx-1,1:Ny-1]  # 前差
            #B0y = U0[1:Nx-1,1:Ny-1]*(V0[2:Nx,1:Ny-1]- V0[1:Nx-1,1:Ny-1])/deltaX[1:Nx-1,1:Ny-1]  # 前差
            UAddAbsU = U0[1:Nx-1,1:Ny-1]  + np.abs(U0[1:Nx-1,1:Ny-1])
            USubAbsU = U0[1:Nx-1,1:Ny-1]  - np.abs(U0[1:Nx-1,1:Ny-1])
            diffUxa  = U0[1:Nx-1,1:Ny-1]  - U0[0:Nx-2,1:Ny-1]
            diffUxb  = U0[2:Nx,1:Ny-1]    - U0[1:Nx-1,1:Ny-1]
            diffVxa  = V0[1:Nx-1,1:Ny-1]  - V0[0:Nx-2,1:Ny-1]
            diffVxb  = V0[2:Nx,1:Ny-1]    - V0[1:Nx-1,1:Ny-1]
            B0x = 0.5*(np.multiply(UAddAbsU,diffUxa) + np.multiply(USubAbsU,diffUxb))/deltaX[1:Nx-1,1:Ny-1] # 迎风
            B0y = 0.5*(np.multiply(UAddAbsU,diffVxa) + np.multiply(USubAbsU,diffVxb))/deltaX[1:Nx-1,1:Ny-1] # 迎风
    
            #B1x = V0[1:Nx-1,1:Ny-1]*(U0[1:Nx-1,2:Ny]- U0[1:Nx-1,1:Ny-1])/deltaY/XX[1:Nx-1,1:Ny-1] # 前差
            #B1y = V0[1:Nx-1,1:Ny-1]*(V0[1:Nx-1,2:Ny]- V0[1:Nx-1,1:Ny-1])/deltaY/XX[1:Nx-1,1:Ny-1] # 前差
    
            VAddAbsV = V0[1:Nx-1,1:Ny-1]  + np.abs(V0[1:Nx-1,1:Ny-1])
            VSubAbsV = V0[1:Nx-1,1:Ny-1]  - np.abs(V0[1:Nx-1,1:Ny-1])
            diffUya  = U0[1:Nx-1,1:Ny-1]  - U0[1:Nx-1,0:Ny-2]
            diffUyb  = U0[1:Nx-1,2:Ny]    - U0[1:Nx-1,1:Ny-1]
            diffVya  = V0[1:Nx-1,1:Ny-1]  - V0[1:Nx-1,0:Ny-2]
            diffVyb  = V0[1:Nx-1,2:Ny]    - V0[1:Nx-1,1:Ny-1]
            B1x = 0.5*(np.multiply(VAddAbsV,diffUya) + np.multiply(VSubAbsV,diffUyb))/deltaY/XX[1:Nx-1,1:Ny-1] # 迎风 
            B1y = 0.5*(np.multiply(VAddAbsV,diffVya) + np.multiply(VSubAbsV,diffVyb))/deltaY/XX[1:Nx-1,1:Ny-1] # 迎风 
    
    
            # integration
            U1[1:Nx-1,1:Ny-1] = U0[1:Nx-1,1:Ny-1] + deltaT*(Cx+Px+Ex+Fx-Ax-B0x-B1x)
            V1[1:Nx-1,1:Ny-1] = V0[1:Nx-1,1:Ny-1] + deltaT*(Cy+Ey+Fy-Ay-B0y-B1y)
            #print(np.max(Ax),np.max(B0x),np.max(B1x),np.max(Cx),np.max(Px),np.max(Ex),np.max(Fx)) 
            # smooth 
            for iSmooth in range(1): #平滑次数
                U1[1:Nx-1,1:Ny-1] = A[0]*U1[0:Nx-2,1:Ny-1] + A[1]*U1[2:Nx,1:Ny-1] + A[2]*U1[1:Nx-1,1:Ny-1] + \
                                    A[3]*U1[1:Nx-1,0:Ny-2] + A[4]*U1[1:Nx-1,2:Ny]
                U1[1:Nx-1,0]      = A[0]*U1[0:Nx-2,0] + A[1]*U1[2:Nx,0] + A[2]*U1[1:Nx-1,0] + \
                                    A[3]*U1[1:Nx-1,Ny-2] + A[4]*U1[1:Nx-1,1]
                U1[1:Nx-1,Ny-1]   = U1[1:Nx-1,0]
    
                V1[1:Nx-1,1:Ny-1] = A[0]*V1[0:Nx-2,1:Ny-1] + A[1]*V1[2:Nx,1:Ny-1] + A[2]*V1[1:Nx-1,1:Ny-1] + \
                                    A[3]*V1[1:Nx-1,0:Ny-2] + A[4]*V1[1:Nx-1,2:Ny]
                V1[1:Nx-1,0]      = A[0]*V1[0:Nx-2,0] + A[1]*V1[2:Nx,0] + A[2]*V1[1:Nx-1,0] + \
                                    A[3]*V1[1:Nx-1,Ny-2] + A[4]*V1[1:Nx-1,1]
                V1[1:Nx-1,Ny-1]   = V1[1:Nx-1,0]
            # BC
            U1[0,:] = U_BC_Inner
            V1[0,:] = V_BC_Inner
            U1[Nx-1,:] = U_BC_Outer
            V1[Nx-1,:] = V_BC_Outer
            U1[:,Ny-1] = U1[:,0]
            V1[:,Ny-1] = V1[:,0]
            # n -> n+1
            U0 = U1
            V0 = V1
    
            UV1 = np.sqrt(U1[ix,iy]*U1[ix,iy]+V1[ix,iy]*V1[ix,iy])
            deltaUV = UV1 - UV0
            if it > 100 and deltaUV < eps: # 当模拟点前后两次的风速差>小于eps时，停止迭代
                #print("it = ",it," ,deltaUV < eps = ",eps," ,stop iterating!")
                break
            else:
                UV0 = UV1
        # total wind speed 全风速
        UVspeed = np.sqrt(U1[ix,iy]*U1[ix,iy]+V1[ix,iy]*V1[ix,iy])
        # wind direction 风向
        alpha0 = YY[ix,iy]
        if U1[ix,iy] != 0.0 :
            alpha1 = math.atan(V1[ix,iy]/U1[ix,iy])*180.0/math.pi
            if U1[ix,iy] >= 0 :
                UVdirection = alpha0 + alpha1
            elif U1[ix,iy] < 0 :
                UVdirection = alpha0 + alpha1 +180.0
        else:
            if V1[ix,iy] > 0 :
                UVdirection = alpha0+90 ###
            elif V1[ix,iy]<0 :
                UVdirection = alpha0-90
            else:
                UVdirection = alpha0
       
        if UVdirection < 0 :
            UVdirection = 360 + UVdirection
        elif UVdirection > 360 :
            UVdirection = UVdirection-360
        else:
            pass
        
        #  add by gaoyy at 2019.08.13
        UVdirection = UVdirection + Theta0 
        if UVdirection < 0 :
            UVdirection = 360 + UVdirection
        elif UVdirection > 360 :
            UVdirection = UVdirection-360
        else:
            pass

        # add by gaoy at 20190910 风的去向转化为风的来向，旋转180°
        UVdirection = UVdirection + 180.0
        if UVdirection >360 :
            UVdirection = UVdirection - 360
        elif UVdirection < 0 :
            UVdirection = UVdirection + 360
        else:
            pass
       
        return (UVspeed,UVdirection)
   
if __name__ == '__main__':
    print("I am ShapiroWindFieldModel")
 
