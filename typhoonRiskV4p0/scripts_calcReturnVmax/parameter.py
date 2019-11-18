#!/usr/bin/env python
#coding:utf8

################################################################
# function: this script provides parameters for other programs
# history : 2019.07.25 V1.0
# author  : gaoyuanyong
###############################################################

class SiteInfo:
    def __init__(self):
        pass
    def allWeatherStaionInfo(self):
        dict1 = {'59754':{'lon':110.17,'lat':20.33,'name':u'徐闻'}, \
                 '59663':{'lon':111.97,'lat':21.87,'name':u'阳江'}, \
                 '59488':{'lon':113.58,'lat':22.28,'name':u'珠海'}, \
                 '59317':{'lon':116.30,'lat':23.03,'name':u'惠来'}, \
                 '59318':{'lon':116.58,'lat':23.27,'name':u'潮阳'}, \
                 '59324':{'lon':117.03,'lat':23.43,'name':u'南澳'}, \
                 '59321':{'lon':117.50,'lat':23.70,'name':u'东山'}, \
                 '58941':{'lon':119.50,'lat':25.97,'name':u'长乐'}, \
                 '58944':{'lon':119.78,'lat':25.52,'name':u'平潭'}, \
                 '58938':{'lon':118.98,'lat':25.23,'name':u'秀屿'}, \
                 '58843':{'lon':120.00,'lat':26.88,'name':u'霞浦'}}
        return dict1
    def allWindFarmInfo(self):
        dict2 = {'A1':{'lon':120.44,'lat':26.64,'name':u'宁德霞浦'},          \
                 'B1':{'lon':120.15,'lat':25.88,'name':u'长乐'},              \
                 'C1':{'lon':119.53,'lat':24.24,'name':u'南日岛'},            \
                 'D1':{'lon':118.03,'lat':23.60,'name':u'漳州六鳌'},          \
                 'E1':{'lon':117.29,'lat':23.40,'name':u'南澳'},              \
                 'E2':{'lon':117.63,'lat':23.01,'name':u'粤东近海深水场址6'}, \
                 'E3':{'lon':118.06,'lat':22.52,'name':u'粤东近海深水场址6'}, \
                 'F1':{'lon':116.23,'lat':22.66,'name':u'甲子'},    \
                 'F2':{'lon':116.33,'lat':22.29,'name':u'粤东近海深水场址2'}, \
                 'G1':{'lon':113.73,'lat':22.12,'name':u'珠海桂山'},          \
                 'H1':{'lon':112.20,'lat':21.48,'name':u'阳江帆石一'},        \
                 'H2':{'lon':112.23,'lat':21.05,'name':u'阳江帆石二'},        \
                 'I1':{'lon':110.55,'lat':20.54,'name':u'外罗'}}
        return dict2
    def specialWindFarmInfo(self): # 要求分析的9点
        dict3 = {'A1':{'lon':120.44,'lat':26.64,'name':u'宁德霞浦'},          \
                 'B1':{'lon':120.15,'lat':25.88,'name':u'长乐'},              \
                 'C1':{'lon':119.53,'lat':24.24,'name':u'南日岛'},            \
                 'D1':{'lon':118.03,'lat':23.60,'name':u'漳州六鳌'},          \
                 'E1':{'lon':117.29,'lat':23.40,'name':u'南澳'},              \
                 'F1':{'lon':116.23,'lat':22.66,'name':u'甲子'},    \
                 'G1':{'lon':113.73,'lat':22.12,'name':u'珠海桂山'},          \
                 'H1':{'lon':112.20,'lat':21.48,'name':u'阳江帆石一'},        \
                 'I1':{'lon':110.55,'lat':20.54,'name':u'外罗'}}
        return dict3
    def caseInfo(self):
        dict4 = {1:{'stationID':59663,'tyNum':1816},  \
                 2:{'stationID':59663,'tyNum':1608},  \
                 3:{'stationID':59324,'tyNum':1619},  \
                 4:{'stationID':59324,'tyNum':1716},  \
                 5:{'stationID':59317,'tyNum':1716},  \
                 6:{'stationID':59317,'tyNum':1619},  \
                 7:{'stationID':59488,'tyNum':1608},  \
                 8:{'stationID':59488,'tyNum':1804},  \
                 9:{'stationID':59488,'tyNum':1816},  \
                 10:{'stationID':59754,'tyNum':1804},  \
                 11:{'stationID':59754,'tyNum':1809},  \
                 12:{'stationID':59754,'tyNum':1816}}
        return dict4
    def allObsInfo(self):
        dict1 = {'59754':{'begY':1971,'endY':2015,'name':u'徐闻'}, \
                 '59663':{'begY':1971,'endY':2015,'name':u'阳江'}, \
                 '59488':{'begY':1980,'endY':2015,'name':u'珠海'}, \
                 '59317':{'begY':1971,'endY':2015,'name':u'惠来'}, \
                 '59318':{'begY':1980,'endY':2015,'name':u'潮阳'}, \
                 '59324':{'begY':1971,'endY':2015,'name':u'南澳'}, \
                 '59321':{'begY':1971,'endY':2015,'name':u'东山'}, \
                 '58941':{'begY':1985,'endY':2015,'name':u'长乐'}, \
                 '58944':{'begY':1971,'endY':2015,'name':u'平潭'}, \
                 '58938':{'begY':1992,'endY':2015,'name':u'秀屿'}, \
                 '58843':{'begY':1979,'endY':2015,'name':u'霞浦'}}
        return dict1
    def oneSiteInfo(self):
        dict1 = {'J1':{'lon':110.18,'lat':21.09,'name':'湛江'}}
        return dict1
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
    print("Begain year  :",AA.begYear())
    print("End    year  :",AA.endYear())
    print("Influence radius :",AA.radiusInflu())
    print("return period :",AA.returnPeriod())

