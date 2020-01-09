# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.interpolate import griddata 

#图片
plt.figure(figsize=(16,12))
fig = plt.gcf()
plt.rcParams['savefig.dpi'] = 1000 #像素
plt.rcParams['figure.dpi'] = 1000 #分辨率
ax = fig.add_subplot(111)
myfont = mpl.font_manager.FontProperties(fname=r'../chinese_font/simkai.ttf')
# 提取数据
figName = r"Vmax50a100m_highResolution.png"
inputFileName1 = r"VmaxReturnPeriodAllWindFarm50a100m_highResolution.csv"
inputFileName2 = r"VmaxReturnPeriodAllWeatherStation50a100m.csv"
inputFileName3 = r"VmaxReturnPeriodOneSite50a100m.csv"
inputFileName4 = r"VmaxReturnPeriodAllWindFarm50a100m.csv"
dataset1 = pd.read_csv(inputFileName1,header=None,sep=' ')
dataset1 = np.array(dataset1)
m1 ,n1   = np.shape(dataset1)
lons1    = dataset1[:,0]
lats1    = dataset1[:,1]
vmax1    = dataset1[:,2]
dataset2 = pd.read_csv(inputFileName2,header=None,sep=' ')
dataset2 = np.array(dataset2)
m2 ,n2   = np.shape(dataset2)
lons2    = dataset2[:,0]
lats2    = dataset2[:,1]
vmax2    = dataset2[:,2]
dataset3 = pd.read_csv(inputFileName3,header=None,sep=' ')
dataset3 = np.array(dataset3)
m3 ,n3   = np.shape(dataset3)
lons3    = dataset3[:,0]
lats3    = dataset3[:,1]
vmax3    = dataset3[:,2]
dataset4 = pd.read_csv(inputFileName4,header=None,sep=' ')
dataset4 = np.array(dataset4)
m4 ,n4   = np.shape(dataset4)
lons4    = dataset4[:,0]
lats4    = dataset4[:,1]
vmax4    = dataset4[:,2]
lons = np.append(lons1,lons2)
lons = np.append(lons,lons3)
lons = np.append(lons,lons4)
lats = np.append(lats1,lats2)
lats = np.append(lats,lats3)
lats = np.append(lats,lats4)
vmax = np.append(vmax1,vmax2)
vmax = np.append(vmax,vmax3)
vmax = np.append(vmax,vmax4)
m = m1+m2+m3+m4
n = n1+n2+n3+n4
#设置地图边界值
minLon = int(np.min(lons)) - 2
maxLon = int(np.max(lons)) + 2
minLat = int(np.min(lats)) - 2
maxLat = int(np.max(lats)) + 2

#初始化地图
m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat,urcrnrlon=maxLon,urcrnrlat=maxLat,resolution='h')
chn_shp = '../GADM_Shapefile/gadm36_CHN_1'
twn_shp = '../GADM_Shapefile/gadm36_TWN_1'
hkg_shp = '../GADM_Shapefile/gadm36_HKG_1'
mac_shp = '../GADM_Shapefile/gadm36_MAC_1'
m.readshapefile(chn_shp,'chn',drawbounds=True)
m.readshapefile(twn_shp,'twn',drawbounds=True)
m.readshapefile(hkg_shp,'hkg',drawbounds=True)
m.readshapefile(mac_shp,'mac',drawbounds=True)
m.drawcoastlines(linewidth=0.3)

def set_lonlat(_m, lon_list, lat_list, lon_labels, lat_labels, lonlat_size):
    """
    :param _m: Basemap实例
    :param lon_list: 经度 详见Basemap.drawmeridians函数>介绍
    :param lat_list: 纬度 同上
    :param lon_labels: 标注位置 [左, 右, 上, 下] bool值 默认只标注左上待完善 可使用twinx和twiny实现
    :param lat_labels: 同上
    :param lonlat_size: 字体大小
    :return:
    """
    lon_dict = _m.drawmeridians(lon_list, labels=lon_labels, color='none', fontsize=lonlat_size)
    lat_dict = _m.drawparallels(lat_list, labels=lat_labels, color='none', fontsize=lonlat_size)
    lon_list = []
    lat_list = []
    for lon_key in lon_dict.keys():
        try:
            lon_list.append(lon_dict[lon_key][1][0].get_position()[0])
        except:
            continue

    for lat_key in lat_dict.keys():
        try:
            lat_list.append(lat_dict[lat_key][1][0].get_position()[1])
        except:
            continue
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.set_yticks(lat_list)
    ax.set_xticks(lon_list)
    ax.tick_params(labelcolor='none')

parallels = np.arange(minLat,maxLon,2)
meridians = np.arange(minLon,maxLon,2)
set_lonlat(m,meridians,parallels,[0,0,0,1], [1,0,0,0],15)


# 将经纬度点转换为地图映射点
m_lon, m_lat = m(*(lons, lats))

# 生成经纬度的栅格数据
numcols, numrows = 500,500
xi = np.linspace(m_lon.min(), m_lon.max(), numcols)
yi = np.linspace(m_lat.min(), m_lat.max(), numrows)
xi, yi = np.meshgrid(xi, yi)

# 插值
#vi = griddata((m_lon,m_lat),vmax,(xi,yi),method='cubic')
vi = griddata((m_lon,m_lat),vmax,(xi,yi),method='linear')
#vi = griddata((m_lon,m_lat),vmax,(xi,yi),method='nearest')

#m.drawmapboundary(fill_color = 'skyblue', zorder = 1)
con = m.contourf(xi, yi, vi,100,cmap='jet', zorder = 1)
plt.plot(lons1,lats1,'k.',ms=6)
plt.plot(lons2,lats2,'r.',ms=10)
plt.plot(lons3,lats3,'r.',ms=10)
plt.plot(lons4,lats4,'r.',ms=10)
dictSheng = {0:{"name":"海南","lon":109.5,"lat":19.0},
             1:{"name":"台湾","lon":120.5,"lat":23.5}, 
             2:{"name":"广东","lon":111.0,"lat":22.0}, 
             3:{"name":"福建","lon":113.8,"lat":23.8}, 
             4:{"name":"浙江","lon":118.0,"lat":26.0}}
for iKey in dictSheng.keys():
    text = dictSheng[iKey]["name"]
    lonS = dictSheng[iKey]["lon"]
    latS = dictSheng[iKey]["lat"]
    tx,ty = m(lonS,latS) 
    plt.text(tx,ty,text,fontproperties=myfont,fontsize='20')
position=fig.add_axes([0.15, 0.03, 0.72, 0.03])#位置[左,下,右,上]
cb = plt.colorbar(con,cax=position,orientation='horizontal')
cb.ax.tick_params(labelsize=15)
cbTicks = range(36,55,2) # 50a,100m
cb.set_ticks(cbTicks)
plt.show()
fig.savefig(figName)



