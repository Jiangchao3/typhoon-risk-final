###############################################################
# This script calculate Vmax according return period 
# History : 2019.07.25 V1.0
# Author  : Gao Yuanyong 1471376165@qq.com
###############################################################
from scipy import stats as st
import pandas as pd
import numpy as np
import parameter
import datetime
import matplotlib.pyplot as plt

print("start program",datetime.datetime.now())

### getting parameter
print("getting parameters")
parameter    = parameter.SiteInfo()
begYear      = parameter.begYear()
endYear      = parameter.endYear()
totalYear    = endYear-begYear+1
radiusInflu  = parameter.radiusInflu()
returnPeriod = parameter.returnPeriod()
allWeatherStationInfo = parameter.allWeatherStaionInfo()
allWindFarmInfo = parameter.allWindFarmInfo()
specialWindFarmInfo = parameter.specialWindFarmInfo()
oneSiteInfo = parameter.oneSiteInfo()


KEY = 2 # 2,3
if KEY==1: #陆地站点
    totalDict = allWeatherStationInfo
    #衰减系数
    factor = [1.0,1.0,1.0,0.95,0.85,0.9,1.1,0.8,0.9,0.75,0.9]
    outVmax50a = "VmaxReturnPeriodAllWeatherStation50a.csv" 
if KEY==2: #海上风电场
    totalDict = allWindFarmInfo
    factor = [1,1,1,1,1,1,1,1,1,1,1,1,1]
    outVmax50a = "VmaxReturnPeriodAllWeatherStation50a.csv"
if KEY==3: #湛江
    totalDict = oneSiteInfo #湛江
    factor = [0.85]
    outVmax50a = "VmaxReturnPeriodOneSite50a.csv"

factor = np.array(factor)
numF = 0

for iKey in totalDict.keys():
    ### 
    siteName = totalDict[iKey]['name']
    latSite  = totalDict[iKey]['lat']
    lonSite  = totalDict[iKey]['lon']
   
    print(' ') 
    print('station:',iKey,siteName)
    ### read data 
    inputFileSim = r"./allTyphoonVmax/"+iKey+"Vmax.csv"
   
    outputAnnualSeqVmax = r"./outputVmax/AnnualSeq/"+iKey+"AnnualSeqVmax.csv" 
    outputTyCaseVmax = r"./outputVmax/TyCase/"+iKey+"TyCaseVmax.csv" 
    
    datasetSim = pd.read_csv(inputFileSim,header=None,sep=',')
    datasetSim = np.array(datasetSim)
    mSim ,nSim = np.shape(datasetSim)
    VmaxSim    = datasetSim[:,2]  # Vmax at 10m
    DirSim     = datasetSim[:,3]  # Vmax at 10m
    DirSim[DirSim>360] = DirSim[DirSim>360] - 360
    DirSim[DirSim<0] = DirSim[DirSim<0] + 360
    tyNumSim   = datasetSim[:,0]
    allDate    = datasetSim[:,1]  # Vmax at 10m
    # 衰减
    VmaxSim = VmaxSim*factor[numF]
    print("factor:",factor[numF],numF)
    numF += 1 
    
    VmaxSim0 = []
    dateNew  = []
    vmaxDict = {}
    yyyyMax = int(int(allDate[0])/1000000)
    VmaxMax     = 0
    VmaxMax100m = 0
    for i in range(mSim):
        iDate = allDate[i]
        yyyy = int(int(iDate)/1000000)
        if yyyy == yyyyMax:
            if VmaxSim[i] > VmaxMax:
                VmaxMax = VmaxSim[i]
                VmaxMax100m = VmaxMax*1.32
        else:
            VmaxSim0.append(VmaxMax)
            dateNew.append(yyyyMax)
            vmaxDict[int(yyyyMax)] = {'spd10m':VmaxMax,'spd100m':VmaxMax100m} 
            yyyyMax = int(int(allDate[i])/1000000)
            VmaxMax = VmaxSim[i]
            VmaxMax100m = VmaxMax*1.32
        if i == mSim-1:
            VmaxSim0.append(VmaxMax)
            dateNew.append(yyyyMax)
            vmaxDict[int(yyyyMax)] = {'spd10m':VmaxMax,'spd100m':VmaxMax100m}
 
    VmaxSim0 = np.array(VmaxSim0)
    length = 2019-1970
    year = []
    spd10m = []
    spd100m = []
    for i in range(length):
        itKey = i+1970
        if itKey in vmaxDict.keys():
            year.append(itKey)
            spd10m.append(vmaxDict[itKey]['spd10m'])
            spd100m.append(vmaxDict[itKey]['spd100m'])
        else:
            year.append(itKey)
            spd10m.append(-999.0)
            spd100m.append(-999.0)
    spd10m  = np.array(spd10m)
    spd100m = np.array(spd100m)
    spd10m  = np.around(spd10m, decimals=2)
    spd100m = np.around(spd100m, decimals=2)
    dataframe = pd.DataFrame({'Year':year,'Vmax10m':spd10m,'Vmax100m':spd100m})
    dataframe.to_csv(outputAnnualSeqVmax,sep=',',index=False)
 
    tyNumSim1 = []
    spdSim10m  = []
    spdSim100m = []
    VmaxMax   = VmaxSim[0]
    VmaxMax100m  = VmaxSim[0]*1.32
    tyNumMax = tyNumSim[0]
    for i in range(1,mSim):
        if tyNumSim[i] == tyNumSim[i-1]:
            if VmaxSim[i]>VmaxMax:
                VmaxMax = VmaxSim[i]
                VmaxMax100m = VmaxSim[i]*1.32
                if i == mSim-1:
                    tyNumSim1.append(tyNumSim[i])
                    spdSim10m.append(VmaxMax)
                    spdSim100m.append(VmaxMax100m)
            else:
                if i == mSim-1:
                    tyNumSim1.append(tyNumSim[i])
                    spdSim10m.append(VmaxMax)
                    spdSim100m.append(VmaxMax100m)
        else:
            tyNumSim1.append(tyNumSim[i-1])
            spdSim10m.append(VmaxMax)
            spdSim100m.append(VmaxMax100m)
            VmaxMax = VmaxSim[i]
            VmaxMax100m = VmaxSim[i]*1.32
            if i == mSim-1:
                tyNumSim1.append(tyNumSim[i])
                spdSim10m.append(VmaxMax)
                spdSim100m.append(VmaxMax100m)
    tyNumSim1  = np.array(tyNumSim1)
    spdSim10m  = np.array(spdSim10m)
    spdSim100m = np.array(spdSim100m)
    tyNumSim1  = tyNumSim1.astype(int)
    tyNumList  = []
    for i in range(len(tyNumSim1)):
        tyNumStr = str(tyNumSim1[i])
        tyNumList.append(tyNumStr.zfill(4))
    spdSim10m  = np.around(spdSim10m, decimals=2)
    spdSim100m = np.around(spdSim100m, decimals=2)
    dataframe = pd.DataFrame({'tyNum':tyNumList,'Vmax10m':spdSim10m,'Vmax100m':spdSim100m})
    dataframe.to_csv(outputTyCaseVmax,sep=',',index=False)

print("end program:", datetime.datetime.now())

