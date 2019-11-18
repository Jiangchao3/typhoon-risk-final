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
import math
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

work = 2 # 1 or 2 or 3
if work == 1:
    totalDict = allWeatherStationInfo
    outVmax1a = "VmaxReturnPeriodAllWeatherStation1a.csv"
elif work == 2:
    totalDict = allWindFarmInfo
    outVmax1a = "VmaxReturnPeriodAllWindFarm1a.csv"
elif work == 3:
    totalDict = oneSiteInfo
    outVmax1a = "VmaxReturnPeriodOneSite1a.csv"

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
    inputFileSim = r"./data_Vmax/"+iKey+"VmaxFinal.csv"
    if work != 1:
        inputFileObs = r"../obs_data/"+iKey+"_obs_vmax.csv" #obs
    else:
        if iKey in ['59488','59324','59321','58941']:
            inputFileObs = r"../obs_data/"+iKey+"_obs_vmax.csv" #obs
        else:
            inputFileObs = r"../obs_data/"+iKey+"_obs_vmax_correct.csv"
    
    datasetSim = pd.read_csv(inputFileSim,header=None,sep=',')
    datasetSim = np.array(datasetSim)
    mSim ,nSim = np.shape(datasetSim)
    VmaxSim    = datasetSim[:,1]  # Vmax at 10m
    datasetObs = pd.read_csv(inputFileObs,header=None,sep=' ')
    datasetObs = np.array(datasetObs)
    mObs ,nObs = np.shape(datasetObs)
    VmaxObs    = datasetObs[:,0]  # Vmax at 10m
    print("observation data length:",len(VmaxObs)) 
    T = 50
    arg = 1-1/T
    VmaxSimNew = []
    for i in range(mSim):
        if VmaxSim[i] >-0:
            VmaxSimNew.append(VmaxSim[i])
    VmaxSim = np.array(VmaxSimNew)

    ## Type I : Gumbel -> st.gumbel_r
    locSim1, scaleSim1 = st.gumbel_r.fit(VmaxSim) 
    locObs1, scaleObs1 = st.gumbel_r.fit(VmaxObs)
    
    VmaxSim50a   = st.gumbel_r.ppf(arg,loc=locSim1,scale=scaleSim1)
    VmaxObs50a   = st.gumbel_r.ppf(arg,loc=locObs1,scale=scaleObs1)
    VmaxSim1a = (0.36+0.1*math.log(12))*VmaxSim50a
    VmaxObs1a = (0.36+0.1*math.log(12))*VmaxObs50a
   
    iDataLine2[numV,0] = lonSite
    iDataLine2[numV,1] = latSite
    iDataLine2[numV,2] = VmaxSim1a
    numV += 1

    ErrG  = VmaxSim1a  - VmaxObs1a
    ErrG1 = ErrG/VmaxObs1a*100

    print("Gumbel:","VmaxSim=",VmaxSim1a,"VmaxObs=",VmaxObs1a,"Err:",ErrG,"m/s",ErrG1,"%")
    
    SumErrG += abs(ErrG1)


mm = len(totalDict)
mErrG = SumErrG/mm    
print("Gumbel mean err",mErrG,"%")   
np.savetxt(outVmax1a,iDataLine2, delimiter = ' ', fmt='%s') 
print("end program:", datetime.datetime.now())

