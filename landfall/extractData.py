import  numpy as np
import csv
import parameter

###############################################################
# function: extract CMA-STI best track typhoon data and output 
#           typhoon number, date, lat, lon, pressure and grade  
# histary: 2019.07.01 v1.0
#          2019.07.25 V2.0
# anthor : gaoyuanyong
###############################################################
parameter = parameter.SiteInfo()

begYear = parameter.begYear()
endYear = parameter.endYear()
totalYear = endYear - begYear+1

fileName = []
for i in range(begYear,endYear+1):
    iFile = 'CH'+str(i)+'BST.txt'
    fileName.append(iFile)

allNewLine = []
for i in range(0,totalYear):
    filePath = 'CMABSTdata1949_2018/' + fileName[i]
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
        
        newLine = ['numberTy', 'yyyymmddhh', 'latRec',  \
                  'lonRec', 'presRec','gradeRec']
        if line[8:10] in ["00","06","12","18"]:
            numberTy  = numberTy
            yyymmddhh = line[0:10]
            latRec    = float(line[13:16]) * 0.1 #unit 1.0 degree
            lonRec    = float(line[17:21]) * 0.1
            presRec   = line[22:26]
            gradeRec  = line[11:12]
            newLine[0] = numberTy
            newLine[1] = yyymmddhh
            newLine[2] = str(latRec)
            newLine[3] = str(lonRec)
            newLine[4] = presRec
            newLine[5] = gradeRec
            #if numberTy == "0000":
            if int(numberTy) == 0:
                continue #  Skip nameless TC
            allNewLine.append(newLine)
    fileRead.close
    print("")
allNewLineArr = np.array(allNewLine)
#print(allNewLine[0:20])

# output
outFileName = "CMA-STI_BestTrack"+str(begYear)+"-"+ \
                                  str(endYear)+".csv"
np.savetxt(outFileName, allNewLineArr, delimiter = ',', fmt='%s')







