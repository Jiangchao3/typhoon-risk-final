#coding=utf-8
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import parameter
from customizeFunction import function as custfunc
from dateutil.parser import parse
import datetime
import re
import time

'''
V2.0 版本，对00，06，12，18时观测资料最大风速的提取中，将前3小时，后2小时的资料中也提取，如针对06时，则将03，04，05，06，07，08时刻的资料提取，将其中的最大风速作为06时的最大风速。
'''

class plotCase:
    def __int__(self):
        pass
    def plotCaseVmaxSpd(self,simFile,obsFile,stationID,tyNum):
        datasetSim = pd.read_csv(simFile,header=None,sep=',')    
        datasetSim = np.array(datasetSim)
        mSim ,nSim = np.shape(datasetSim)
        dateSim    = datasetSim[:,1]
        spdSim     = datasetSim[:,2]
        spdSim     = spdSim*0.85
        dirSim     = datasetSim[:,3]
        datasetObs = pd.read_csv(obsFile,header=None,sep=',')    
        datasetObs = np.array(datasetObs)
        mObs ,nObs = np.shape(datasetObs)
        dateObs    = datasetObs[:,0]
        spdObs     = datasetObs[:,9]
        dirObs     = datasetObs[:,10]
        
        dateCase   = [] # dd-hh
        spdObsCase = []
        spdSimCase = [] 
        for i in range(mSim):
        #for i in range(4,mSim):
            iDateSimInt = int(dateSim[i])
            print(iDateSimInt)
            for j in range(mObs):
                iDateObsSplt = re.split('[-: ]',dateObs[j])
                iDateObsStr = "".join(iDateObsSplt[0:4])
                iDateObsInt = int(iDateObsStr)
                if iDateSimInt == iDateObsInt:
                    iSpdMax = np.max(spdObs[j]) #前3h,后2h
                    spdObsCase.append(iSpdMax)
                    spdSimCase.append(spdSim[i])
                    dd_hh = iDateObsSplt[2]+"-"+iDateObsSplt[3]
                    dateCase.append(dd_hh)
                    print(i,dd_hh,'obsVmax:',spdObs[j],'simVmax:',spdSim[i])
        dateCase   = np.array(dateCase)
        spdObsCase = np.array(spdObsCase)
        spdSimCase = np.array(spdSimCase)
        iX = range(1,len(dateCase)+1)
        # plot
        fig = plt.gcf()
        #plt.rcParams['savefig.dpi'] = 3000 #像素
        #plt.rcParams['figure.dpi'] = 3000 #分辨率
        fontsize = 10
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simkai.ttf',size=fontsize)
        plt.plot(iX, spdObsCase, "bo-",label=u'观测', linewidth=1)
        plt.plot(iX, spdSimCase, "ro-",label=u'模拟', linewidth=1)
        plt.legend(loc='upper left', frameon=False, prop=myfont,fontsize=fontsize)
        plt.xlabel(u'日期(dd-hh)', fontproperties=myfont,fontsize=fontsize)
        plt.ylabel(u'风速(m/s)', fontproperties=myfont,fontsize=fontsize)
        plt.xlim(0,len(dateCase)+2)
        plt.xticks(iX,list(dateCase),rotation=20,fontproperties=myfont,fontsize=fontsize)
        plt.show()
        figName = "caseV2.0/"+str(stationID)+"_"+str(tyNum)+"_VmaxObsSimV2.0.png"
        fig.savefig(figName)
        plt.close()
        return None

    def plotCaseVmaxDir(self,simFile,obsFile,stationID,tyNum):
        datasetSim = pd.read_csv(simFile,header=None,sep=',')    
        datasetSim = np.array(datasetSim)
        mSim ,nSim = np.shape(datasetSim)
        dateSim    = datasetSim[:,1]
        spdSim     = datasetSim[:,2]
        spdSim     = spdSim*0.85
        dirSim     = datasetSim[:,3]
        datasetObs = pd.read_csv(obsFile,header=None,sep=',')    
        datasetObs = np.array(datasetObs)
        mObs ,nObs = np.shape(datasetObs)
        dateObs    = datasetObs[:,0]
        spdObs     = datasetObs[:,9]
        dirObs     = datasetObs[:,10]
        
        dateCase   = [] # dd-hh
        dirObsCase = []
        dirSimCase = [] 
        for i in range(mSim):
        #for i in range(4,mSim):
            iDateSimInt = int(dateSim[i])
            for j in range(mObs):
                iDateObsSplt = re.split('[-: ]',dateObs[j])
                iDateObsStr = "".join(iDateObsSplt[0:4])
                iDateObsInt = int(iDateObsStr)
                if iDateSimInt == iDateObsInt:
                    dirObsCase.append(dirObs[j])
                    dirSimCase.append(dirSim[i])
                    dd_hh = iDateObsSplt[2]+"-"+iDateObsSplt[3]
                    dateCase.append(dd_hh)
                    print(i,dd_hh,'obsDir:',dirObs[j],'simDir:',dirSim[i])
        dateCase   = np.array(dateCase)
        dirObsCase = np.array(dirObsCase)
        dirSimCase = np.array(dirSimCase)
        iX = range(1,len(dateCase)+1)
        # plot
        fig = plt.gcf()
        #plt.rcParams['savefig.dpi'] = 3000 #像素
        #plt.rcParams['figure.dpi'] = 3000 #分辨率
        fontsize = 10
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simkai.ttf',size=fontsize)
        plt.plot(iX, dirObsCase, "bo-",label=u'观测', linewidth=1)
        plt.plot(iX, dirSimCase, "ro-",label=u'模拟', linewidth=1)
        plt.legend(loc='upper left', frameon=False, prop=myfont,fontsize=fontsize)
        plt.xlabel(u'日期(dd-hh)', fontproperties=myfont,fontsize=fontsize)
        plt.ylabel(u'风向(度)', fontproperties=myfont,fontsize=fontsize)
        plt.xlim(0,len(dateCase)+2)
        plt.xticks(iX,list(dateCase),rotation=20,fontproperties=myfont,fontsize=fontsize)
        plt.show()
        figName = "caseV2.0/"+str(stationID)+"_"+str(tyNum)+"_DirObsSimV2.0.png"
        fig.savefig(figName)
        plt.close()
        return None

if __name__ == '__main__':
    # get parameter
    parameter = parameter.SiteInfo()
    caseInfo  = parameter.caseInfo()
    plotCase = plotCase()
    for i in caseInfo.keys():
        tyNum     = caseInfo[i]['tyNum']
        stationID = caseInfo[i]['stationID']
        simFile = r"case_dataV2.0/"+str(stationID)+"_"+str(tyNum)+"_Vmax.csv"
        obsFile = r"obs_data_hours/"+str(stationID)+".csv"
        plt1 = plotCase.plotCaseVmaxSpd(simFile,obsFile,stationID,tyNum)
        plt2 = plotCase.plotCaseVmaxDir(simFile,obsFile,stationID,tyNum)

    
