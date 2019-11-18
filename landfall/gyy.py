import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from functools import reduce

# 装个shapely
from shapely.geometry import Polygon, Point, LineString, MultiLineString

# haversine 是用latlon得到km距离的函数
from haversine import haversine

'''
我的台风数据格式是： [ 
                        {
                            'name' : 这是
                            'lat'  : 一个
                            'lon'  : 台风
                            ...
                        } ,
                        { ... }
                    ]
'''


def getHNAcPoints(self):
    m_temp = Basemap()
    m_temp.readshapefile(r'gadm36_CHN_1', 'chn', drawbounds=False)
    hnshape = []
    for info, shape in zip(m_temp.chn_info, m_temp.chn):
        # 这个得自己画一下看看哪个是主轮廓，Name_1==海南的有一些是面积很小的区域，别的地区应该也一样。
        if info['NAME_1'] == 'Hainan' and info['RINGNUM'] == 38:
            hnshape = shape
            break
    return list(zip(*hnshape))


def HN_landfall(self):
    '''
    统计登录的台风
    '''
    HNPoints = self.getHNAcPoints()
    # 两次又zip又list的，好像重复了，你注意一下。。
    reginPoly = Polygon(list(zip(*HNPoints))).simplify(0.05)
    # 简化完的轮廓可能有些地方会在真实轮廓的外面，需要往里缩一点，不然可能会miss一些台风。
    insidePoly = reginPoly.buffer(-0.05)
    # plotbasemap是我自己用basemap画图的函数，替换一下自己的basemap画图就行。
    m = self.plotbasemap([106, 113, 15, 23])
    hitHN = []
    # self.data 里是台风的数据
    for ty in self.data:
        lat, lon = ty['lat'], ty['long']
        intersection = self.getIntersection(lon, lat, reginPoly)
        if intersection != False and not insidePoly.contains(Point(intersection[0])):
            plt.scatter(*intersection[0], color='r',
                        alpha=0.2, s=100, zorder=10)

            hitHN.append({
                'ID': ty['ID'],
                'name': ty['name'],
                'landfall': intersection[0],
                'lat': ty['lat'],
                'lon': ty['lon'],
                'intst': ty['intst'],
                # 根据自己需要记一些别的信息啥的
            })

    plt.show()
    return hitHN

def HNLF(self):
    '''
    这个是按行政区域统计
    '''
    hnlf = self.HN_landfall()
    # 同上，另一个我自己用basemap画图的函数
    m = self.plotbasemapHNLF([107, 113, 17, 23])
    # mainHN在下面给
    count = {dstct: [] for dstct in self.mainHN.keys()}

    for ty in hnlf:
        point = Point(ty['landfall'])
        x = ty['lon']
        y = ty['lat']
        i = 0
        # 找到登陆的那一段，统计方位速度强度
        while i < len(x)-1:
            if LineString([(x[i], y[i]), (x[i+1], y[i+1])]).intersects(point.buffer(0.01)):
                ty.update({'lfDirect': np.arctan2(y[i] - y[i+1], x[i] - x[i+1]) * 180 / np.pi,
                           'lfSpeed': haversine((y[i], x[i]), (y[i+1], x[i+1])) / ty['intvl'],
                           'lfIntst': ty['intst'][i]
                           })
                plt.plot(*zip((point.x, point.y),
                              (x[i], y[i])), color='b', alpha=0.2, linewidth=3)
                break
            i += 1
        
        # 按行政区划统计。
        for district, shape in self.mainHN.items():
            if Polygon(shape).intersects(point.buffer(0.04)):
                plt.scatter(*ty['landfall'], c='r',
                            alpha=0.2, s=100, zorder=10)
                count[district].append([ty['lfIntst'], ty['lfDirect']])
                break
    plt.show()
    print(count)


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



# 附上读取行政区域的一段，记录为self.mainHN
m = Basemap()
m.readshapefile(r'gadm36_CHN_3', 'chn', drawbounds=False)
for info, shape in zip(m.chn_info, m.chn):
    if info['NAME_1'] == 'Hainan' and Polygon(shape).area > 0.01:
        x, y = zip(*shape)
        self.mainHN.update({info['NAME_2']+' '+info['NAME_3']: shape})
        m.plot(x, y, marker=None, linewidth=1, color='black')
