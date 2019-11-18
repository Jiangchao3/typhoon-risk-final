############################################################
# read typhoon key parameter and use Georgious windfield model 
# to get the Vmax
# history:2019.08.03
# author : GAO Yuanyong 1471376165@qq.com
# NMEFC 
############################################################
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import pandas as pd
import math
import datetime
import csv
import parameter
import Georgiou
import warnings
warnings.filterwarnings("ignore")

print("start program:",datetime.datetime.now())

# intsance the windfield model
georgiou = Georgiou.Georgiou()
starttime = datetime.datetime.now()

# getting parameter
print("getting parameters")
parameter    = parameter.SiteInfo()
begYear      = parameter.begYear()
endYear      = parameter.endYear()
totalYear    = endYear-begYear+1
radiusInflu  = parameter.radiusInflu()
returnPeriod = parameter.returnPeriod()
dictInfo = parameter.allWeatherStaionInfo()
#dictInfo = parameter.allWindFarmInfo()
deltaT1 = 10
deltaT2 = 5

for iKey in dictInfo.keys():
    ### read typhoon key parameter 
    inputFileName= r"data_allTyKeyParameter/"+iKey+"KeyParameters.csv"
    print("reading data from",inputFileName)
    dataset = pd.read_csv(inputFileName,header=None,sep=',')
    dataset = np.array(dataset)
    m ,n    = np.shape(dataset)
    allTyNum    = dataset[:,0] 
    allDate     = dataset[:,1] 
    allVT       = dataset[:,2] 
    allDeltaP   = dataset[:,3] 
    allRmax     = dataset[:,4] 
    allDmin     = dataset[:,5]
    allL_ST     = dataset[:,6]
    allAlpha_ST = dataset[:,7] 
    allTheta    = dataset[:,8]
   
    ###
    print("simulate the Vmax by Georgious windfield model")
    outFileName = "data_allTyphoonVmax/"+iKey+"Vmax.csv"
    outFile = open(outFileName,'w')
    writerData = csv.writer(outFile,delimiter=',')
    iRow = []
    iV10Spd = [] 
    iV10Dir = []
    # for i = 0
    try:
        jV10Spd,jV10Dir = georgiou.GeorgiouWindFieldModel(allDeltaP[0],allVT[0],allRmax[0],allTheta[0],allL_ST[0],allAlpha_ST[0],deltaT=deltaT1)
    except UnboundLocalError as e:
        print("warning!!!",0,allTyNum[0],allDate[0],"Unstable calculation, set the deltaT = 5 and calculate again")
        try:
            jV10Spd,jV10Dir = georgiou.GeorgiouWindFieldModel(allDeltaP[0],allVT[0],allRmax[0],allTheta[0],allL_ST[0],allAlpha_ST[0],deltaT=deltaT2)
        except UnboundLocalError as e:
            print("warning!!!",0,allTyNum[0],allDate[0],"Unstable calculation, set the Spd and Dir as -999.0")
            jV10Spd = -999.0
            jV10Dir = -999.0
    iV10Spd.append(jV10Spd) 
    iV10Dir.append(jV10Dir)
    for i in range(1,m):
        try:
            jV10Spd,jV10Dir = georgiou.GeorgiouWindFieldModel(allDeltaP[i],allVT[i],allRmax[i],allTheta[i],allL_ST[i],allAlpha_ST[i],deltaT=deltaT1)
        except UnboundLocalError as e:
            print("warning!!!",0,allTyNum[i],allDate[i],"Unstable calculation, set the deltaT = 5 and calculate again") 
            try:
                jV10Spd,jV10Dir = georgiou.GeorgiouWindFieldModel(allDeltaP[i],allVT[i],allRmax[i],allTheta[i],allL_ST[i],allAlpha_ST[i],deltaT=deltaT2)
            except UnboundLocalError as e:
                print("warning!!!",i,allTyNum[i],allDate[i],"Unstable calculation, set the Spd and Dir as -999.0")
                jV10Spd = -999.0
                jV10Dir = -999.0
        if allTyNum[i] == allTyNum[i-1]: #同一个台风，继续添加
            if i != m-1:
                iV10Spd.append(jV10Spd) 
                iV10Dir.append(jV10Dir)
            else:
                iV10Spd.append(jV10Spd) 
                iV10Dir.append(jV10Dir)
                iV10Spd = np.array(iV10Spd)   
                iV10Dir = np.array(iV10Dir)
                idxMax  = np.argmax(iV10Spd)
                iV10SpdMax = iV10Spd[idxMax]
                iV10DirMax = iV10Dir[idxMax]
                iRow.append(str(int(allTyNum[i-1])).zfill(4))
                iRow.append(allDate[i-1])
                iRow.append(iV10SpdMax)
                iRow.append(iV10DirMax)
                writerData.writerow(iRow) 
        else: #下一个台风，先把上一个台风处理
            iV10Spd = np.array(iV10Spd)   
            iV10Dir = np.array(iV10Dir)
            idxMax  = np.argmax(iV10Spd)
            iV10SpdMax = iV10Spd[idxMax]
            iV10DirMax = iV10Dir[idxMax]
            iRow.append(str(int(allTyNum[i-1])).zfill(4))
            iRow.append(allDate[i-1])
            iRow.append(iV10SpdMax)
            iRow.append(iV10DirMax)
            writerData.writerow(iRow) 
            print(i-1,allTyNum[i-1],allDate[i-1],"V10Spd and V10Dir ",iV10SpdMax,iV10DirMax)
            if i != m-1: 
                iRow = []    
                iV10Spd = [] 
                iV10Dir = []
                iV10Spd.append(jV10Spd) 
                iV10Dir.append(jV10Dir)
            else:  # for i = m-1
                iRow = []
                iRow.append(str(int(allTyNum[i])).zfill(4))
                iRow.append(allDate[i])
                iRow.append(jV10Spd)
                iRow.append(jV10Dir)
                writerData.writerow(iRow)
                print(i,allTyNum[i],allDate[i],"V10Spd and V10Dir ",iV10SpdMax,iV10DirMax)

    endtime = datetime.datetime.now()
    print("output file:",outFileName)
print("consume time:",endtime - starttime)
print("end program",datetime.datetime.now())
        
