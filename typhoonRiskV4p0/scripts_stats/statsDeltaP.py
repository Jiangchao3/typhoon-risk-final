import numpy as np
import scipy.stats as st
import csv
import pandas as pd
from math import sin,radians,cos,asin,sqrt
import matplotlib.pyplot as plt
import datetime
import parameter

"""
This script is used to calculate the Central Pressure Difference(DeltaP), fitting and testing the goodness of fitting, final plotting the distribution of DeltaP
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

P0 = 1010.0 # hPa, Periphery pressure

# Read data
inputFileName = siteName+str(begYear)+"-"+str(endYear)+".csv"
print("reading data from ",inputFileName)
dataset = pd.read_csv(inputFileName,header=None,sep=',')
dataset = np.array(dataset)
m ,n    = np.shape(dataset)
Pres    = dataset[:,4]

print("calculate deltaP")
deltaP = []
for i in range(0,m):
    deltaP_temp = P0 - Pres[i]
    if deltaP_temp >= 0.0 and deltaP_temp <= 135 :
        deltaP.append(deltaP_temp)
deltaP = np.array(deltaP)
print('Max and Min deltaP : ',np.max(deltaP),np.min(deltaP))

Var = deltaP
###  Weibull Distrbute ##########################################
print("fitting the DeltaP with Weibull(max) distribution")
# Fitting Data 
c, loc, scale = st.weibull_min.fit(Var)

# Goodness test
KS_Test=st.kstest(Var,'weibull_max',args=(c, loc, scale)) 
print(KS_Test)

# Monte carlo sample
MonteCarlo = np.random.uniform(0,1,totalYear)
Var_WeibullSamples = st.weibull_min.ppf(MonteCarlo,c,loc,scale)

# plot
fig = plt.gcf()
plt.subplot(121)
x= sorted(Var)
y = st.norm.pdf(x,loc,scale)
y = y * 2500
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 135))
plt.xlabel('deltaP hPa')
plt.ylabel('PDF')
plt.title('Weibull')

###  LogNormal Distrbute ########################################
print("fitting the DeltaP with Lognormal distribution")
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

#np.savetxt('DeltaP_LognormSamplesYear100.csv', Var_LognormSamples, delimiter = ',')

# plot
plt.subplot(122)
x= sorted(Var)
y = st.lognorm.pdf(x,s=shape,scale=scale,loc=loc)
y = y * 2100
plt.hist(x, bins=40, density=0, facecolor="blue", edgecolor="black", alpha=0.7)
plt.plot(x,y,color='red')
plt.ylim((0, 135))
plt.xlabel('DeltaP hPa')
plt.ylabel('PDF')
plt.title('Lognormal')
plt.show()
figName = siteName+str(returnPeriod)+"YearsDeltaP.png"
fig.savefig(figName)
plt.close()


print("end program:", datetime.datetime.now())

