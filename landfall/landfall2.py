import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from functools import reduce
from shapely.geometry import Polygon, Point, LineString, MultiLineString
from haversine import haversine
import pandas as pd

class typhoonLandfall:
    def __int__(self):
        pass

    def getProfilePoints(self,province,ringNum):
        '''
        获取省份轮廓点
        province:省份拼音，shape文件中的 NAME_1
        ringNum：省份主轮廓代码，shape文件中的 RINGNUM
        例子：Hainan 38
              Guangdong 279
              Fujian 360
              Guangxi 71      
        '''      
        m = Basemap()
        m.readshapefile(r'gadm36_CHN_1','chn',drawbounds=False)
        provinceShape = []
        for info, shape in zip(m.chn_info, m.chn):
            #if info['NAME_1'] == province and info['RINGNUM'] == ringNum:
            if info['NAME_1'] == 'Zhejiang':
                provinceShape = shape
                print(info['RINGNUM'],np.shape(provinceShape))
        return list(zip(*provinceShape))
    

    def getIntersectionPoint(self, x, y, poly):
        if len(x) < 2:
            return False
        line = LineString(zip(x, y))
        intersection = poly.intersection(line)
        if intersection.is_empty:
            return False
        if type(intersection) == MultiLineString:
            return reduce(lambda x, y: x + y, [list(p.coords) for p in intersection])
        elif type(intersection) == LineString:
            return list(intersection.coords)
        return False
    
    def getLandfallPoints(self,data):
        '''
        统计登录的台风
        '''
        gdProfilePoints = self.getProfilePoints('Guangdong',279)
        fjProfilePoints = self.getProfilePoints('Fujian',360)
        gxProfilePoints = self.getProfilePoints('Guangxi',71)
        gdRegionPoly = Polygon(list(zip(*gdProfilePoints))).simplify(0.05)
        fjRegionPoly = Polygon(list(zip(*fjProfilePoints))).simplify(0.05)
        gxRegionPoly = Polygon(list(zip(*gxProfilePoints))).simplify(0.05)
        regionPoly1 = gdRegionPoly.union(fjRegionPoly)
        regionPoly  = regionPoly1.union(gxRegionPoly)
        # 简化完的轮廓可能有些地方会在真实轮廓的外面，需要往里缩一点，不然可能会miss一些台风。
        insidePoly = regionPoly.buffer(-0.05)
        gdInsidePoly = gdRegionPoly.buffer(-0.05)
        landfallPoints = {}
        num = 0
        # data 里是台风的数据
        for tyID in data:
            iLandfallPoint = {}
            tyData = data[tyID]
            lats = tyData['lat']
            lons = tyData['lon']
            intersection = self.getIntersectionPoint(lons,lats,regionPoly)
            if intersection != False and not insidePoly.contains(Point(intersection[0])):
                if gdRegionPoly.contains(Point(intersection[0])):
                    iLandfallPoint['tyID'] = tyID
                    iLandfallPoint['landfallPoint'] = intersection[0]
                    iLandfallPoint['allLats'] = lats
                    iLandfallPoint['allLons'] = lons
                    landfallPoints[str(num)] = iLandfallPoint
                    num += 1
        return landfallPoints
        
    def plotLandfallPoints(self,points,minLat=0,maxLat=70,minLon=90,maxLon=180,figName='landfallPoints.png'):
        lons = points[:,0]
        lats = points[:,1]
        fig = plt.gcf()
        m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat,urcrnrlon=maxLon,urcrnrlat=maxLat)
        m.drawmapboundary(fill_color = 'aqua')
        m.fillcontinents(color = 'grey', lake_color = 'aqua')
        m.drawcoastlines()
        plt.scatter(lons,lats,color='r', alpha=0.2, s=20, marker=".",zorder=10)
        plt.show()
        fig.savefig(figName)
        plt.close
        return None

    def plotTyphoonTracks(self,landfallTy,minLat=0,maxLat=70,minLon=90,maxLon=180,figName='typhoonTracks.png'):
        fig = plt.gcf()
        m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat,urcrnrlon=maxLon,urcrnrlat=maxLat)
        m.drawmapboundary(fill_color = 'aqua')
        m.fillcontinents(color = 'grey', lake_color = 'aqua')
        m.drawcoastlines()
        for i in landfallTy.keys():
            iTy = landfallTy[i]
            iLats = iTy['allLats'] 
            iLons = iTy['allLons'] 
            plt.plot(iLons,iLats,color='r')
        plt.show()
        fig.savefig(figName)
        plt.close
        return None
if __name__ == '__main__': 
    # Read data
    inputFileName = "CMA-STI_BestTrack1970-2018.csv"
    print("reading data from ",inputFileName)
    dataset = pd.read_csv(inputFileName,header=None,sep=',')
    dataset = np.array(dataset)
    m ,n    = np.shape(dataset)
    lats = dataset[:,2]
    lons = dataset[:,3]
    tyID = dataset[:,0]
   
    data  = {}
    idata = {} # empty dictionary
    latTemp = []
    lonTemp = []
    for i in range(m-1):
        tyID1 = tyID[i] 
        tyID2 = tyID[i+1]
        if tyID2==tyID1 :
            latTemp.append(lats[i])
            lonTemp.append(lons[i])
        else:
            latTemp.append(lats[i])
            lonTemp.append(lons[i])
            latTempArr = np.array(latTemp)
            lonTempArr = np.array(lonTemp)
            tyIDKey = str('%04d'%int(tyID1))
            idata['lat'] = latTempArr
            idata['lon'] = lonTempArr
            data[tyIDKey] = idata
            latTemp = []
            lonTemp = []
            idata = {}
   
 
    for tyID in data.keys():
        iTy = data[tyID]
        tyLat = iTy['lat']
        #print(tyID,tyLat[0])
    
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
    landfall = typhoonLandfall()
    landfallTyphoon = landfall.getLandfallPoints(data)
    points = []
    for i in landfallTyphoon.keys():
        iTy = landfallTyphoon[i]
        iPoint = iTy['landfallPoint']
        #print(iPoint)
        points.append(iPoint)
    points = np.array(points)
    print(np.shape(points))
    plot1 = landfall.plotLandfallPoints(points,minLat=15,maxLat=30,minLon=105,maxLon=125,figName='landfallPoints.png')

 
    plot2 = landfall.plotTyphoonTracks(landfallTyphoon,minLat=0,maxLat=70,minLon=90,maxLon=180,figName='typhoonTracks.pdf')




