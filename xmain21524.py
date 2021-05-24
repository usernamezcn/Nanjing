import sys
sys.path.append('F:\Reliability_Evaluation')
from outliers import smirnov_grubbs as grubbs
from fault_.fault_describe import X, S
from fault_.des import SS
from data_.model_one import main_model_one
from bayes_.bayes_model import main_model_two
from Oracle_.xTraversing_database import xload_data_from_orcale
from parameter_Definition import threshold, point_1, slide, point,thresholdSudden, point_1Sudden, slideSudden, pointSudden, jump
from fuzzy_.fuzzy_model import weight, W_weight, s_mat_weight
from Oracle_.oracle import TestOracle
from fault_.fault_describe import univariate,univariate_dist
from Oracle_.xInsert_to_oracle import Ins2Orc
from print_.to_pic import plt2pic
from print_.to_pic import xplt2pic
import numpy as np
import pandas as pd
import datetime, time, os, io
import schedule


'''
趋势告警分析：
如果一个滑动窗口内存在10个连续上升（下降）的子序列
或者在一个20个数据的子滑窗内，有17个上升（下降）的子序列
那么就发出     趋势告警
(斜率超过阈值<threshold>称为上升)



'''
minnnn = 0.00000001

#       数据    斜率阈值 连续子序列阈值 子滑动窗口大小 序列阈值
#               0.03       10         20          17       趋势告警
#               0.25       5          10          8        突变告警
def alarm(data,threshold,     slide,      point):
    slope = []
    up, down = 0, 0
    # point_1, slide, point = 10, 20, 17
    end = False
    for i in range(1, len(data)):
        if ((data[i] - data[i - 1])/(data[i-1]+minnnn))>=threshold:
            slope.append(1)
        elif ((data[i] - data[i - 1])/(data[i-1]+minnnn))<=(threshold*-1):
            slope.append(-1)
        else:
            slope.append(0)
    #连续子序列
    '''
    for i in slope:
        if down > point_1 or up > point_1:
            end_1 = True
            break
        if i > 0:
            down = 0
            up += 1
        elif i < 0:
            up = 0
            down += 1
    '''
    # 非连续子序列
    if slide > len(data):#如果数据本身的长度不足一个滑窗，那么暂时将滑窗定义为本身数据的长度。
        slide = len(data) - 1
    for i in range(0, len(data) - slide):
        count_up, count_down = 0, 0
        for j in range(slide):
            if slope[i + j] > 0: count_up += 1
            if slope[i + j] < 0: count_down += 1
        if count_up >= point or count_down >= point:
            end = True
            break
    if end:
        return 1
    return 0

def alarmSudden(data,threshold,point_1,     slide,      point):
    slope = []
    tmp = 0
    # point_1, slide, point = 10, 20, 17
    end_1, end_2 = False, False
    for i in range(1, len(data)):
        if ((data[i] - data[i - 1])>=threshold) or ((data[i] - data[i - 1])<=(threshold*-1)):
            slope.append(1)
        else:
            slope.append(0)
    #连续子序列
    for i in slope:
        if tmp > point_1:
            end_1 = True
            break
        if i == 1:
            tmp+=1
        elif i == 0:
            tmp=0
    if slide > len(data):
        slide = len(data) - 1
    # 非连续子序列
    for i in range(0, len(data) - slide):
        count = 0
        for j in range(slide):
            if slope[i + j] == 0: count += 1
        if count >= point:
            end_2 = True
            break
    if end_1 or end_2:
        return 1
    return 0

'''数据库的读取'''
for i in xload_data_from_orcale():
    result_dict = {'0': 1.0, '1': 0.0, '2': 0.0}
    # end_trend, end_mutation = 0,0
    #趋势告警阈值
    # threshold, point_1, slide, point = 0.03, 10, 20, 17
    #突变告警阈值
    # thresholdSudden, point_1Sudden, slideSudden, pointSudden = 0.06,5,10,8
    data_act,state,broken_reason = i['data'],0,'wu'
    DEVICECODE = i['DeviceCode']
    name = i['MonitorTypeName']
    Monitoring_type_parameter = i['Monitoring_type_parameter']
    print(name,'    ',univariate[name])
    jump_ = int(jump[Monitoring_type_parameter])
    if data_act.empty == True:
        continue
    columns_ = data_act.columns[0]
    data_act.rename(columns={columns_: 'b'}, inplace=True)
    data_list = data_act['b'].tolist()
    if all(e is None for e in data_list):
        continue
    data = data_act
    ''' 线性函数归一化：将原始数据等比例缩放到  [0,1]  的范围内，
    不仅 保留了数据的原始特征，而且提高 模型的运算速度和准确率。
    '''
    max_,min_ = max(data_list),min(data_list)
    if max_ == min_:
        # 说明数据重复，完全相同
        pass
    else:
        for i in range(len(data_list)):
            data_list[i] = abs((data_list[i]-min_)/max_-min_)
        # end_trend,end_mutation = trend_nor(data_list),mutation_nor(data_list)
        end_trend, end_mutation = alarm(data_list,threshold,slide,point),alarm(data_list,thresholdSudden,slideSudden,pointSudden)
        if end_trend or end_mutation:
            result_dict['1'] = 1.0
            result_dict['0'] =  0.0
            state = 1
        if end_trend and end_mutation:
            result_dict['2'] = 1.0
            result_dict['1'] = 0.0
            state = 2

    Ins2Orc.insert_(state=state, result_dict=result_dict, DEVICECODE=DEVICECODE,broken_reason=broken_reason)


    print(result_dict, '                \n趋势告警：', end_trend, '        \n突变告警 ：', end_mutation)
    plt2pic(data_act)
    # time.sleep(2)
    # xplt2pic(data_list)
    time.sleep(6)

