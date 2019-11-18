#coding=utf-8
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import landfall3 as landfall
import landfall4 as landfall4
import pandas as pd

class plotTyphoon:
    def __int__(self):
        pass

    def plotLandfallPoints(self,ldTyInfo,minLat=0,maxLat=70, \
          minLon=90,maxLon=180,figName='tyLandfallPoints.png'):
        points = []
        grades = []
        for i in ldTyInfo.keys():
            iTy    = ldTyInfo[i]
            iPoint = iTy['landfallPoint']
            iGrade = iTy['landfallGrade']
            #print(iPoint)
            #print(iGrade)
            points.append(iPoint)
            grades.append(iGrade) 
        points = np.array(points)
        grades = np.array(grades)
        lons = points[:,0]
        lats = points[:,1]
   
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 3000 #像素
        plt.rcParams['figure.dpi'] = 3000 #分辨率
        m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat, \
                    urcrnrlon=maxLon,urcrnrlat=maxLat, \
                    resolution='h')
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
        
        legendIdx = {0:'Weak than TD',1:'TD(10.8-17.1m/s)',\
                   2:'TS(17.2-24.4m/s)',3:'STS(24.5-32.6m/s)',\
                   4:'TY(32.7-41.4m/s)',5:'STY(41.5-50.9m/s)',\
                   6:'SuperTY(>51.0m/s)',9:'Typhoon degeneration'}
        colorIdx = {0:'grey',1:'brown',2:'blue', \
                    3:'green',4:'red',5:'magenta',\
                    6:'purple',9:'yellow'}
        firstIdx = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 9:1}
        handlesDict = {}
        for i in range(len(grades)):
            iKey  = int(grades[i])
            first = firstIdx[iKey]
            if first != 1 :
                plt.scatter(lons[i],lats[i],s=10, marker="o",\
                  color=colorIdx[iKey])
            else: 
                iHandle = {}
                iHandle.update({'iLon':lons[i]})
                iHandle.update({'iLat':lats[i]})
                iHandle.update({'iColor':colorIdx[iKey]})
                iHandle.update({'iLabel':legendIdx[iKey]})
                handlesDict.update({iKey:iHandle})
                firstIdx.update({iKey:0})
        for i in range(10):
            if i in handlesDict.keys():
                iHandle = handlesDict[i]
                iLon    = iHandle['iLon']
                iLat    = iHandle['iLat']
                iColor  = iHandle['iColor']
                iLabel  = iHandle['iLabel']
                plt.scatter(iLon,iLat,color=iColor,\
                    s=10, marker="o",label=iLabel)
        plt.legend(loc='lower left',fontsize='x-small')
        plt.show()
        fig.savefig(figName)
        plt.close()
        return None

    def plotTyphoonTracks(self,ldTyInfo,minLat=0,maxLat=70, \
          minLon=90,maxLon=180,figName='tyLandfallTracks.png'):
        fontsize = 6
        myfont = mpl.font_manager.FontProperties(fname=r'./chinese_font/simhei.ttf',size=fontsize)
        grades = [] #强度等级
        for i in ldTyInfo.keys():
            iTy    = ldTyInfo[i]
            iGrade = iTy['landfallGrade']
            grades.append(iGrade) 
        grades = np.array(grades)
 
        fig = plt.gcf()
        plt.rcParams['savefig.dpi'] = 3000 #像素
        plt.rcParams['figure.dpi'] = 3000 #分辨率
        m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat, \
                    urcrnrlon=maxLon,urcrnrlat=maxLat, \
                    resolution='h')
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
        handlesDict = {}
        countGrade = {}  #统计各强度的次数
        for i in range(len(grades)):
            iTy = ldTyInfo[str(i)]
            iKey  = int(grades[i])
            first = firstIdx[iKey]
            if first != 1 :
                iLons = iTy['allLons']
                iLats = iTy['allLats']
                plt.plot(iLons,iLats,color=colorIdx[iKey], \
                              linewidth=0.5,linestyle='-')
                countGrade[iKey] = countGrade[iKey] + 1
            else: 
                iHandle = {}
                iHandle.update({'iLons':iTy['allLons']})
                iHandle.update({'iLats':iTy['allLats']})
                iHandle.update({'iColor':colorIdx[iKey]})
                iHandle.update({'iLabel':legendIdx[iKey]})
                handlesDict.update({iKey:iHandle})
                firstIdx.update({iKey:0})
                countGrade[iKey] = 1
        for i in range(10):
            if i in handlesDict.keys():
                iHandle = handlesDict[i]
                iLons   = iHandle['iLons']
                iLats   = iHandle['iLats']
                iColor  = iHandle['iColor']
                iLabel0 = iHandle['iLabel']
                iLabel1 = u'发生次数'+str(countGrade[i])
                iLabel  = iLabel0+iLabel1
                plt.plot(iLons,iLats,linewidth=0.5, \
                    linestyle='-',color=iColor,label=iLabel)
        plt.legend(loc='upper right',shadow=True,facecolor='white',frameon=True,prop=myfont,fontsize=fontsize)
        plt.show()
        fig.savefig(figName)
        plt.close()
        return None


if __name__ == '__main__':
    # Read data
    inputFileName = "CMA-STI_BestTrack1970-2018.csv"
    print("reading data from ",inputFileName)
    dataset = pd.read_csv(inputFileName,header=None,sep=',')
    dataset = np.array(dataset)
    m ,n    = np.shape(dataset)
    tyID    = dataset[:,0]
    date    = dataset[:,1]
    lats    = dataset[:,2]
    lons    = dataset[:,3]
    grades  = dataset[:,5]

    data      = {}
    idata     = {} # empty dictionary
    latTemp   = []
    lonTemp   = []
    gradeTemp = []
    dateTemp  = []
    for i in range(m-1):
        tyID1 = tyID[i]
        tyID2 = tyID[i+1]
        if tyID2==tyID1 :
            latTemp.append(lats[i])
            lonTemp.append(lons[i])
            gradeTemp.append(grades[i])
            dateTemp.append(date[i])
        else:
            latTemp.append(lats[i])
            lonTemp.append(lons[i])
            gradeTemp.append(grades[i])
            dateTemp.append(date[i])
            latTempArr = np.array(latTemp)
            lonTempArr = np.array(lonTemp)
            gradeTempArr = np.array(gradeTemp)
            dateTempArr = np.array(dateTemp)
            tyIDKey = str('%04d'%int(tyID1))
            idata['lat']   = latTempArr
            idata['lon']   = lonTempArr
            idata['grade'] = gradeTempArr
            idata['date']  = dateTempArr
            data[tyIDKey]  = idata
            latTemp   = []
            lonTemp   = []
            gradeTemp = []
            dateTemp  = []
            idata     = {}

    '''
    我的台风数据格式是：{ 
                           tyID0:{
                                'lat'  : 一个
                                'lon'  : 台风
                           },
                           tyID1:{ 
                                'lat'  : 另一个
                                'lon'  : 台风
                           },
                           ....
                        }
    '''
    # 实例化
    landfall  = landfall.typhoonLandfall()  
    landfall4 = landfall4.typhoonLandfall()  
    plotTy   = plotTyphoon()
    # 获取登陆信息
    #landfallTyphoon = landfall.getLandfallPoints(data,'Guangdong')
   # ldTyInfo, dstctLfCount = landfall.getLfTyInfo(data,'Guangdong')
    # plot1 绘制登陆点
    #plot1 = plotTy.plotLandfallPoints(ldTyInfo,minLat=18,maxLat=26,minLon=109,maxLon=119,figName='GuangdongTyLfPoints.png')
    # plot2 绘制登陆台风轨迹
    #ldTyInfo, dstctLfCount = landfall.getLfTyInfo(data,'Guangdong')
    #plot2 = plotTy.plotTyphoonTracks(ldTyInfo,minLat=0,maxLat=50,minLon=90,maxLon=170,figName='GuangdongTyLfTracks.png')
    
    #ldTyInfo, dstctLfCount = landfall.getLfTyInfo(data,'Guangdong')
    #plot3 = plotTy.plotTyphoonTracks(ldTyInfo,minLat=0,maxLat=50,minLon=90,maxLon=170,figName='FujianTyLfTracks.png')
    #ldTyInfo, dstctLfCount = landfall.getLfTyInfo(data,'Fujian')
    #plot4 = plotTy.plotTyphoonTracks(ldTyInfo,minLat=0,maxLat=50,minLon=90,maxLon=170,figName='FujianTyLfTracks.png')
    ldTyInfo, dstctLfCount = landfall.getLfTyInfo(data,'China')
    plot5 = plotTy.plotTyphoonTracks(ldTyInfo,minLat=0,maxLat=50,minLon=90,maxLon=170,figName='ChinaTyLfTracks.png')





