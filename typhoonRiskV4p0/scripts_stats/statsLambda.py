import numpy as np
import scipy.stats as st
import csv
import pandas as pd
from math import sin,radians,cos,asin,sqrt
import matplotlib.pyplot as plt
import datetime
import parameter

############################################################
# This script is used to calculate the annual occurrence rate
# gaoyy 201724
############################################################
print("start program : ",datetime.datetime.now())

# Parameter Setting
print("getting parameter")
parameter    = parameter.SiteInfo()
begYear      = parameter.begYear()
endYear      = parameter.endYear()
totalYear    = endYear-begYear+1
siteName     = parameter.name

# Read data
inputFileName = siteName+str(begYear)+"-"+str(endYear)+".csv"
print("reading data from file :",inputFileName)
dataset = pd.read_csv(inputFileName,header=None,sep=',')
dataset = np.array(dataset)
m ,n    = np.shape(dataset)
tcNum = dataset[:,0]

# stats how many typhooon influence the station duiring 1970-2018
print("calculate annual occurrence rate Lambda")
tcNumNew = []
for element in tcNum :
    if(element not in tcNumNew):
        tcNumNew.append(element)
        element0 = str(int(element))
        element0 = element0.zfill(4)
        # print("typhoon numbering :",element0)
totalNum = np.shape(tcNumNew)

Lambda = totalNum[0]/totalYear
print("total year during 1970-2018 :",totalYear)
print(totalNum[0]," typhoons influence the station during 1970-2018")
print("annual occurrence rate Lambda : ",Lambda)

print("end program : ", datetime.datetime.now())

