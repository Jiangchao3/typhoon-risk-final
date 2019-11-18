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

    def getProfilePoly(self,province):
        '''
        获取省份轮廓点
        province:省份拼音，shape文件中的 NAME_1
        例子：getProfilePoints('Guangdong') 
              getProfilePoints('Fujian') 
        '''     
        m = Basemap()
        m.readshapefile(r'./GADM_Shapefile/gadm36_CHN_1','chn',drawbounds=False)
        m.readshapefile(r'./GADM_Shapefile/gadm36_HKG_0','hk',drawbounds=False)
        m.readshapefile(r'./GADM_Shapefile/gadm36_MAC_0','mac',drawbounds=False)
        #寻找省份的主轮廓,即shape的点数最多（维度最大），也可按面积最大的思路找
        maxShapePoints = 0
        if province not in ['Hongkong','Macao']: #香港澳门特殊处理,只考虑NAME_0
            # 寻找身份主轮廓按shape中维度最大的那个来找，但是对一些岛屿较多的省份比如福建浙江不适用，
            #  最大的主轮廓会将岛屿和陆地之间的海域包括，导致虚假登陆点，无法找到对应的市县级行政区域
            for info, shape in zip(m.chn_info, m.chn):#找到主轮廓对应的维度
                if info['NAME_1'] == province:
                    dim0,dim1 = np.shape(shape)
                    iShapePoints = dim0
                    if iShapePoints > maxShapePoints: 
                        maxShapePoints = iShapePoints
            # 遍历所有区域，将区域大于0.01的添加进去,避免上述问题，2019.09.17 add by gaoyy
            first = 0
            for info, shape in zip(m.chn_info, m.chn):  #
                if info['NAME_1'] == province and Polygon(shape).area > 0.01:
                    dim0,dim1 = np.shape(shape)
                    iShapePoints = dim0
                    if iShapePoints != maxShapePoints : #避免主轮廓加入
                    #if True : #避免主轮廓加入
                        if first == 1:
                            iShapePoly = Polygon(shape)
                            provincePoly = provincePoly.union(iShapePoly)
                        else:
                            provincePoly = Polygon(shape)
                            first = 1
                    else:
                        pass # 主轮廓，跳过
        elif province == 'Hongkong':
            province = 'Hong Kong' # rename according info 
            for info, shape in zip(m.hk_info, m.hk): #找主轮廓
                if info['NAME_0'] == province:
                    dim0,dim1 = np.shape(shape)
                    iShapePoints = dim0
                    if iShapePoints > maxShapePoints: 
                        maxShapePoints = iShapePoints
            for info, shape in zip(m.hk_info, m.hk): #将主轮廓找到并poly
                dim0,dim1 = np.shape(shape)
                iShapePoints = dim0 
                if iShapePoints == maxShapePoints : #只要主轮廓
                    provincePoly = Polygon(shape)
        elif province == 'Macao':
            for info, shape in zip(m.mac_info, m.mac):
                if info['NAME_0'] == province:
                    dim0,dim1 = np.shape(shape)
                    iShapePoints = dim0
                    if iShapePoints > maxShapePoints: 
                        maxShapePoints = iShapePoints
            for info, shape in zip(m.mac_info, m.mac):  #
                dim0,dim1 = np.shape(shape)
                iShapePoints = dim0 
                if iShapePoints == maxShapePoints:
                    provincePoly = Polygon(shape)
        else:
            pass
        #return list(zip(*provinceShape))
        return provincePoly

    def getIntersectionPoint(self,x,y,poly):
        '''
        寻找相交点并返回第一个相交点，即登陆点
        '''
        if len(x) < 2:
            return False
        line = LineString(zip(x, y))
        intersection = poly.intersection(line)
        if intersection.is_empty:
            # 无相交点
            return False
        if type(intersection) == LineString:
            # 只有一个相交点
            return list(intersection.coords)
        elif type(intersection) == MultiLineString:
            # 多个相交点，返回第一个
            return reduce(lambda x, y: x + y, [list(p.coords) for p in intersection])
        return False
    
    def getLandfallPoints(self,tyData,province):
        '''
        统计某个省份台风登陆点，返回的是一个字典，包含台风编号，台风登陆点，整个台风过程的轨迹。
        '''
        # 针对某省设置其沿海邻近省份，统计包含相邻省份在内的登陆台风，再选取目标省份的台风，避免将从相邻省份边界进入的台风误认为登陆台风
        if province == 'Guangdong': 
            allProvinces = ['Guangxi','Guangdong','Fujian','Hongkong','Macao']
        elif province == 'Fujian': 
            allProvinces = ['Guangdong','Fujian','Zhejiang']
        elif province == 'Hainan': 
            allProvinces = ['Hainan']
        elif province == 'Guangxi': 
            allProvinces = ['Guangxi','Guangdong'] # add Vietnam
        elif province == 'Zhejiang': 
            allProvinces = ['Fujian','Zhejiang','Shanghai','Jiangsu']
        elif province == 'Shanghai': 
            allProvinces = ['Zhejiang','Shanghai','Jiangsu']
        elif province == 'Jiangsu': 
            allProvinces = ['Zhejiang','Shanghai','Jiangsu','Shangdong']
        elif province == 'Shangdong': 
            allProvinces = ['Jiangsu','Shangdong']
        elif province == 'Hongkong':
            allProvinces = ['Guangdong','Hongkong','Macao']
        elif province == 'Macao':
            allProvinces = ['Guangdong','Hongkong','Macao']
        elif province == 'GuangdongFujian':
            allProvinces = ['Guangxi','Guangdong','Fujian','Hongkong','Macao','Zhejiang']
        elif province == 'China':
            allProvinces = ['Hainan','Guangxi','Guangdong','Fujian','Hongkong','Macao','Zhejiang','Shanghai','Jiangsu','Shangdong','Liaoning']
        else:
            pass
            # maybe add Taiwan in the future

        allRegionPolyDict = {}
        for iProvince in allProvinces:
            iRegionPoly = self.getProfilePoly(iProvince).simplify(0.05)
            allRegionPolyDict[iProvince] = iRegionPoly
        # 合并沿海各省的poly 
        allRegionPolyUnion = allRegionPolyDict[province]
        for iProvince in allProvinces:
             iRegionPoly = allRegionPolyDict[iProvince]
             allRegionPolyUnion = allRegionPolyUnion.union(iRegionPoly)
        # 简化完的轮廓可能有些地方会在真实轮廓的外面，需要往外buffer一点，不然可能会错过一些台风。
        insidePoly = allRegionPolyUnion.buffer(-0.05)
        targetPoly = allRegionPolyDict[province]
        # 如果是广东，则targetPoly将港澳合并
        if province == 'Guangdong':
            targetPoly = targetPoly.union(allRegionPolyDict['Hongkong'])
            targetPoly = targetPoly.union(allRegionPolyDict['Macao'])
        # 台风登陆点
        landfallPoints = {}
        num = 0
        for tyID in tyData:
            iLandfallPoint = {}
            iTyData = tyData[tyID]
            lats    = iTyData['lat']
            lons    = iTyData['lon']
            grades  = iTyData['grade']
            date    = iTyData['date']
            intersection = self.getIntersectionPoint(lons,lats,allRegionPolyUnion)
            if intersection != False and not insidePoly.contains(Point(intersection[0])):
                #if targetPoly.contains(Point(intersection[0])):
                point = Point(intersection[0])
                if targetPoly.intersects(point.buffer(0.1)):
                    iLandfallPoint['tyID']          = tyID
                    iLandfallPoint['landfallPoint'] = intersection[0]
                    iLandfallPoint['allLats']       = lats
                    iLandfallPoint['allLons']       = lons
                    iLandfallPoint['allGrades']     = grades
                    iLandfallPoint['allDate']       = date
                    landfallPoints[str(num)]        = iLandfallPoint
                    num += 1
        print('Total number of typhoon landfall',province,'is',num)
        return landfallPoints
        
    def getDistricts(self,province):
        '''
        获取某个省份的市县级行政区域划分
        province : 省份名称，例如 'Hainan','Guangdong'
        '''
        districts = {}
        m = Basemap()
        m.readshapefile(r'./GADM_Shapefile/gadm36_CHN_3','chn',drawbounds=False)
        m.readshapefile(r'./GADM_Shapefile/gadm36_HKG_0','hk',drawbounds=False)
        m.readshapefile(r'./GADM_Shapefile/gadm36_MAC_0','mac',drawbounds=False)
        if province != 'Guangdong':
            for info, shape in zip(m.chn_info, m.chn):
                if info['NAME_1'] == province and Polygon(shape).area > 0.01:
                    districts.update({info['NL_NAME_2']+info['NL_NAME_3']: shape}) # 汉字
        elif province == 'Guangdong': #广东特殊处理，将港澳包含
            for info, shape in zip(m.chn_info, m.chn):
                if info['NAME_1'] == province and Polygon(shape).area > 0.01:
                    districts.update({info['NL_NAME_2']+info['NL_NAME_3']: shape}) # 汉字
            #港澳行政区域不进行细分 
            maxShapePoints = 0
            for info, shape in zip(m.hk_info, m.hk):
                if info['NAME_0'] == 'Hong Kong':
                    dim0,dim1 = np.shape(shape)
                    iShapePoints = dim0
                    if iShapePoints > maxShapePoints:
                        maxShapePoints = iShapePoints
                        hkShape = shape
            districts.update({'香港': hkShape})
            maxShapePoints = 0
            for info, shape in zip(m.mac_info, m.mac):
                if info['NAME_0'] == 'Macao':
                    dim0,dim1 = np.shape(shape)
                    iShapePoints = dim0
                    if iShapePoints > maxShapePoints:
                        maxShapePoints = iShapePoints
                        macShape = shape
            districts.update({'澳门': macShape})
        else:
            pass
        return districts

    def getLfTyInfo(self,tyData,province):
        '''
        获取某省份登陆台风信息
        '''
        # 获取台风登陆的经纬度
        landfallPoints = self.getLandfallPoints(tyData,province)
        # 获取省份的行政区域划分，市县（区）级
        districts = self.getDistricts(province)
        # 新建空字典记录台风信息
        tyLfInfo = {}
        # 行政区域空字典，用于记录登陆各市县的台风编号（tyID）
        dstctLfCount = {dstct: [] for dstct in districts.keys()}
        # for循环遍历所有登陆台风并提取信息
        for num in landfallPoints.keys():
            iTy = landfallPoints[num]
            point = Point(iTy['landfallPoint'])
            x = iTy['allLons']
            y = iTy['allLats']
            intvl = 6 #台风数据间隔6h 
            
            # 找到登陆的那一段，提取台风登陆信息
            # 登陆角度，速度，强度，登陆时间
            # for循环遍历一个登陆台风的轨迹，找到登陆点所在的一段
            for i in range(len(x)-1):
                if LineString([(x[i], y[i]), (x[i+1], y[i+1])]).intersects(point.buffer(0.01)):
                    lfDirect = np.arctan2(y[i] - y[i+1], x[i] - x[i+1]) * 180 / np.pi
                    lfSpeed  = haversine((y[i], x[i]), (y[i+1], x[i+1])) / intvl
                    lfGrade  = iTy['allGrades'][i]
                    lfDate   = iTy['allDate'][i]
                    break
            # 按行政区划统计登陆点
            # 遍历所有行政区，找到登录点所在行政区
            for district, shape in districts.items():
                if Polygon(shape).intersects(point.buffer(0.04)):
                    dstctLfCount[district].append(iTy['tyID'])
                    ldDistrict = district
                    break
            # 记录提取到的所有信息
            iTyLfInfo = {} # 子字典，记录一个登陆台风的信息
            iTyLfInfo['tyID']             = iTy['tyID'] 
            iTyLfInfo['landfallPoint']    = iTy['landfallPoint']
            iTyLfInfo['landfallDistrict'] = ldDistrict
            iTyLfInfo['landfallDirction'] = lfDirect  
            iTyLfInfo['landfallSpeed']    = lfSpeed
            iTyLfInfo['landfallGrade']    = lfGrade
            iTyLfInfo['landfallDate']     = lfDate
            iTyLfInfo['allLats']          = iTy['allLats']
            iTyLfInfo['allLons']          = iTy['allLons']
            iTyLfInfo['allGrades']        = iTy['allGrades']
            iTyLfInfo['allDate']          = iTy['allDate']
            tyLfInfo[num] = iTyLfInfo # 子字典添加到父字典
        return (tyLfInfo,dstctLfCount)

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
    landfall = typhoonLandfall()
    #b = landfall.getProfilePoly('Fujian')
    #c = landfall.getDistricts('Fujian')
    ldTyInfo, count = landfall.getLfTyInfo(data,'Shangdong')
