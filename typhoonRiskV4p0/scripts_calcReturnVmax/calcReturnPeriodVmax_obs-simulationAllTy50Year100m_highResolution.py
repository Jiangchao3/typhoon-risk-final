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
outVmax50a = "VmaxReturnPeriodAllWindFarm50a100m_highResolution.csv"
numV = 0
iDataLine2 = np.zeros((len(totalDict),3))
for iKey in totalDict.keys():
    ### 
    siteName = totalDict[iKey]['name']
    latSite  = totalDict[iKey]['lat']
    lonSite  = totalDict[iKey]['lon']
   
    print(' ') 
    print('station:',iKey,siteName)
    ### read data 
    inputFileSim = r"./data_Vmax_highResolution/"+iKey+"VmaxFinal100m.csv"
    
    datasetSim = pd.read_csv(inputFileSim,header=None,sep=',')
    datasetSim = np.array(datasetSim)
    mSim ,nSim = np.shape(datasetSim)
    VmaxSim    = datasetSim[:,1]  # Vmax at 10m
    ### fitting Vmax with extreme value distribution and calculating Vmax in return period 
    T = 50
    arg = 1-1/T
    VmaxSimNew = []
    for i in range(mSim):
        if VmaxSim[i] >0:
            VmaxSimNew.append(VmaxSim[i])
    VmaxSim = np.array(VmaxSimNew)
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

