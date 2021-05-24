'''定义各种故障类型'''

#数据异常类型
X = {'X1': '数据中断(瞬时)', 'X2': '数据中断(长期)', 'X3': '数据重复', 'X4': '数据固定偏移',
     'X5': '数据为零', 'X6': '数据连续增长(降低)', 'X7': '数据跳变', 'X8': '数据抖动', 'X9': '离群点'}
#故障类型
S = {'S1_0.0': '软件故障', 'S2_0.0': '通信中断', 'S3_0.0': '电源故障', 'S4_0.0': '传感器异常',
     'S5_0.0': '外部环境', 'S6_0.0': '装置本体故障', 'S7_0.0': '设备状态变化', 'S8_0.0': '恶劣工况',
     'S9_0.0': '环境干扰', 'S10_0.0': '软件缺陷', 'S11_0.0': '参数错误', 'S12_0.0': '通信质量差',
     'S13_0.0': '模块损坏等', 'S14_0.0': '完全失效', 'S15_0.0': '固定偏移', 'S16_0.0': '灵敏度下降',
     'S17_0.0': '漂移'}

univariate  = {'油中溶解气体':'H2','SF6气体水分':'MOISTURE','SF6气体压力':'PRESSURE20C','避雷器绝缘监测':'TOTALCURRENT',
               '断路器局部放电':'DISCHARGECAPACITY','储能电机工作状态':'CHARGETIME','顶层油温':'OILTEMPERATURE',
               '分合闸线圈电流波形':'ACTION','容性设备绝缘监测':'CAPACITANCE','铁芯接地电流':'TOTALCORECURRENT',
               '微水':'MOISTURE','覆冰监测':'EQUAL_ICETHICKNESS','导线温度监测':'Line_Temperature1','导线舞动':'U_VERTICAL_AMPLITUDE',
               '风偏监测':'Windage_Yaw_Angle','微风振动监测':'Vibration_Amplitude','微气象监测':'Average_WindSpeed',
               '现场污秽度监测':'ESDD','倒置式电流互感器压力监测':'none','SF6气体压力（天山换流站）':'PRESSURE20C',
               '套管压力监测':'none','变压器局部放电':'none','顶层油温（天山换流站）':'OILTEMPERATURE','视频监测':'none',
               '图像监测':'none','微水（天山换流站）':'MOISTURE','避雷器绝缘监测（天山换流站）':'TOTALCURRENT',
               '铁芯接地电流（天山换流站）':'TOTALCORECURRENT','油中溶解气体（天山换流站）':'H2','杆塔倾斜监测':'none'}

newUnivariate  = {'油中溶解气体':'H2','SF6气体水分':'MOISTURE','SF6气体压力':'PRESSURE20C','避雷器绝缘监测':'TOTALCURRENT',
               '断路器局部放电':'DISCHARGECAPACITY','储能电机工作状态':'none','顶层油温':'OILTEMPERATURE',
               '分合闸线圈电流波形':'none','容性设备绝缘监测':'CAPACITANCE','铁芯接地电流':'TotalCoreCurrent',
               '微水':'MOISTURE','覆冰监测':'EQUAL_ICETHICKNESS','导线温度监测':'Line_Temperature1','导线舞动':'none',
               '风偏监测':'none','微风振动监测':'none','微气象监测':'none',
               '现场污秽度监测':'ESDD','倒置式电流互感器压力监测':'none','SF6气体压力（天山换流站）':'PRESSURE20C',
               '套管压力监测':'none','变压器局部放电':'none','顶层油温（天山换流站）':'OILTEMPERATURE','视频监测':'none',
               '图像监测':'none','微水（天山换流站）':'MOISTURE','避雷器绝缘监测（天山换流站）':'TOTALCURRENT',
               '铁芯接地电流（天山换流站）':'TOTALCORECURRENT','油中溶解气体（天山换流站）':'H2','杆塔倾斜监测':'Inclination'}

'''
{'油中溶解气体':'H2','SF6气体水分':'MOISTURE','SF6气体压力':'PRESSURE20C','避雷器绝缘监测':'TOTALCURRENT',
'断路器局部放电':'DISCHARGECAPACITY','储能电机工作状态':'CHARGETIME','顶层油温':'OILTEMPERATURE',
'分合闸线圈电流波形':'ACTION','容性设备绝缘监测':'CAPACITANCE','铁芯接地电流':'TOTALCORECURRENT',
'微水':'MOISTURE','覆冰监测':'EQUAL_ICETHICKNESS','导线温度监测':'Line_Temperature1','导线舞动':'U_VERTICAL_AMPLITUDE',
'风偏监测':'Windage_Yaw_Angle','微风振动监测':'Vibration_Amplitude','微气象监测':'Average_WindSpeed',
'现场污秽度监测':'ESDD','SF6气体压力（天山换流站）':'PRESSURE20C','顶层油温（天山换流站）':'OILTEMPERATURE',
'微水（天山换流站）':'MOISTURE','避雷器绝缘监测（天山换流站）':'TOTALCURRENT',
'铁芯接地电流（天山换流站）':'TOTALCORECURRENT','油中溶解气体（天山换流站）':'H2'}
'''


univariate_dist = {'H2':1,'MOISTURE':2,'PRESSURE20C':3,'TOTALCURRENT':4,'DISCHARGECAPACITY':4,'CHARGETIME':5,
                   'OILTEMPERATURE':6,'ACTION':7,'CAPACITANCE':8,'TOTALCORECURRENT':9,
                   'MOISTURE':10,'EQUAL_ICETHICKNESS':11,'Line_Temperature1':12,'U_VERTICAL_AMPLITUDE':13,
                   'Windage_Yaw_Angle':14,'Vibration_Amplitude':15,'Average_WindSpeed':16,
                   'ESDD':17,'PRESSURE20C':18,'OILTEMPERATURE':19,'MOISTURE':20,'TOTALCURRENT':21,
                   'TOTALCORECURRENT':22,'H2':23}
