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
import GeorgiouSimple
import json

print("start program:",datetime.datetime.now())

# intsance the windfield model
georgiou = GeorgiouSimple.Georgiou()
starttime = datetime.datetime.now()

# getting parameter
print("getting parameters")
parameter    = parameter.SiteInfo()
begYear      = parameter.begYear()
endYear      = parameter.endYear()
totalYear    = endYear-begYear+1
radiusInflu  = parameter.radiusInflu()
returnPeriod = parameter.returnPeriod()
fInfo = open('dictInfo.txt', 'r')
js = fInfo.read()
allSiteInfo = json.loads(js)
dictInfo = allSiteInfo
fInfo.close()

for iKey in dictInfo.keys():
    ### read typhoon key parameter 
    inputFileName= r"data_allTyKeyParameter_highResolution/"+iKey+"KeyParameters.csv"
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
    outFileName = "data_allTyphoonSimpleVmax_highResolution/"+iKey+"Vmax.csv"
    outFile = open(outFileName,'w')
    writerData = csv.writer(outFile,delimiter=',')
    for i in range(m):
        iRow = []
        iV10Spd,iV10Dir = georgiou.GeorgiouWindFieldModel(allDeltaP[i],allVT[i],allRmax[i],allTheta[i],allL_ST[i],allAlpha_ST[i])
        iRow.append(allTyNum[i])
        iRow.append(allDate[i])
        iRow.append(iV10Spd)
        iRow.append(iV10Dir)
        writerData.writerow(iRow)
        print(i,allTyNum[i],allDate[i],iV10Spd,iV10Dir) 
    endtime = datetime.datetime.now()
    print("output file:",outFileName)
print("consume time:",endtime - starttime)
print("end program",datetime.datetime.now())
        
