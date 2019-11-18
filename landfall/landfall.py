import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from functools import reduce
from shapely.geometry import Polygon, Point, LineString, MultiLineString
from haversine import haversine
import pandas as pd

class landfall:
    def __int__(self):
        pass

    def getHNAcPoints(self):
        m_temp = Basemap()
        m_temp.readshapefile(r'gadm36_CHN_1','chn',drawbounds=False)
        hnshape = []
        for info, shape in zip(m_temp.chn_info, m_temp.chn):
            # 这个得自己画一下看看哪个是主轮廓，Name_1==省一级区域，RINGNUM ??
            #if info['NAME_1'] == 'Hainan' :#and info['RINGNUM'] == 38:
            if info['NAME_1'] == 'Guangdong' and info['RINGNUM'] == 279:
            #if info['NAME_1'] == 'Fujian' and info['RINGNUM'] == 360:
                hnshape = shape
                print(info['RINGNUM'],np.shape(hnshape))
        return list(zip(*hnshape))
    
    def getHNAcPoints2(self):
        m_temp = Basemap()
        m_temp.readshapefile(r'gadm36_CHN_1','chn',drawbounds=False)
        hnshape = []
        for info, shape in zip(m_temp.chn_info, m_temp.chn):
            if info['NAME_1'] == 'Fujian' and info['RINGNUM'] == 360:
                hnshape = shape
                print(info['RINGNUM'],np.shape(hnshape))
        return list(zip(*hnshape))

    def getIntersection(self, x, y, poly):
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
    
    def HN_landfall(self,data):
        '''
        统计登录的台风
        '''
        HNPoints = self.getHNAcPoints()
        HNPoints2 = self.getHNAcPoints2()
        # 两次又zip又list的，好像重复了，你注意一下。。
        reginPoly1 = Polygon(list(zip(*HNPoints))).simplify(0.05)
        reginPoly2 = Polygon(list(zip(*HNPoints2))).simplify(0.05)
        reginPoly = reginPoly1.union(reginPoly2)
        # 简化完的轮廓可能有些地方会在真实轮廓的外面，需要往里缩一点，不然可能会miss一些台风。
        insidePoly = reginPoly.buffer(-0.05)
        # plotbasemap是我自己用basemap画图的函数，替换一下自己的basemap画图就行。
        #m = plotbasemap([106, 113, 15, 23])
        fig = plt.gcf()
        m = Basemap(llcrnrlon=105,llcrnrlat=10,urcrnrlon=130,urcrnrlat=35)
        m.drawmapboundary(fill_color = 'aqua')
        #m.fillcontinents(color = 'coral', lake_color = 'aqua')
        m.fillcontinents(color = 'grey', lake_color = 'aqua')
        m.drawcoastlines()
        hitHN = {}
        # data 里是台风的数据
        for tyID in data:
            hitHN_temp = {}
            tyData = data[tyID]
            lat = tyData['lat']
            lon = tyData['lon']
            #print(lat[0],lat[30])
            #print(np.shape(lat))
            intersection = self.getIntersection(lon, lat, reginPoly)
            if intersection != False and not insidePoly.contains(Point(intersection[0])):
                plt.scatter(*intersection[0], color='r', alpha=0.2, s=20, marker=".",zorder=10)
                hitHN_temp['landfall'] = intersection[0]
               # hitHN_temp['lat'] = lat
               # hitHN_temp['lon'] = lon
                hitHN[tyID] = hitHN_temp
    
        plt.show()
        fig.savefig("landfall.png")
        plt.close
        return hitHN

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
    landfall = landfall()
    aa = landfall.HN_landfall(data)
    #print(aa) 
