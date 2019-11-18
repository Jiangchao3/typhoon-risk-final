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
from decimal import Decimal
import math

class homogenization:
    def __int__(self):
        pass
    def detectHomogen(self,begY,endY,Vmax): #均一性检验
        VmaxO = Vmax[0:endY-begY+1]
        mO    = len(VmaxO)
        F = []
        for i in range(5,mO-5): #滑动计算F,掐头去尾5年,避免子序列过短
            X1 = VmaxO[0:i]
            X2 = VmaxO[i:mO]
            iF = self.calcF(X1,X2)
            F.append(iF)
        F = np.array(F)
        Fmax = np.max(F)
        if Fmax>5:
            #print("F test Ok")
            idx = np.argmax(F)
            idx += 5
            homoYear = begY + idx
            return (homoYear,Fmax) #返回突变年
        else:
            return False
        
    def calcF(self,X1,X2):
        n1 = len(X1)
        n2 = len(X2)
        n = n1+n2
        x1Mean = np.mean(X1)
        x2Mean = np.mean(X2)
        x1VarS = np.sum(np.square(X1-x1Mean)) # 方差
        x2VarS = np.sum(np.square(X2-x2Mean))
        arg0 =  n1*n2/n
        arg0 =  arg0*(x1Mean-x2Mean)**2
        arg1 = x1VarS + x2VarS
        Fvalue = arg0/arg1*(n-2)  # F检验
        return Fvalue
  
    def correctVmax(self,iKey,begY,endY,homoYear,Vmax):
        '''
        homoYear-endY之间订正
        begY-homoYear城市化之前、endY-len(Vmax)台站迁移之后不变
        ''' 
        n1 = homoYear - begY 
        n2 = endY - homoYear+1
        n3 = len(Vmax)-n1-n2
        VmaxB = Vmax[0:n1] # B:Before homoYear
        meanB = np.mean(VmaxB)
        stdB  = np.std(VmaxB)
        VmaxA = Vmax[n1:n1+n2] # A:After homoYear(include)
        VmaxU = VmaxA-meanB
        meanU = np.mean(VmaxU)
        stdU  = np.std(VmaxU)
        n = []
        m = []
        VmaxC = [] # correct
        for i in range(len(VmaxA)):
            iN = 10.0*np.abs(VmaxA[i]-meanB)/stdB+0.5
            iM = 10.0*(VmaxU[i]-meanU)/stdU+0.5
            iN = int(iN)
            iM = int(iM)
            iVmaxC = VmaxA[i]+ (iN*stdB+iM*stdU)/10.0 # C:Correct
            if np.abs(iVmaxC-meanB)>3*stdB:
                if iVmaxC>meanB:
                    iVmaxC = meanB+3*stdB
                else:
                    iVmaxC = meanB-3*stdB
            VmaxC.append(iVmaxC)
        VmaxC = np.array(VmaxC)
        VmaxAll = np.append(list(VmaxB),list(VmaxC))
        if n3>0:
            VmaxHE = list(Vmax[n1+n2:len(Vmax)]) # homeYear-endY
            VmaxAll = np.append(VmaxAll,VmaxHE)
        outputFileName = r"obs_data/"+iKey+"_obs_vmax_correct.csv"
        np.savetxt(outputFileName,VmaxAll, delimiter = ',', fmt='%s') 
        return VmaxAll

if __name__ == '__main__':
    # get parameter
    parameter = parameter.SiteInfo()
    allObsInfo = parameter.allObsInfo()
    homo = homogenization()
    fontsize = 14
    myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=fontsize)
    plt.figure(figsize=(16, 16))
    fig = plt.gcf()
    plt.rcParams['savefig.dpi'] = 800 #像素
    plt.rcParams['figure.dpi'] = 800 #分辨率
    figNum = 0
    for iKey in allObsInfo.keys():   
        figNum += 1
        ax = plt.subplot(6,2,figNum)
        obsFileName=r"obs_data/"+iKey+"_obs_vmax.csv"
        print("reading from",obsFileName)
        dataset  = pd.read_csv(obsFileName,header=None,sep=',')
        dataset  = np.array(dataset)
        m  ,n    = np.shape(dataset)
        Vmax     = dataset[:,0] # wind speed
        begY = allObsInfo[iKey]['begY'] 
        endY = allObsInfo[iKey]['endY'] 
        begY1 = begY
        endY1 = endY
        iX = range(begY,endY+1)
        plt.plot(iX,Vmax,'ro-',label=u'订正前', linewidth=1)
        if iKey == '59754': #徐闻气象站2003年搬迁
            endY1 = 2003 
        if iKey == '59663': #阳江气象站2004年搬迁
            endY1 = 2003
        if iKey == '58941': #长乐气象站2005年搬迁
            endY1 = 2004
        #if iKey == '58843': #霞浦气象站20017年搬迁
        #    endY1 = 2006 
        Ftest = homo.detectHomogen(begY1,endY1,Vmax)
        if Ftest != False:
            print(Ftest[0],Ftest[1])
            homoYear = Ftest[0]
            VmaxC = homo.correctVmax(iKey,begY1,endY1,homoYear,Vmax)
            plt.plot(iX,VmaxC,'bo-',label=u'订正后', linewidth=1)
            VmaxMAX = np.max([np.max(Vmax),np.max(VmaxC)])
            VmaxMin = np.min([np.min(Vmax),np.min(VmaxC)])
            textInfo = u"订正年份:"+str(homoYear)+"-"+str(endY1)
            plt.text(iX[int(len(iX)/2)],VmaxMAX-1,textInfo,fontproperties=myfont,fontsize=fontsize)
        else:
            print("F test failure!!!")
            VmaxMAX = np.max(Vmax)
            VmaxMin = np.min(Vmax)
            textInfo = u"未订正"
            plt.text(iX[int(len(iX)/2)],VmaxMAX-1,textInfo,fontproperties=myfont,fontsize=fontsize)
        plt.ylabel(u'Vmax(m/s)', fontproperties=myfont,fontsize=fontsize) 
        plt.xlabel(u'年份', fontproperties=myfont,fontsize=fontsize) 
        plt.ylim(VmaxMin-2,VmaxMAX+3)
        plt.legend(loc='upper right', frameon=False, prop=myfont,fontsize=fontsize)
        iStationInfo = iKey+":"+allObsInfo[iKey]['name']
        plt.text(iX[0],VmaxMAX-1,iStationInfo,fontproperties=myfont,fontsize=fontsize)
    plt.tight_layout()
    figName = 'allWeatherStationCorrectionObsVmax.png'
    fig.savefig(figName)
    plt.close()



