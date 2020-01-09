This project is about typhoon risk assessment.
(1).process typhoon data
(2).GeogrgiouWindFieldModel
(3).calculate and plot

1.模型使用步骤：
（1）step01_extractSiteData.py提取加密控制点的台风记录（控制点数据从parameter.py读取）
（2）step02_keyParameterAllTyphoon.py计算台风关键参数
（3）step03_WindfiledModel_allTyphoonSimple.py使用台风风场模型计算最大风速和风向
带有_highResolution脚本的脚本是用来计算更多规则加密点，加密点的经纬度信息从dictInfo.txt中读取，dictInfo.txt内含有一个字典，使用inject_bathy脚本生成，引入水深数据去除了陆地点，只加密海洋区域。
2.统计脚本
scripts_stats:包含台风关键参数的统计，使用monte-carlo方法才会用到
3.计算重现期风速
scripts_calcReturnVmax:计算重现期脚本，包含50年1年，10m和100m高度
4.绘图脚本
scripts_plot
6.其他文件夹
data_开头的文件夹是各个步骤存放输出数据的文件夹
chinese_font中文字体
CMABSTdata1970_2018台风最佳路径数据集
ETOPO水深数据
GADM_Shapefile地理信息文件shapefile
obs_观测数据
