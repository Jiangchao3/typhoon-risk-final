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

# 1 for WeatherStation, 2 for WindFarmInfo, 3 for ZhanJiang
work  = 1 
if work == 1:
    totalDict = allWeatherStationInfo
    factor = [1.0,1.0,1.0,0.95,0.85,0.9,1.1,0.8,0.9,0.75,0.9]
    outVmax50a = "VmaxReturnPeriodAllWeatherStation50a.csv"
elif work == 2:
    totalDict = allWindFarmInfo
    factor = [1,1,1,1,1,1,1,1,1,1,1,1,1]
    outVmax50a = "VmaxReturnPeriodAllWindFarm50a.csv"
elif work == 3:
    totalDict = oneSiteInfo #湛江
    factor = [0.85]
    outVmax50a = "VmaxReturnPeriodOneSite50a.csv"

factor = np.array(factor)
numF = 0
numV = 0
SumErrG = 0

iDataLine2 = np.zeros((len(totalDict),3))
for iKey in totalDict.keys():
    ### 
    siteName = totalDict[iKey]['name']
    latSite  = totalDict[iKey]['lat']
    lonSite  = totalDict[iKey]['lon']
   
    print(' ') 
    print('station:',iKey,siteName)
    ### read data 
    inputFileSim = r"../data_allTyphoonSimpleVmax/"+iKey+"Vmax.csv"
    if work != 1:
        inputFileObs = r"../obs_data/"+iKey+"_obs_vmax.csv" #obs
    else:
        if iKey in ['59488','59324','59321','58941']:
            inputFileObs = r"../obs_data/"+iKey+"_obs_vmax.csv" #obs
        else:
            inputFileObs = r"../obs_data/"+iKey+"_obs_vmax_correct.csv" #obs
   
    outputFileName     = r"./data_vmax/"+iKey+"VmaxFinal.csv" 
    outputFileName100m = r"./data_vmax/"+iKey+"VmaxFinal100m.csv" 
    #print("reading simulation data from",inputFileSim)
    #print("reading observation data from",inputFileObs)
    
    datasetSim = pd.read_csv(inputFileSim,header=None,sep=',')
    datasetSim = np.array(datasetSim)
    mSim ,nSim = np.shape(datasetSim)
    VmaxSim    = datasetSim[:,2]  # Vmax at 10m
    DirSim     = datasetSim[:,3]  # Vmax at 10m
    DirSim[DirSim>360] = DirSim[DirSim>360] - 360
    DirSim[DirSim<0] = DirSim[DirSim<0] + 360
    allDate    = datasetSim[:,1]  # Vmax at 10m
    datasetObs = pd.read_csv(inputFileObs,header=None,sep=' ')
    datasetObs = np.array(datasetObs)
    mObs ,nObs = np.shape(datasetObs)
    VmaxObs    = datasetObs[:,0]  # Vmax at 10m
    print("observation data length:",len(VmaxObs)) 
    ### fitting Vmax with extreme value distribution and calculating Vmax in return period 
    VmaxSim = VmaxSim*factor[numF]
    print("factor:",factor[numF],numF)
    numF += 1 
    T = 50
    arg = 1-1/T
    VmaxSimNew = []
    dateNew    = []
    vmaxDict = {}
    yyyyMax = int(int(allDate[0])/1000000)
    VmaxMax = 0
    for i in range(mSim):
        iDate = allDate[i]
        yyyy = int(int(iDate)/1000000)
        #print(yyyy) 
        if yyyy == yyyyMax:
            if VmaxSim[i] > VmaxMax:
                VmaxMax = VmaxSim[i]
                Dir = DirSim[i]
        else:
            VmaxSimNew.append(VmaxMax)
            dateNew.append(yyyyMax)
            vmaxDict[int(yyyyMax)] = {'spd':VmaxMax,'dir':Dir} 
            yyyyMax = int(int(allDate[i])/1000000)
            VmaxMax = VmaxSim[i]
            Dir = DirSim[i]
        if i == mSim-1:
            VmaxSimNew.append(VmaxMax)
            dateNew.append(yyyyMax)
            vmaxDict[int(yyyyMax)] = {'spd':VmaxMax,'dir':Dir}

    #print(vmaxDict)   
 
    VmaxSim = np.array(VmaxSimNew)

    length = 2019-1970
    iDataLine     = np.zeros((length,3))
    iDataLine100m = np.zeros((length,3))
    for i in range(length):
        itKey = i+1970
        if itKey in vmaxDict.keys():
            iDataLine[i,0] = itKey
            iDataLine[i,1] = vmaxDict[itKey]['spd']
            iDataLine[i,2] = vmaxDict[itKey]['dir']
            iDataLine100m[i,0] = itKey
            iDataLine100m[i,1] = vmaxDict[itKey]['spd']*1.32
            iDataLine100m[i,2] = vmaxDict[itKey]['dir']*1.32
        else:
            iDataLine[i,0] = itKey
            iDataLine[i,1] = -999
            iDataLine[i,2] = -999
            iDataLine100m[i,0] = itKey
            iDataLine100m[i,1] = -999
            iDataLine100m[i,2] = -999
    np.savetxt(outputFileName,iDataLine, delimiter = ',', fmt='%s')
    np.savetxt(outputFileName100m,iDataLine100m, delimiter = ',', fmt='%s')

    ## Type I : Gumbel -> st.gumbel_r
    locSim1, scaleSim1 = st.gumbel_r.fit(VmaxSim) 
    locObs1, scaleObs1 = st.gumbel_r.fit(VmaxObs)
    
    VmaxSimGumbel   = st.gumbel_r.ppf(arg,loc=locSim1,scale=scaleSim1)
    VmaxObsGumbel   = st.gumbel_r.ppf(arg,loc=locObs1,scale=scaleObs1)

    iDataLine2[numV,0] = lonSite
    iDataLine2[numV,1] = latSite
    iDataLine2[numV,2] = VmaxSimGumbel
    numV += 1
    
    ErrG  = VmaxSimGumbel  - VmaxObsGumbel 
    ErrG1 = ErrG/VmaxObsGumbel*100
    
    print("Gumbel:","VmaxSim=",VmaxSimGumbel,"VmaxObs=",VmaxObsGumbel,"Err:",ErrG,"m/s",ErrG1,"%")
    SumErrG += abs(ErrG1)


mm = len(totalDict)
mErrG = SumErrG/mm    
print("Gumbel mean err",mErrG,"%")    
np.savetxt(outVmax50a,iDataLine2, delimiter = ' ', fmt='%s')
print("end program:", datetime.datetime.now())

