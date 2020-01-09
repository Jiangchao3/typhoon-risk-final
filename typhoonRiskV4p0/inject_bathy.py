import numpy as np
from scipy import interpolate
from scipy.interpolate import griddata
from scipy.spatial import cKDTree as KDTree
import netCDF4 as nc4
import shutil
import os
from skimage import measure
import json

def generate_grid(lonMin,lonMax,latMin,latMax,dx):
    """
    input: lonMax,lonMin,latMax,latMin,dx, unit is degree
    output: Simulation grid,numpy array(nx,ny)
    """
    nx = int((lonMax - lonMin)/dx)+1
    ny = int((latMax - latMin)/dx)+1
    #print("nx=",nx,"ny=",ny)
    xi = np.linspace(lonMin,lonMax,nx)
    yi = np.linspace(latMin,latMax,ny)
    gridX,gridY = np.meshgrid(xi, yi)
    return gridX,gridY

def inject_bathymetry(gridX,gridY):
    """
    input: gridX 
    """
    etopoFile = "ETOPO/etopo1_bedrock.nc"
    etopo = nc4.Dataset(etopoFile,'r+')
    lat0  = etopo.variables['lat']
    lon0  = etopo.variables['lon']
    topo0 = etopo.variables['Band1']
    nx = len(lon0); ny = len(lat0)
    lon1,lat1 = np.meshgrid(lon0,lat0)
    lon2  = np.reshape(lon1,(nx*ny,))
    lat2  = np.reshape(lat1,(nx*ny,))
    topo2 = np.reshape(topo0,(nx*ny,))

    #interpMethod = "nearest"
    interpMethod = "linear"
    depth = griddata((lon2,lat2), topo2,(gridX,gridY), method=interpMethod)

    f = nc4.Dataset('depth.nc','w',format='NETCDF4')
    f.createDimension('lon',len(gridX[0,:]))
    f.createDimension('lat',len(gridY[:,0]))
    lonC = f.createVariable("lon",'f4',("lon"))
    latC = f.createVariable("lat",'f4',("lat"))
    depthC = f.createVariable('depth','f8',('lat','lon'))
    lonC.units = 'degrees_east'
    lonC.long_name = 'longitude'
    latC.units = 'degrees_north'
    latC.long_name = 'latitude'
    depthC.units = 'm'
    depthC.long_name = 'depth'
    lonC[:]   = gridX[0,:]
    latC[:]   = gridY[:,0]
    depthC[:,:] = depth
    f.close()

    return depth

if __name__ == '__main__':
    """
    lonMin = 110.1
    lonMax = 120.5
    latMin = 20.3
    latMax = 26.9
    dx     = 0.1
    """
    """
    lonMin = 110.0
    lonMax = 120.5
    latMin = 20.0
    latMax = 27.0
    dx     = 0.5
    """
    lonMin = 110.0
    lonMax = 120.6
    latMin = 20.0
    latMax = 27.0
    dx     = 0.2

    gridX,gridY = generate_grid(lonMin,lonMax,latMin,latMax,dx)
    depth = inject_bathymetry(gridX,gridY)
    depthFile = "depth.nc"
    f     = nc4.Dataset(depthFile,'r+')
    lat   = f.variables['lat']
    lon   = f.variables['lon']
    depth = f.variables['depth']
    ny,nx = np.shape(gridX)
    dictInfo = {}
    iKey = 0
    for i in range(nx):
        for j in range(ny):
            if depth[j,i]<0:
                dictInfo[iKey] = {"lon":gridX[j,i],"lat":gridY[j,i],"name":str(iKey)}    
                iKey += 1
    js   = json.dumps(dictInfo)
    fInfo = open('dictInfo.txt', 'w')
    fInfo.write(js)
    fInfo.close()
    fInfo = open('dictInfo.txt', 'r') 
    js = fInfo.read()
    dictInfo2 = json.loads(js)   
    print(dictInfo2) 
    fInfo.close()
    
    print("sucessful")


