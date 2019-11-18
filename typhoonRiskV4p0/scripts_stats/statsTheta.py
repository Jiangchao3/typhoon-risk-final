import numpy as np
import scipy.stats as st
from scipy import integrate
import csv
import pandas as pd
import math
from math import sin,radians,cos,asin,sqrt
import matplotlib.pyplot as plt
import datetime
import parameter
from customizeFunction import function as func

"""
This script is used to calculate the Approach Angle(Theta, which clockwise positive from North), fitting and testing the goodness of fitting, final plotting the distribution of Theta.
gaoyy 20190724
"""
print("start program:",datetime.datetime.now())

# seed
np.random.seed(2)
# get parameter
print("getting parameter")
parameter = parameter.SiteInfo()
begYear = parameter.begYear()
endYear = parameter.endYear()
totalYear = endYear-begYear+1
siteName = parameter.name
returnPeriod = parameter.returnPeriod()

# Read data
inputFileName = siteName+str(begYear)+"-"+str(endYear)+".csv"
print("reading data from ",inputFileName)
dataset = pd.read_csv(inputFileName,header=None,sep=',')
dataset = np.array(dataset)
m ,n    = np.shape(dataset)
lats    = dataset[:,2]
lons    = dataset[:,3]
tyNum   = dataset[:,0]

print("calculate Theta")
Theta = []
for i in range(m-1):
    if tyNum[i] != tyNum[i+1]:
        # print("next typhoon")
        continue
    lon1 = lons[i]
    lat1 = lats[i]
    lon2 = lons[i+1]
    lat2 = lats[i+1]
    if lon1==lon2 and lat1==lat2 :
        #print(i)
        continue
    iAzimuth = func.getAzimuth(lon1,lat1,lon2,lat2)
    Theta.append(iAzimuth)
Theta = np.array(Theta)
#print(np.max(Theta),np.min(Theta))

# Fitting Data
ThetaP0 = [] # Part 0, 0-180 deg
ThetaP1 = [] # Part 1, 180-360 deg
mP0 = 0
mP1 = 0
for i in range(len(Theta)):
    if Theta[i] < 180:
        ThetaP0.append(Theta[i])
        mP0 += 1
    else:
        ThetaP1.append(Theta[i])
        mP1 += 1
#print(mP0,mP1)

# parameter of double normal distrubution
a0     = mP0/(mP0+mP1)
mu0    = np.mean(ThetaP0)
sigma0 = np.std(ThetaP0, ddof=1)
mu1    = np.mean(ThetaP1)
sigma1 = np.std(ThetaP1, ddof=1)
print(a0,mu0,sigma0,mu1,sigma1)

def doubleNormalDensity(x,a0=a0,mu0=mu0,sigma0=sigma0,mu1=mu1,sigma1=sigma1):
    # double normal distribution density function
    #a0     = 0.2570888468809074 
    #mu0    = 60.610614246593954 
    #sigma0 = 43.48371317669466 
    #mu1    = 290.30608264938354 
    #sigma1 = 33.24478656956373
   
    arg0 = -0.5*pow(((x-mu0)/sigma0),2)
    arg1 = -0.5*pow(((x-mu1)/sigma1),2)
    A    = a0/math.sqrt(2.0*math.pi)/sigma0
    B    = (1.0-a0)/math.sqrt(2.0*math.pi)/sigma1
    func = A*np.exp(arg0) + B*np.exp(arg1)
    #print(func)
    return func

def getTheta(cdf0):
    """
    give the cdf(0-1), calculate the Theta
    """
    Theta0 = 180.0
    deltaTheta = 20.0
    deltaPN0 = 1
    deltaPN1 = 1
    cdf1, density = integrate.quad(doubleNormalDensity,0,Theta0)
    for i in range(1000): 
        eps = abs(cdf0-cdf1)
        if eps < 0.0001:
            break
        if cdf1>cdf0:
            Theta0 = max(Theta0 - deltaTheta,0)
            deltaPN0 = 1
        else:
            Theta0 = min(Theta0 + deltaTheta,360)
            deltaPN0 = -1
        if deltaPN0 != deltaPN1 :
            deltaTheta = deltaTheta*0.5
            deltaPN1 = deltaPN0
        cdf1,density = integrate.quad(doubleNormalDensity,0,Theta0)
        #print(cdf0,cdf1,Theta0)
    return Theta0

## fitting
print("fitting Theta with double normal distribution")
allCDF    = [] 
sortTheta = sorted(Theta)
for i in range(len(Theta)):
    cdf0 = sortTheta[i]
    bb,density = integrate.quad(doubleNormalDensity,0,cdf0) 
    allCDF.append(bb)
allCDF = np.array(allCDF)
#
cdf2 = []
angleCdf2 = []
for i in range(100):
    icdf2 = (i+1)/100
    iangleCdf2 = getTheta(icdf2)    
    cdf2.append(icdf2)
    angleCdf2.append(iangleCdf2)
cdf2 = np.array(cdf2)
angleCdf2 = np.array(angleCdf2)


fig = plt.gcf()
x = sorted(Theta)
y = np.zeros(len(x))
for i in range(len(x)):
    y[i] = doubleNormalDensity(x[i])
y = y*6000
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.xlabel('Theta')
plt.show()
figName =  siteName+str(returnPeriod)+"YearsTheta.png"
fig.savefig(figName)
plt.close()



print("end program:",datetime.datetime.now())


