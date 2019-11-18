import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import parameter
from customizeFunction import function as custfunc
from windrose import WindroseAxes
from matplotlib.ticker import FuncFormatter

class plotInfluTotalTime:
    def __int__(self):
        pass
    def plotInfluTotalTime(self,dictSiteInfo,begYear,endYear):
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simkai.ttf')
        maker = ['-o','-D','-s','-*','-d','-v','-+','-x','-^','-<','->','-p','-h']
        #plt.figure(figsize=(12,10)) 
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 2000 #像素
        plt.rcParams['figure.dpi'] = 2000 #分辨率
        mIdx  = 0 # marker index
        for iKey in dictSiteInfo.keys():
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"
            print("reading data from ",inputFileName)
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            tcNum    = dataset[:,0]
            count = {}
            num = 1 # 统计该台风有多少个时间点
            for i in range(1,m): #去重
                if tcNum[i] == tcNum[i-1]: #
                    num += 1   #同一个台风，影响时间点加一
                else: 
                    #首先把这个台风的持续时间记录
                    totalTimes = int(num*6)
                    if totalTimes in count.keys():
                        totalNum = count[totalTimes] + 1
                        count[totalTimes] = totalNum
                    else:
                        count[totalTimes] = 1
                    #下一个台风初始化num
                    num = 1
            print(iKey)
            print(count)
            # plot
            NT  = len(count)
            maxTime = 6*NT
            iX = range(6,maxTime+1,6)
            iY = []
            for it in iX:
                if it in count.keys():
                    totalNum = count[it]
                    iY.append(totalNum)
                else:
                    totalNum = 0
                    iY.append(totalNum)
            iY = np.array(iY)
            
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name']
            fontsize = 15
            plt.plot(iX, iY, maker[mIdx],label=iStationInfo, linewidth=1, ms=3)
            mIdx += 1
        plt.legend(loc='upper right', frameon=False, prop=myfont,fontsize=fontsize)
        plt.xlabel(u'持续时间(小时)', fontproperties=myfont,fontsize=fontsize)
        plt.ylabel(u'影响台风频数(个)', fontproperties=myfont,fontsize=fontsize)
        Xtick = range(12,125,12)
        plt.xticks(Xtick)
        #plt.ylim(-1,10)
        # save fig
        figName = "SiteInfluenceTotalTimesDistribution.png"
        fig.savefig(figName)
        plt.close()
        return None

    def plotInfluTotalTimeCDF(self,dictSiteInfo,begYear,endYear):
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simkai.ttf')
        maker = ['-o','-D','-s','-*','-d','-v','-+','-x','-^','-<','->','-p','-h']
        #plt.figure(figsize=(12,10)) 
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 2000 #像素
        plt.rcParams['figure.dpi'] = 2000 #分辨率
        mIdx  = 0 # marker index
        for iKey in dictSiteInfo.keys():
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"
            print("reading data from ",inputFileName)
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            tcNum    = dataset[:,0]
            count = {}
            num = 1 # 统计该台风有多少个时间点
            for i in range(1,m): #去重
                if tcNum[i] == tcNum[i-1]: #
                    num += 1   #同一个台风，影响时间点加一
                else: 
                    #首先把这个台风的持续时间记录
                    totalTimes = int(num*6)
                    if totalTimes in count.keys():
                        totalNum = count[totalTimes] + 1
                        count[totalTimes] = totalNum
                    else:
                        count[totalTimes] = 1
                    #下一个台风初始化num
                    num = 1
            print(iKey)
            print(count)
            # plot
            NT  = len(count)
            maxTime = 6*NT
            iX = range(6,maxTime+1,6)
            iY = []
            for it in iX:
                if it in count.keys():
                    totalNum = count[it]
                    iY.append(totalNum)
                else:
                    totalNum = 0
                    iY.append(totalNum)
            iY = np.array(iY)
            iCDF = []
            sumY = np.sum(iY)
            for it in range(len(iX)):
                iCDF.append(np.sum(iY[0:it])/sumY)
            iCDF = np.array(iCDF)
            iCDF = iCDF*100
            
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name']
            fontsize = 15
            plt.plot(iX, iCDF, maker[mIdx],label=iStationInfo, linewidth=1, ms=3)
            mIdx += 1
        plt.legend(loc='lower right', frameon=False, prop=myfont,fontsize=fontsize)
        plt.ylabel(u'累计概率(%)', fontproperties=myfont,fontsize=fontsize)
        plt.xlabel(u'持续时间(小时)', fontproperties=myfont,fontsize=fontsize)
        Xtick = range(12,125,12)
        plt.xticks(Xtick)
        #plt.ylim(-1,10)
        # save fig
        figName = "SiteInfluenceTotalTimesCDF.png"
        fig.savefig(figName)
        plt.close()
        return None

if __name__ == '__main__':
    # get parameter
    print("getting parameter")
    parameter = parameter.SiteInfo()
    begYear = parameter.begYear()
    endYear = parameter.endYear()
    totalYear = endYear-begYear+1
    radiusInflu = parameter.radiusInflu() # influence radius ,unit:KM
    returnPeriod = parameter.returnPeriod()
    allWeatherStaionInfo = parameter.allWeatherStaionInfo()
    allWindFarmInfo = parameter.allWindFarmInfo()
    specialWindFarmInfo = parameter.specialWindFarmInfo()

    plotFunc = plotInfluTotalTime()
    #plt1 = plotFunc.plotInfluTotalTime(specialWindFarmInfo,begYear,endYear)    
    plt2 = plotFunc.plotInfluTotalTimeCDF(specialWindFarmInfo,begYear,endYear)   

