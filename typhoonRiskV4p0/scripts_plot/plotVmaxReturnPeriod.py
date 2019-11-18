# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from scipy.interpolate import griddata 

#图片
plt.figure(figsize=(16,12))
fig = plt.gcf()
plt.rcParams['savefig.dpi'] = 1000 #像素
plt.rcParams['figure.dpi'] = 1000 #分辨率
ax = fig.add_subplot(111)
# 提取数据
#inputFileName = r"Vmax50a24.csv"
#figName = r"Vmax50a24.png"
#inputFileName = r"Vmax50a.csv"
#figName = r"Vmax50a.png"
#inputFileName = r"Vmax50a100m.csv"
#figName = r"Vmax50a100m.png"
#inputFileName = r"Vmax1a.csv"
#figName = r"Vmax1a.png"
inputFileName = r"Vmax1a100m.csv"
figName = r"Vmax1a100m.png"
dataset = pd.read_csv(inputFileName,header=None,sep=' ')
dataset = np.array(dataset)
m ,n    = np.shape(dataset)
lons    = dataset[:,0]
lats    = dataset[:,1]
vmax    = dataset[:,2]
#设置地图边界值
minLon = int(np.min(lons)) - 2
maxLon = int(np.max(lons)) + 2
minLat = int(np.min(lats)) - 2
maxLat = int(np.max(lats)) + 2

#初始化地图
m = Basemap(llcrnrlon=minLon,llcrnrlat=minLat,urcrnrlon=maxLon,urcrnrlat=maxLat,resolution='h')
chn_shp = './GADM_Shapefile/gadm36_CHN_1'
twn_shp = './GADM_Shapefile/gadm36_TWN_1'
hkg_shp = './GADM_Shapefile/gadm36_HKG_1'
mac_shp = './GADM_Shapefile/gadm36_MAC_1'
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

#m.drawmapboundary(fill_color = 'skyblue', zorder = 1)
con = m.contourf(xi, yi, vi,100,cmap='jet', zorder = 1)
plt.plot(lons,lats,'k.',ms=10)
position=fig.add_axes([0.15, 0.05, 0.72, 0.04])#位置[左,下,右,上]
cb = plt.colorbar(con,cax=position,orientation='horizontal')
cb.ax.tick_params(labelsize=15)
#cbTicks = range(15,25,1)
cbTicks = range(21,33,1)
cb.set_ticks(cbTicks)
plt.show()
fig.savefig(figName)



