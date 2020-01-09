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
import json

print("start program",datetime.datetime.now())

### getting parameter
print("getting parameters")
parameter    = parameter.SiteInfo()
begYear      = parameter.begYear()
endYear      = parameter.endYear()
totalYear    = endYear-begYear+1
radiusInflu  = parameter.radiusInflu()
returnPeriod = parameter.returnPeriod()
fInfo = open('../dictInfo.txt', 'r')
js = fInfo.read()
allSiteInfo = json.loads(js)
fInfo.close()

totalDict = allSiteInfo
outVmax50a = "VmaxReturnPeriodAllWindFarm50a_highResolution.csv"

numV =0 
iDataLine2 = np.zeros((len(totalDict),3))
for iKey in totalDict.keys():
    ### 
    siteName = totalDict[iKey]['name']
    latSite  = totalDict[iKey]['lat']
    lonSite  = totalDict[iKey]['lon']
   
    print(' ') 
    print('station:',iKey,siteName)
    ### read data 
    inputFileSim = r"../data_allTyphoonSimpleVmax_highResolution/"+iKey+"Vmax.csv"
    
    datasetSim = pd.read_csv(inputFileSim,header=None,sep=',')
    datasetSim = np.array(datasetSim)
    mSim ,nSim = np.shape(datasetSim)
    VmaxSim    = datasetSim[:,2]  # Vmax at 10m
    allDate    = datasetSim[:,1]  # Vmax at 10m
    DirSim     = datasetSim[:,3]  # Vmax at 10m
    DirSim[DirSim>360] = DirSim[DirSim>360] - 360
    DirSim[DirSim<0] = DirSim[DirSim<0] + 360
    ### fitting Vmax with extreme value distribution and calculating Vmax in return period 
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
    outputFileName     = r"./data_Vmax_highResolution/"+iKey+"VmaxFinal.csv"
    outputFileName100m = r"./data_Vmax_highResolution/"+iKey+"VmaxFinal100m.csv"

    np.savetxt(outputFileName,iDataLine, delimiter = ',', fmt='%s')
    np.savetxt(outputFileName100m,iDataLine100m, delimiter = ',', fmt='%s')

    ## Type I : Gumbel -> st.gumbel_r
    locSim1, scaleSim1 = st.gumbel_r.fit(VmaxSim) 
    
    VmaxSimGumbel   = st.gumbel_r.ppf(arg,loc=locSim1,scale=scaleSim1)

    iDataLine2[numV,0] = lonSite
    iDataLine2[numV,1] = latSite
    iDataLine2[numV,2] = VmaxSimGumbel
    numV += 1
    
    
    print("Gumbel:","VmaxSim=",VmaxSimGumbel)


np.savetxt(outVmax50a,iDataLine2, delimiter = ' ', fmt='%s')
print("end program:", datetime.datetime.now())

