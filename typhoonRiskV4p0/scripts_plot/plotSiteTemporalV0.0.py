#coding=utf-8
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import parameter
from customizeFunction import function as custfunc
from windrose import WindroseAxes
from matplotlib.ticker import FuncFormatter

class plotTemporalSpatial:
    def __int__(self):
        pass 
    def plotSiteInterannualVariability(self,dictSiteInfo,begYear,endYear,trendline=True):
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simkai.ttf')
        for iKey in dictSiteInfo.keys():
            fig = plt.gcf()
            plt.rcParams['savefig.dpi'] = 3000 #像素
            plt.rcParams['figure.dpi'] = 3000 #分辨率
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"   
            print("reading data from ",inputFileName) 
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            tcNum    = dataset[:,0]
            date     = dataset[:,1]
            tcNumNew = []
            dateNew  = []
            for i in range(m): #去重
                if tcNum[i] not in tcNumNew:
                    tcNumNew.append(tcNum[i])
                    dateNew.append(date[i])
            # x dim
            iX = range(begYear,endYear+1)
            # y dim
            yDict  = {}
            for i in range(len(dateNew)):
                dateSplt = list(str(dateNew[i]))
                sYYYY = "".join(dateSplt[0:4]) # strYear
                if sYYYY in yDict.keys():
                    num = yDict[sYYYY]+1
                    yDict[sYYYY] = num
                else:
                    yDict[sYYYY] = 1 
            for i in range(len(iX)):
                iYYYY = iX[i] # integerYear
                if str(iYYYY) in yDict.keys():
                    pass
                else:
                    yDict[str(iYYYY)] = 0
            iY = []
            for i in range(len(iX)):
                sYYYY = str(iX[i])
                iY.append(yDict[sYYYY])
            # iStationInfo
            #iStationInfo = dictSiteInfo[iKey]['name']+":"+iKey
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name']
            # plot
            fontsize = 15
            plt.plot(iX, iY, "bo-",label=u'年际变化', linewidth=1)
            if trendline: #趋势线
                parameter = np.polyfit(iX, iY, 1) # n=1为一次函数，返回函数参数
                f = np.poly1d(parameter) # 拼接方程
                plt.plot(iX, f(iX),"r--",label=u"趋势线",linewidth=1)
            plt.legend(loc='upper right', frameon=False, prop=myfont,fontsize=fontsize)
            plt.text(iX[2],9,iStationInfo,fontproperties=myfont,fontsize=fontsize)
            plt.xlabel(u'年份', fontproperties=myfont,fontsize=fontsize)
            plt.ylabel(u'频数(个)', fontproperties=myfont,fontsize=fontsize)
            plt.ylim(-1,10)
            # save fig
            figName = "picture2/InterannualVariability/"+iKey+"_InterannualVariability.png"
            fig.savefig(figName)
            plt.close()
        return None

    def plotSiteInterannualVariabilitySubplot(self,dictSiteInfo,begYear,endYear,trendline=True):
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=5)
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 3000 #像素
        plt.rcParams['figure.dpi'] = 3000 #分辨率
        figNum = 0
        for iKey in dictSiteInfo.keys():
            figNum += 1
            ax = plt.subplot(3,3,figNum)
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"   
            print("reading data from ",inputFileName) 
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            tcNum    = dataset[:,0]
            date     = dataset[:,1]
            tcNumNew = []
            dateNew  = []
            for i in range(m): #去重
                if tcNum[i] not in tcNumNew:
                    tcNumNew.append(tcNum[i])
                    dateNew.append(date[i])
            # x dim
            iX = range(begYear,endYear+1)
            # y dim
            yDict  = {}
            for i in range(len(dateNew)):
                dateSplt = list(str(dateNew[i]))
                sYYYY = "".join(dateSplt[0:4]) # strYear
                if sYYYY in yDict.keys():
                    num = yDict[sYYYY]+1
                    yDict[sYYYY] = num
                else:
                    yDict[sYYYY] = 1 
            for i in range(len(iX)):
                iYYYY = iX[i] # integerYear
                if str(iYYYY) in yDict.keys():
                    pass
                else:
                    yDict[str(iYYYY)] = 0
            iY = []
            for i in range(len(iX)):
                sYYYY = str(iX[i])
                iY.append(yDict[sYYYY])
            # iStationInfo
            #iStationInfo = dictSiteInfo[iKey]['name']+":"+iKey
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name']
            # plot
            fontsize=6
            plt.plot(iX, iY, "bo-",label=u'年际变化', linewidth=0.5,ms=0.8)
            if trendline: #趋势线
                parameter = np.polyfit(iX, iY, 1) # n=1为一次函数，返回函数参数
                f = np.poly1d(parameter) # 拼接方程
                plt.plot(iX, f(iX),"r--",label=u"趋势线",linewidth=0.5)
            #plt.legend(loc='upper right', frameon=False, prop=myfont,fontsize=3)
            ax.legend(loc='upper right', frameon=False, prop=myfont,fontsize=3)
            plt.text(iX[2],9,iStationInfo,fontproperties=myfont,fontsize=fontsize)
            plt.xlabel(u'年份', fontproperties=myfont,fontsize=fontsize)
            plt.ylabel(u'频数(个)',fontproperties=myfont,fontsize=fontsize)
            plt.ylim(-1,10)
            plt.xticks(range(begYear,endYear+3,10),fontsize=5)
            plt.yticks(range(0,10,2),fontsize=5)
        # save fig
        plt.show()
        figName = "picture2/InterannualVariability/"+"allInterannualVariability.png"
        fig.savefig(figName) 
        plt.close()
        return None

    def plotSiteSeasonalVariability(self,dictSiteInfo,begYear,endYear):
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simkai.ttf')
        maker = ['-o','-D','-s','-*','-d','-v','-+','-x','-^','-<','->','-p','-h']
        mIdx  = 0
        for iKey in dictSiteInfo.keys():
            fig = plt.gcf()
            plt.rcParams['savefig.dpi'] = 3000 #像素
            plt.rcParams['figure.dpi'] = 3000 #分辨率
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"   
            print("reading data from ",inputFileName) 
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            tcNum    = dataset[:,0]
            date     = dataset[:,1]
            tcNumNew = []
            dateNew  = []
            for i in range(m): #去重
                if tcNum[i] not in tcNumNew:
                    tcNumNew.append(tcNum[i])
                    dateNew.append(date[i])
            # x dim
            iX = range(1,12+1)
            # y dim
            yDict  = {}
            for i in range(len(dateNew)):
                dateSplt = list(str(dateNew[i]))
                sMM = "".join(dateSplt[4:6]) # str Month
                if sMM in yDict.keys():
                    num = yDict[sMM]+1
                    yDict[sMM] = num
                else:
                    yDict[sMM] = 1 
            for i in range(len(iX)):
                sMM0 = str(iX[i]) # 
                sMM  = sMM0.zfill(2)
                if sMM in yDict.keys():
                    pass
                else:
                    yDict[sMM] = 0
            iY = []
            for i in range(len(iX)):
                sMM0 = str(iX[i])
                sMM  = sMM0.zfill(2)
                iY.append(yDict[sMM])
            # iStationInfo
            #iStationInfo = dictSiteInfo[iKey]['name']+":"+iKey
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name']
            # plot
            fontsize = 15
            plt.plot(iX, iY, maker[mIdx],label=iStationInfo, linewidth=1)
            mIdx += 1
            plt.legend(loc='upper left', frameon=False, prop=myfont,fontsize=fontsize)
            plt.xlabel(u'月份', fontproperties=myfont,fontsize=fontsize)
            plt.ylabel(u'频数(个)', fontproperties=myfont,fontsize=fontsize)
            plt.xticks(iX)
            #plt.ylim(-1,10)
        # save fig
        figName = "picture2/SeasonalVariability/"+"allStationSeasonalVariability.png"
        fig.savefig(figName)
        plt.close()
        return None
    def plotSiteIntensitySpatialDistribution(self,dictSiteInfo,begYear,endYear,minLat=0,maxLat=70, \
          minLon=90,maxLon=180,figName='SiteIntensitySpatailDistribution.png'):
        allData = {}  # {'site':{'tyNum':{'lat':21,'lon':120,'grade':2}...}...}
        for iKey in dictSiteInfo.keys():
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"
            print("reading data from ",inputFileName)
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            iTyNums  = dataset[:,0]
            iDate    = dataset[:,1]
            iLats    = dataset[:,2]
            iLons    = dataset[:,3]
            iGrades  = dataset[:,5]
            allData[iKey] = {}
            for i in range(m):
                tyNum = iTyNums[i]
                #对于某个台风过程影响某一站点，只从整个台风记录中选取最靠近站点的相应记录
                if tyNum not in allData[iKey].keys():
                    #第一次出现直接写入，防止台风记录只有一条时会遗漏
                    allData[iKey][tyNum] = {'lat':iLats[i],'lon':iLons[i],'grade':iGrades[i],'date':iDate[i]} 
                else:
                    latSite  = dictSiteInfo[iKey]['lat'] 
                    lonSite  = dictSiteInfo[iKey]['lon']
                    latTyPre = allData[iKey][tyNum]['lat']
                    lonTyPre = allData[iKey][tyNum]['lon']
                    latTyNow = iLats[i]
                    lonTyNow = iLons[i]
                    distSiteTyPre = custfunc.SphereDistance(lonSite,latSite,lonTyPre,latTyPre) 
                    distSiteTyNow = custfunc.SphereDistance(lonSite,latSite,lonTyNow,latTyNow) 
                    if distSiteTyNow < distSiteTyPre:
                        allData[iKey].update({tyNum:{'lat':iLats[i],'lon':iLons[i],'grade':iGrades[i],'date':iDate[i]}})
        chinesFontSize = 6
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=chinesFontSize)
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 3000 #像素
        plt.rcParams['figure.dpi'] = 3000 #分辨率
        m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat,urcrnrlon=maxLon,urcrnrlat=maxLat,resolution='h')
        m.drawcoastlines(linewidth=0.3)
        #m.drawcountries(linewidth=0.3),此命令香港会有一个方框
        #m.drawrivers(linewidth=0.3)
        chn_shp = './GADM_Shapefile/gadm36_CHN_1'
        twn_shp = './GADM_Shapefile/gadm36_TWN_1'
        hkg_shp = './GADM_Shapefile/gadm36_HKG_1'
        mac_shp = './GADM_Shapefile/gadm36_MAC_1'
        m.readshapefile(chn_shp,'chn',drawbounds=True)
        m.readshapefile(twn_shp,'twn',drawbounds=True)
        m.readshapefile(hkg_shp,'hkg',drawbounds=True)
        m.readshapefile(mac_shp,'mac',drawbounds=True)

        legendIdx = {0:u'低于热带低压',1:u'热带低压(10.8-17.1m/s)',\
                     2:u'热带风暴(17.2-24.4m/s)',3:u'强热带风暴(24.5-32.6m/s)',\
                     4:u'台风(32.7-41.4m/s)',5:u'强台风(41.5-50.9m/s)',\
                     6:u'超强台风(>51.0m/s)',9:u'变性台风'}
        colorIdx = {0:'grey',1:'brown',2:'blue', \
                    3:'green',4:'red',5:'gold',\
                    6:'magenta',9:'purple'}
        firstIdx = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 9:1}
        handlesDict = {} # 收集第一次出现的强度，用于绘制图例
        for iKey in allData.keys():
            iSiteData = allData[iKey]
            for jKey in iSiteData.keys():
                jLat   = iSiteData[jKey]['lat']
                jLon   = iSiteData[jKey]['lon']
                jGrade = iSiteData[jKey]['grade']
                legengColorKey = int(jGrade)
                first = firstIdx[legengColorKey]
                if first != 1 : #强度等级不是第一次出现，绘制
                    plt.scatter(jLon,jLat,s=5, marker="o",\
                      color=colorIdx[legengColorKey])
                else: #强度等级第一次出现，保留以便后面绘制顺便加上图例
                    iHandle = {}
                    iHandle.update({'lon':jLon})
                    iHandle.update({'lat':jLat})
                    iHandle.update({'color':colorIdx[legengColorKey]})
                    iHandle.update({'label':legendIdx[legengColorKey]})
                    handlesDict.update({legengColorKey:iHandle})
                    firstIdx.update({legengColorKey:0})
        #统计每个等级发生的次数
        # 去重:以发生日期和台风编号为唯一索引去重
        deduplicateData = {} # {dateTyNum:{'grade':1,...}
        countGrade = {}  
        for iKey in allData.keys(): # site is key
            siteData = allData[iKey]
            for jKey in siteData.keys(): # tyNum is key
                jDate = siteData[jKey]['date']
                dateTyNum = str(int(jDate))+str(int(jKey))
                if dateTyNum not in deduplicateData:
                    jGrade = int(siteData[jKey]['grade'])
                    deduplicateData[dateTyNum] = {'grade':jGrade}
                    if jGrade in countGrade.keys():
                        numGrades = countGrade[jGrade] + 1
                        countGrade[jGrade] = numGrades
                    else:
                        countGrade[jGrade] = 1
        #print(countGrade)            
        for i in range(10): 
            if i in handlesDict.keys():
                iHandle = handlesDict[i]
                iLon    = iHandle['lon']
                iLat    = iHandle['lat']
                iColor  = iHandle['color']
                iLabel0 = iHandle['label']
                iLabel1 = u' 发生次数:'+str(countGrade[i])
                iLabel  = iLabel0+iLabel1
                plt.scatter(iLon,iLat,color=iColor,\
                    s=5, marker="o",label=iLabel)
        plt.legend(loc='lower right',prop=myfont)
        plt.show()
        fig.savefig(figName)
        plt.close()
        return None

    def plotSiteIntensityFrequencyDistribution(self,dictSiteInfo,begYear,endYear,figName='SiteIntensityFrequencyDistribution.png'):
        allData = {}  # {'site':{'tyNum':{'lat':21,'lon':120,'grade':2}...}...}
        for iKey in dictSiteInfo.keys():
            # read data
            inputFileName="site_data/"+iKey+"_"+str(begYear)+"-"+str(endYear)+".csv"
            print("reading data from ",inputFileName)
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset  = np.array(dataset)
            m ,n     = np.shape(dataset)
            iTyNums  = dataset[:,0]
            iDate    = dataset[:,1]
            iLats    = dataset[:,2]
            iLons    = dataset[:,3]
            iGrades  = dataset[:,5]
            allData[iKey] = {}
            for i in range(m):
                tyNum = iTyNums[i]
                #对于某个台风过程影响某一站点，只从整个台风记录中选取最靠近站点的相应记录
                if tyNum not in allData[iKey].keys():
                    #第一次出现直接写入，防止台风记录只有一条时会遗漏
                    allData[iKey][tyNum] = {'lat':iLats[i],'lon':iLons[i],'grade':iGrades[i],'date':iDate[i]} 
                else:
                    latSite  = dictSiteInfo[iKey]['lat'] 
                    lonSite  = dictSiteInfo[iKey]['lon']
                    latTyPre = allData[iKey][tyNum]['lat']
                    lonTyPre = allData[iKey][tyNum]['lon']
                    latTyNow = iLats[i]
                    lonTyNow = iLons[i]
                    distSiteTyPre = custfunc.SphereDistance(lonSite,latSite,lonTyPre,latTyPre) 
                    distSiteTyNow = custfunc.SphereDistance(lonSite,latSite,lonTyNow,latTyNow) 
                    if distSiteTyNow < distSiteTyPre:
                        allData[iKey].update({tyNum:{'lat':iLats[i],'lon':iLons[i], \
                                                'grade':iGrades[i],'date':iDate[i]}})
        chinesFontSize = 10
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=chinesFontSize)
        fig = plt.gcf()
        fontsize = 10
        plt.rcParams['savefig.dpi'] = 3000 #像素
        plt.rcParams['figure.dpi'] = 3000 #分辨率
        xticks    = range(1,9)
        xtickName = [u'低于热带低压',u'热带低压',u'热带风暴',u'强热带风暴',\
                  u'台风',u'强台风',u'超强台风',u'变性台风']
        countGrade = {} 
        iCountDict = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,9:7}
        iCountArr  = np.zeros(8)
        maker = ['-o','-D','-s','-*','-d','-v','-+','-x','-^']
        mIdx = 0 # makerIndex
        for iKey in allData.keys(): # site is key
            siteData = allData[iKey]
            iCountArr  = np.zeros(8)
            for jKey in siteData.keys(): # tyNum is key
                jGrade = int(siteData[jKey]['grade'])
                index= iCountDict[jGrade]
                iCountArr[index] += 1
            countGrade[iKey] = iCountArr
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name'] 
            plt.plot(xticks,iCountArr,maker[mIdx],label=iStationInfo,linewidth=1.0,ms=5)     
            mIdx += 1   
        plt.legend(loc='upper right', frameon=False, prop=myfont,fontsize=fontsize) 
        plt.ylabel(u'频数(个)', fontproperties=myfont,fontsize=fontsize)
        plt.xticks(xticks,xtickName,rotation=23,fontproperties=myfont,fontsize=fontsize)
        plt.show()
        fig.savefig(figName)
        plt.close()
        return None

class plotVmax:
    def __int__(self):
        pass
    def plotSiteWindRose(self,dictSiteInfo,returnPeriod,figName='siteWindRose.png'):
        fontsize = 12
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=fontsize)
        plt.figure(figsize=(16, 16))
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 2000 #像素
        plt.rcParams['figure.dpi'] = 2000 #分辨率
        
        figNum = 0
        for iKey in dictSiteInfo.keys():
            figNum += 1
            ax = plt.subplot(3,3,figNum,projection='polar')
            # read data 
            inputFileName="vmax_data/"+iKey+"_"+str(returnPeriod)+"YearsVmax.csv"
            print("reading data from ",inputFileName)
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset = np.array(dataset)
            m ,n    = np.shape(dataset)
            wspd    = dataset[:,0] # wind speed
            wdir0   = dataset[:,1] # wind direction
            indexs  = ['<10m/s','10-20m/s','20-30m/s','30-40m/s','>40m/s']
            columns = 'N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW'.split()
            #columns = list(columns)
            N = len(columns) #16个方向
            width   = 360/N # 绘制扇形的宽度
            thetaStd = np.linspace(0,360,N,endpoint=False) #16个方向的角度
            speedStd = np.array([5,15,25,35,45]) 
            spdClass = np.zeros((len(indexs),len(columns)))
            wdir = wdir0 + 180.0
            for i in range(m):
                if wdir[i] >360.0:
                    wdir[i] = wdir[i]-360
                elif wdir[i] <0:
                    wdir[i] = wdir[i]+360
                else:
                    pass
            for i in range(m):
                speedDiff = np.abs(speedStd - wspd[i])
                ix = speedDiff.argmin()
                thetaDiff = np.abs(thetaStd - wdir[i])
                if wdir[i] < 348.75:
                    iy = thetaDiff.argmin()
                else:
                    iy = 0
                spdClass[ix,iy] += 1
            data = pd.DataFrame(spdClass,index=indexs,columns=columns)
            _sum = np.sum(spdClass)
            data = data/_sum # 频数转化为百分比 
            thetaRad = thetaStd*np.pi/180.0
            for idx in data.index:
                # data(即spdClass)的每一行绘制一个扇形 
                radii = data.loc[idx] #每一行数据
                ax.bar(thetaRad,radii,label=idx,tick_label=list(columns))
            #plt.legend(loc=4, bbox_to_anchor=(1.125, -0.125),frameon=False, prop=myfont,fontsize=fontsize)
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda vals, position: '{:.0f}%'.format(100*vals)))
            plt.xticks(fontproperties=myfont,fontsize=fontsize)
            plt.yticks(fontproperties=myfont,fontsize=fontsize)
            title = iKey+":"+dictSiteInfo[iKey]['name']
            plt.title(title,fontproperties=myfont,fontsize=fontsize)
            plt.tight_layout() 
        plt.legend(loc=4, bbox_to_anchor=(1.125, -0.125),frameon=False, prop=myfont,fontsize=fontsize)
        plt.show()
        fig.savefig(figName)
        plt.close()
        return None

    def plotSiteVmaxSeq(self,dictSiteInfo,returnPeriod,figName='allSiteVmaxSeq.png'):
        fontsize = 15
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=fontsize)
        plt.figure(figsize=(16, 16))
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 1000 #像素
        plt.rcParams['figure.dpi'] = 1000 #分辨率
        
        figNum = 0
        for iKey in dictSiteInfo.keys():
            figNum += 1
            ax = plt.subplot(7,2,figNum)
            # read data 
            inputFileName="vmax_data/"+iKey+"_"+str(returnPeriod)+"YearsVmax.csv"
            print("reading data from ",inputFileName)
            dataset  = pd.read_csv(inputFileName,header=None,sep=',')
            dataset = np.array(dataset)
            m ,n    = np.shape(dataset)
            wspd    = dataset[:,0] # wind speed
            #wpsd    = wspd*0.85
            x = range(1,m+1)
            wspdM    = np.zeros(m)
            wspdM[:] = np.sum(wspd)/m
            plt.plot(x,wspd,'b-',label=u'Vmax序列', linewidth=1)
            plt.plot(x,wspdM,'r--',label=u'Vmax均值', linewidth=1)
            plt.legend(loc='upper right', frameon=False, prop=myfont,fontsize=fontsize)
            plt.ylabel(u'Vmax(m/s)', fontproperties=myfont,fontsize=fontsize)
            plt.ylim(0,45)
            plt.xlim(0,200)
            iStationInfo = iKey+":"+dictSiteInfo[iKey]['name']
            plt.text(2,40,iStationInfo,fontproperties=myfont,fontsize=fontsize)
            yTicks = range(0,50,10)
            xTicks = range(0,200,50)
            plt.yticks(yTicks)
            plt.xticks(xTicks)
            plt.show()
        plt.tight_layout()
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
    # plotTemporalSpatial
    plotTemporal = plotTemporalSpatial()   
    #plt0 = plotTemporal.plotSiteInterannualVariability(allWeatherStaionInfo,begYear,endYear)
    #plt1 = plotTemporal.plotSiteSeasonalVariability(allWeatherStaionInfo,begYear,endYear)
    #plt2 = plotTemporal.plotSiteInterannualVariabilitySubplot(specialWindFarmInfo,begYear,endYear)
    #plt3 = plotTemporal.plotSiteSeasonalVariability(specialWindFarmInfo,begYear,endYear)
    #plt4 = plotTemporal.plotSiteIntensitySpatialDistribution(specialWindFarmInfo,begYear,endYear,minLat=16,maxLat=30,minLon=106,maxLon=128,figName='SiteIntensitySpatialDistribution.png')
    #plt5 = plotTemporal.plotSiteIntensityFrequencyDistribution(specialWindFarmInfo,begYear,endYear,figName='SiteIntensityFrequencyDistribution.png')
    # plotVmax
    plotVmax = plotVmax()
    #plt6 = plotVmax.plotSiteWindRose(specialWindFarmInfo,returnPeriod,figName='allWindRose.png')
    plt7 = plotVmax.plotSiteVmaxSeq(allWindFarmInfo,returnPeriod,figName='allWindFarmVmaxSeq.png')
    #plt8 = plotVmax.plotSiteVmaxSeq(allWeatherStaionInfo,returnPeriod,figName='allWeatherStaionVmaxSeq.png')


