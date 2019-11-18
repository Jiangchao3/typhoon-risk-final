import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import pandas as pd
import math
from math import sin,radians,cos,asin,sqrt,atan2
import parameter
from customizeFunction import function as func
from scipy import integrate
import datetime

'''
直接求L_ST Alpha_ST
'''

print("start program:",datetime.datetime.now())
# getting parameter
print("getting parameters")
parameter    = parameter.SiteInfo()
begYear      = parameter.begYear()
endYear      = parameter.endYear()
totalYear    = endYear-begYear+1
radiusInflu  = parameter.radiusInflu()
returnPeriod = parameter.returnPeriod()
allWeatherStaionInfo = parameter.allWeatherStaionInfo()
caseInfo  = parameter.caseInfo()

for iKey in caseInfo.keys():
    tyNum    = str(caseInfo[iKey]['tyNum'])
    siteName = str(caseInfo[iKey]['stationID'])
    caseName = 'typhoon'+tyNum+"_in_site"+siteName
    latSite  = allWeatherStaionInfo[siteName]['lat']
    lonSite  = allWeatherStaionInfo[siteName]['lon']
    
    
    inputFileName = r"data_caseTyKeyParameter/"+caseName+".csv"
    print("reading data from",inputFileName)
    dataset = pd.read_csv(inputFileName,header=None,sep=',')
    dataset = np.array(dataset)
    m ,n    = np.shape(dataset)
    tcNum = dataset[:,0]
    date  = dataset[:,1]
    lats  = dataset[:,2]
    lons  = dataset[:,3]
    Pres  = dataset[:,4]
    
    tyNum    = []
    Date     = []
    VT       = []
    deltaP   = []
    Rmax     = []
    Dmin     = []
    L_ST     = []
    Alpha_ST = []
    Theta    = []
    
    for i in range(0,m-1):
        ### VT
        dist = func.SphereDistance(lons[i], lats[i], lons[i+1], lats[i+1]) # unit:KM
        VT_temp = dist/6.0   # unit: km/h
        ### DeltaP 
        P0 = 1010.0
        deltaP_temp = P0 - Pres[i]
        ### Rmax samples
        # obtain Rmax from center pressure with empirical formula
        Rmax_temp =  1119 * (1010-Pres[i])**(-0.805)
        ### Dmin samples
        lon1 = lons[i]
        lat1 = lats[i]
        lon2 = lons[i+1]
        lat2 = lats[i+1]
        if lon1==lon2 and lat1==lat2 :
            #print(i)
            continue
        iTheta0 = func.getAzimuth(lon1,lat1,lon2,lat2)
        iTheta1 = func.getAzimuth(lon1,lat1,lonSite,latSite)
        iAlpha  = iTheta1 -iTheta0
        if iAlpha < 0 :
            iAlpha = abs(iAlpha)
        if iAlpha > 180:
            iAlpha = iAlpha -180.0
        if iAlpha > 90 :
            iAlpha = 180 - iAlpha
        iDist = func.SphereDistance(lon1,lat1,lonSite,latSite)
        iAlpha = math.pi*iAlpha/180.0
        #iDmin = radiusInflu*sin(iAlpha)
        iDmin = iDist*sin(iAlpha)
        if iTheta0<iTheta1 :
            iDmin = -1.0*abs(iDmin)
        else:
            iDmin = abs(iDmin)
        ### iL_ST 台风中心和模拟点的距离
        iL_ST = iDist
        ### iAlpha_ST 以台风移动和iL_ST之间的夹角
        iAlpha_ST = math.atan(iDmin/iL_ST)*180.0/np.pi
        ### Theta samples 
        iAzimuth = func.getAzimuth(lon1,lat1,lon2,lat2)
        Theta.append(iAzimuth)
      
        if VT_temp >= 2.0 and VT_temp <= 65 : # eliminate data outside the range 0-65km
            if deltaP_temp >= 0.0 and deltaP_temp <= 135 : # eliminate data outside the range 0-135hPa
                #if Rmax_temp >= 8.0 and Rmax_temp <= 100: # eliminate data outside the range 8-100km
                if Rmax_temp >= 8.0 and Rmax_temp <= 200: # eliminate data outside the range 8-100km
                    VT.append(VT_temp)
                    deltaP.append(deltaP_temp)
                    Rmax.append(Rmax_temp)
                    Dmin.append(iDmin)
                    Theta.append(iAzimuth)
                    L_ST.append(iL_ST)
                    Alpha_ST.append(iAlpha_ST)
                    Date.append(date[i])
                    tyNum.append(tcNum[i])
                else:
                    print("eliminate record:",date[i],"for Rmax did not meet the condition, Rmax=",Rmax_temp)
            else:        
                print("eliminate record:",date[i],"for deltaP did not meet the condition, deltaP=",deltaP_temp)
        else:
            print("eliminate record:",date[i],"for VT did not meet the condition, VT=",VT_temp)
                
    VT       = np.array(VT)
    deltaP   = np.array(deltaP)
    Rmax     = np.array(Rmax)
    Dmin     = np.array(Dmin)
    Theta    = np.array(Theta)
    L_ST     = np.array(L_ST)
    Alpha_ST = np.array(Alpha_ST)
    Date     = np.array(Date)
    tyNum    = np.array(tyNum)
    
    # output
    outFileName = "data_caseTyKeyParameter/"+caseName+"_keyParameters.csv"
    print("output file:",outFileName)
    allDataLine = np.zeros((len(VT),9))
    for i in range(len(VT)):
        # VT, DeltaP, Rmax, Theta, Dmin
        allDataLine[i,0] = tyNum[i]
        allDataLine[i,1] = Date[i]
        allDataLine[i,2] = VT[i]
        allDataLine[i,3] = deltaP[i]
        allDataLine[i,4] = Rmax[i]
        allDataLine[i,5] = Dmin[i]
        allDataLine[i,6] = L_ST[i]
        allDataLine[i,7] = Alpha_ST[i]
        allDataLine[i,8] = Theta[i]
    np.savetxt(outFileName, allDataLine, delimiter = ',', fmt='%s')

print("end program:",datetime.datetime.now())

