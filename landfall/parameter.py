#!/usr/bin/env python
#coding:utf8

################################################################
# function: this script provides parameters for other programs
# history : 2019.07.25 V1.0
# author  : gaoyuanyong
###############################################################

class SiteInfo:
    def __init__(self, name="YangJiang",lat=21.52,lon=111.58):
        self.name = name
        self.lat  = lat
        self.lon  = lon
    def begYear(self):
        return 1970
    def endYear(self):
        return 2018
    def radiusInflu(self):
        return 300 
    def returnPeriod(self):
        return 50

if __name__ == '__main__':
    AA =  SiteInfo()
    print("Station name :",AA.name)
    print("Station lat  :",AA.lat)
    print("Station lon  :",AA.lon)
    print("Begain year  :",AA.begYear())
    print("End    year  :",AA.endYear())
    print("Influence radius :",AA.radiusInflu())
    print("return period :",AA.returnPeriod())
