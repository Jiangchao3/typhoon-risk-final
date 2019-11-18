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
allWeatherStaionInfo = parameter.allWeatherStaionInfo()
caseInfo  = parameter.caseInfo()

for iNum in caseInfo.keys():
    tyNum     = str(caseInfo[iNum]['tyNum'])
    siteName  = str(caseInfo[iNum]['stationID'])
    caseName = 'typhoon'+tyNum+"_in_site"+siteName
    latSite  = allWeatherStaionInfo[siteName]['lat']
    lonSite  = allWeatherStaionInfo[siteName]['lon']

    ### read typhoon key parameter 
    inputFileName= "data_caseTyKeyParameter/"+caseName+"_keyParameters.csv"
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
    outFileName = "data_caseTyKeyParameter/"+siteName+"_"+str(tyNum)+"_Vmax.csv"
    outFile = open(outFileName,'w')
    writerData = csv.writer(outFile,delimiter=',')
    for i in range(0,m):
        iRow = []
        jV10Spd,jV10Dir = georgiou.GeorgiouWindFieldModel(allDeltaP[i],allVT[i],allRmax[i],allTheta[i],allL_ST[i],allAlpha_ST[i])
        print(i,allTyNum[i],allDate[i],"V10Spd and V10Dir ",jV10Spd,jV10Dir)
        iRow.append(str(int(allTyNum[i])).zfill(4))
        iRow.append(allDate[i])
        iRow.append(jV10Spd)
        iRow.append(jV10Dir)
        writerData.writerow(iRow) 
    endtime = datetime.datetime.now()
    print("output file:",outFileName)
print("consume time:",endtime - starttime)
print("end program",datetime.datetime.now())
        
