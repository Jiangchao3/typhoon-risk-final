import numpy as np
import scipy.stats as st
import csv
import pandas as pd
import math
from math import sin,radians,cos,asin,atan2,sqrt
import matplotlib.pyplot as plt
import datetime
import parameter
from customizeFunction import function as func

"""
This script is used to calculate the Translation Velocity(VT), fitting and testing the goodness of fitting, final plotting the distribution of VT

gaoyy 20190724
"""
print("start program:", datetime.datetime.now())

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
latSite  = parameter.lat # lattitude and longtitude
lonSite  = parameter.lon # of simualtion site
radiusInflu = parameter.radiusInflu() # influence radius ,unit:KM

# Read data
inputFileName = siteName+str(begYear)+"-"+str(endYear)+".csv"
print("reading data from ",inputFileName)
dataset = pd.read_csv(inputFileName,header=None,sep=',')
dataset = np.array(dataset)
m ,n    = np.shape(dataset)
lats    = dataset[:,2]
lons    = dataset[:,3]
tyNum   = dataset[:,0]

print("calculate Dmin")
Dmin = []
for i in range(m-1):
    if tyNum[i] != tyNum[i+1]:
        #print("next typhoon")
        continue
    lon1 = lons[i]
    lat1 = lats[i]
    lon2 = lons[i+1]
    lat2 = lats[i+1]
    if lon1==lon2 and lat1==lat2 :
        #print(i)
        continue
    iTheta0 = func.getAzimuth(lon1,lat1,lon2,lat2)
    iTheta1 = func.getAzimuth(lon1,lat1,lonSite,latSite) 
    iAlpha  = iTheta1 -iTheta0
    if iAlpha < 0 :
        iAlpha = abs(iAlpha)
    if iAlpha > 180:
        iAlpha = iAlpha -180.0
    if iAlpha > 90 :
        iAlpha = 180 - iAlpha
    iAlpha = math.pi*iAlpha/180.0
    iDmin = radiusInflu*sin(iAlpha)
    if iTheta0<iTheta1 :
        iDmin = -1.0*abs(iDmin)
    else:
        iDmin = abs(iDmin)
    Dmin.append(iDmin)
Dmin = np.array(Dmin)
Var = Dmin
###  nornmal Distrbute ##########################################
print("fitting the Dmin with Uniform distribution")
# Fitting Data
loc, scale = st.uniform.fit(Var)
print('Uniform Mu, Sigma:',loc,scale)

# Goodness test
KS_Test=st.kstest(Var,'uniform',args=(loc, scale))
print('Uniform goodness test')
print(KS_Test)


# plot
fig = plt.gcf()
x= sorted(Var)
y = st.uniform.pdf(x,loc,scale)
y = y * 8000
plt.hist(x, bins=40, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 110))
plt.xlabel('Dmin km')
plt.ylabel('PDF')
plt.title('Uniform')
plt.show()
figName = siteName+str(returnPeriod)+"YearsDmin.png"
fig.savefig(figName)
plt.close()
print("end program:", datetime.datetime.now())





