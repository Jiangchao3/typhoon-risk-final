#!/usr/bin/env python
#coding:utf8

################################################################
# function: this script provides functions for other programs
# history : 2019.07.25 V1.0
# author  : gaoyuanyong
###############################################################
import  numpy as np
import csv
import math
from math import sin,radians,cos,asin,sqrt
import parameter

# function
class function:
    def __int__(self):
        pass

    def SphereDistance(lon1, lat1, lon2, lat2):
        # This function compute the great-circle distance 
        # between (lat1, lon1) and (lat2, lon2) on
        # a sphere with given radius.
        radius = 6371.0 # radius of Earth, unit:KM
        # degree to radians
        lon1, lat1,lon2, lat2 = map(radians,[lon1, lat1,lon2, lat2])
        dlon = lon2 -lon1
        dlat = lat2 -lat1
        arg  = sin(dlat*0.5)**2 +  \
               cos(lat1)*cos(lat2)*sin(dlon*0.5)**2
        dist = 2.0 * radius * asin(sqrt(arg))
        return dist

    def getAzimuth(lon1, lat1, lon2, lat2):
        # This function compute the azimuth from A(lat1, lon1) to
        # B(lat2, lon2) on lats and lons on degree
        lon1, lat1, lon2, lat2 = map(radians,[lon1,lat1,lon2,lat2])
        cosC = cos(90-lat2)*cos(90-lat1) +  \
               sin(90-lat2)*sin(90-lat1)*cos(lon2-lon1)
        sinC = sqrt(1-cosC*cosC)
        if sinC == 0:
            print(lon1, lat1, lon2, lat2)
            sinC = 0.0001
        arg1 = (sin(90-lat2)*sin(lon2-lon1))/sinC
        A = asin(arg1)
        A = A*180/math.pi
        if lat2 >= lat1:
            if lon2 >= lon1:
                Azimuth = A
               # print("1")
            else:
                Azimuth = 360 + A
               # print("2")
        else:
            Azimuth = 180 - A
            #print("3/4")
        return Azimuth


if __name__ == '__main__':
    print("funcion name :","SphereDistance")
    print("funcion name :","getAzimuth")
