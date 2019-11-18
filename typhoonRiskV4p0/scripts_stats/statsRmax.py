import numpy as np
import scipy.stats as st
import csv
import pandas as pd
from math import sin,radians,cos,asin,sqrt
import matplotlib.pyplot as plt
import datetime
import parameter
"""
This script is used to calculate the Radius of maximum Winds(Rmax), fitting and testing the goodness of fitting, final plotting the distribution of Rmax
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
Pres    = dataset[:,4]
Rmax = []
print("calculate the Rmax with Central Pressure Difference(deltaP)by empirical formula")
for i in range(0,m):
    Rmax_temp =  1119 * (1010-Pres[i])**(-0.805)
    if Rmax_temp >= 8.0 and Rmax_temp <= 100:
        Rmax.append(Rmax_temp)
Rmax = np.array(Rmax)
print('Max and Min Rmax : ',np.max(Rmax),np.min(Rmax))

Var = Rmax
###  nornmal Distrbute ##########################################
print("fitting the VT with Normal distribution")
# Fitting Data 
loc, scale = st.norm.fit(Var)
print('Normal Mu, Sigma:',loc,scale)

# Goodness test
KS_Test=st.kstest(Var,'norm',args=(loc, scale)) 
print('Normal goodness test')
print(KS_Test)

# Monte carlo sample
MonteCarlo = np.random.uniform(0,1,totalYear)
Var_WeibullSamplea = st.norm.ppf(MonteCarlo,loc=loc,scale=scale)

# plot
fig = plt.gcf()
plt.subplot(121)
x= sorted(Var)
y = st.norm.pdf(x,loc,scale)
y = y * 2000
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 110))
plt.xlabel('Rmax km')
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

# plot
plt.subplot(122)
x= sorted(Var)
y = st.lognorm.pdf(x,s=shape,scale=scale,loc=loc)
y = y * 2000
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 110))
plt.xlabel('Rmax km')
plt.ylabel('PDF')
plt.title('Lognormal')
plt.show()
figName = siteName+str(returnPeriod)+"YearsRmax.png"
print("save figure:", figName)
fig.savefig(figName)
plt.close()

print("end program:", datetime.datetime.now())

