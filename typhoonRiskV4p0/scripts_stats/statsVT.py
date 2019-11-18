import numpy as np
import scipy.stats as st
import csv
import pandas as pd
from math import sin,radians,cos,asin,sqrt
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

# Read data
inputFileName = siteName+str(begYear)+"-"+str(endYear)+".csv"
print("reading data from ",inputFileName)
dataset = pd.read_csv(inputFileName,header=None,sep=',')
dataset = np.array(dataset)
m ,n    = np.shape(dataset)
lats  = dataset[:,2]
lons  = dataset[:,3]
tcNum = dataset[:,0]

print("calculate translation velocity(VT)")
VT = []
for i in range(0,m-1):
    if tcNum[i] == tcNum[i+1]:
        dist = func.SphereDistance(lons[i], lats[i], lons[i+1], lats[i+1]) # unit:KM
        VT_temp = dist/6.0   # unit: km/h
        if VT_temp >= 2.0 and VT_temp <= 65 :
            VT.append(VT_temp)
VT = np.array(VT)
print('Max and Min VT : ',np.max(VT),np.min(VT))

Var = VT
###  Normal Distrbution ##########################################
print("fitting the VT with Normal distribution")
# Fitting Data 
loc, scale = st.norm.fit(Var)
Var_NormMu  = loc    # mean
Var_NormStd = scale # standard variation
print('norm Mu and Sigma :',Var_NormMu, Var_NormStd)

# Goodness test
KS_Test=st.kstest(Var,'norm',args=(loc, scale)) 
print('Normal goodness test')
print(KS_Test)

# Monte carlo sample
MonteCarlo = np.random.uniform(0,1,totalYear)
Var_NormSamples = st.norm.ppf(MonteCarlo,loc=loc,scale=scale)


# plot
fig = plt.gcf()
plt.subplot(121)
x= sorted(Var)
y = st.norm.pdf(x,Var_NormMu,Var_NormStd)
y = y * 700
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 50))
plt.xlabel('VT km/h')
plt.ylabel('PDF')
plt.title('Normal')

###  LogNormal Distrbute ########################################
print("fitting the VT with Lognormal distribution")
# Fitting Data 
shape, loc, scale = st.lognorm.fit(Var,floc=0)
Var_LognormMu  = scale #np.exp(scale)    # mean
Var_LognormStd = shape # std
print('Lognorm Mu and Sigma :',Var_LognormMu, Var_LognormStd)

# Goodness test
KS_Test=st.kstest(Var,'lognorm',args=(shape, loc, scale)) 
print('Lognorm goodness test')
print(KS_Test)

# Monte carlo sample
MonteCarlo = np.random.uniform(0,1,totalYear)
Var_LognormSamples = st.lognorm.ppf(MonteCarlo,loc=loc,scale=scale,s=shape)
#np.savetxt('VT_LognormSamplesYear100.csv', Var_LognormSamples, delimiter = ',')

# plot
plt.subplot(122)
x= sorted(Var)
y = st.lognorm.pdf(x,s=shape,scale=scale,loc=loc)
y = y * 600
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 50))
plt.xlabel('VT km/h')
plt.ylabel('PDF')
plt.title('Lognormal')
plt.show()

figName = siteName+str(returnPeriod)+"YearsVT.png"
fig.savefig(figName)
plt.close()

print("end program:", datetime.datetime.now())

