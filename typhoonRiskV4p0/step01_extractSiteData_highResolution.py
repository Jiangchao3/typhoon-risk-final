import  numpy as np
import csv
from math import sin,radians,cos,asin,sqrt
import parameter
from customizeFunction import function as func
import datetime
import json

###############################################################
# Function: Given the influence radius, site latitud and lontitud
#       etc, This script extracts typhoon records that afffects  
#       the site. 
# history : 20190725 V1.0
# author  : gaoyy
###############################################################
print("This script extracts typhoon records thats afffects the site")
print("start program :",datetime.datetime.now())
# get parameter
print("getting parameter")
parameter = parameter.SiteInfo()
begYear = parameter.begYear()
endYear = parameter.endYear()
totalYear = endYear-begYear+1
radiusInflu = parameter.radiusInflu() # influence radius ,unit:KM
fInfo = open('dictInfo.txt', 'r') 
js = fInfo.read()
allSiteInfo = json.loads(js)   
fInfo.close()

for iKey in allSiteInfo.keys():
    siteName = iKey
    latSite  = allSiteInfo[iKey]['lat']
    lonSite  = allSiteInfo[iKey]['lon']
     
    # get best track file name
    fileName = []
    for i in range(begYear,endYear+1):
        iFile = 'CH'+str(i)+'BST.txt'
        fileName.append(iFile)
    
    # get typhoon data
    print("read data and process data")
    allNewLine = []
    for i in range(0,totalYear):
        filePath = 'CMABSTdata1970_2018/' + fileName[i]
        print("Processing File : %s" %filePath )
        fileRead = open(filePath) 
        while True:
            line = fileRead.readline()
            if not line:
                break
    
            if line[0:5] == "66666":
                numberTy = line[20:25] # typhoon numbering
                # print("Skip header recording")
                continue
            
            newLine = ['numberCN', 'yyyymmddhh', 'latRec', \
                       'lonRec', 'presRec','gradeRec']
            if line[8:10] in ["00","06","12","18"]:
                numberTy  = numberTy
                yyymmddhh = line[0:10]
                latRec    = float(line[13:16]) * 0.1 #unit 1.0 degree
                lonRec    = float(line[17:21]) * 0.1
                presRec   = line[22:26]
                gradeRec   = line[11:12]
                newLine[0] = numberTy
                newLine[1] = yyymmddhh
                newLine[2] = str(latRec)
                newLine[3] = str(lonRec)
                newLine[4] = presRec
                newLine[5] = gradeRec
                #if numberTy == "0000":
                if int(numberTy) == 0:
                    continue # Skip nameless TC
                distTy2Site = func.SphereDistance(float(lonRec),float(latRec),lonSite,latSite)
                if distTy2Site > radiusInflu:
                    # Skip outside the scope of influence radius
                    continue 
                else:
                    # print(distTy2Site)
                   pass
                allNewLine.append(newLine)
        fileRead.close
    allNewLineArr = np.array(allNewLine)
    
    # output
    outFileName = "data_site_highResolution/"+siteName+"_"+str(begYear)+"-"+str(endYear)+".csv"
    print("output data : ",outFileName)
    np.savetxt(outFileName, allNewLineArr, delimiter = ',', fmt='%s')
    
print("end program :",datetime.datetime.now())
    
    
    
    
    
    
