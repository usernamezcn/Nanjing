import numpy as np
from outliers import smirnov_grubbs as grubbs
from Oracle_.oracle import TestOracle
from fault_.fault_describe import univariate
import pandas as pd
from datetime import datetime,timedelta
import copy

'''从数据库中获取数据'''
# connect参数  用户名、密码、host地址：端口、服务名
# test_oracle=TestOracle('mw_app','app','192.168.2.200', '1521', 'ORCL')
test_oracle=TestOracle()
# test_oracle=TestOracle('mw_app','app','127.0.0.1', '1521', 'DBORCALE')

print("连接成功")
def str_to_int(num):
    a,b = num.split('/')
    return float(float(a)/float(b))
def str_to_list(S_list):
    S_list = S_list[1:-1]
    temp = []
    S_list = S_list.replace(' ', '')
    S_list = S_list.split(',')
    for i in S_list:
        if '/' in i:
            temp.append(str_to_int(i))
        else:
            temp.append(float(i))
    return temp


'''查数据'''
sql_select = 'select PARAM,PARAM_VALUE from bht_sys_config'
data_oracle= pd.DataFrame(test_oracle.select(sql_select))
data_oracle.set_index(['PARAM'],inplace=True)
num_x1_miss,num_x2_miss,num_repeat,jump,num_zero,sliding,operation_cycles = \
    str_to_list(data_oracle.loc['num_x1_miss'].values[0]),str_to_list(data_oracle.loc['num_x2_miss'].values[0]), \
    str_to_list(data_oracle.loc['num_repeat'].values[0]),str_to_list(data_oracle.loc['jump'].values[0]), \
    str_to_list(data_oracle.loc['num_zero'].values[0]),str_to_list(data_oracle.loc['sliding'].values[0]), \
    int(data_oracle.loc['operation_cycles'])
threshold, point_1, slide, point,thresholdSudden, point_1Sudden, slideSudden, pointSudden = float(data_oracle.loc['threshold'].values[0]), \
    int(data_oracle.loc['point_1'].values[0]),int(data_oracle.loc['slide'].values[0]),int(data_oracle.loc['point'].values[0]),float(data_oracle.loc['thresholdSudden'].values[0]), \
    int(data_oracle.loc['point_1Sudden'].values[0]), int(data_oracle.loc['slideSudden'].values[0]), int(data_oracle.loc['pointSudden'].values[0])
S_mat_origin = str_to_list(data_oracle.loc['S_mat_origin'].values[0])
s3_mat_origin = str_to_list(data_oracle.loc['s3_mat_origin'].values[0])
s7_mat_origin,s8_mat_origin,s9_mat_origin,s10_mat_origin,s11_mat_origin, \
s12_mat_origin,s13_mat_origin,s14_mat_origin,s15_mat_origin,s16_mat_origin,s17_mat_origin = \
str_to_list(data_oracle.loc['s7_mat_origin'].values[0]), \
str_to_list(data_oracle.loc['s8_mat_origin'].values[0]),str_to_list(data_oracle.loc['s9_mat_origin'].values[0]), \
str_to_list(data_oracle.loc['s10_mat_origin'].values[0]),str_to_list(data_oracle.loc['s11_mat_origin'].values[0]), \
str_to_list(data_oracle.loc['s12_mat_origin'].values[0]),str_to_list(data_oracle.loc['s13_mat_origin'].values[0]), \
str_to_list(data_oracle.loc['s14_mat_origin'].values[0]),str_to_list(data_oracle.loc['s15_mat_origin'].values[0]), \
str_to_list(data_oracle.loc['s16_mat_origin'].values[0]),str_to_list(data_oracle.loc['s17_mat_origin'].values[0])

# break
# print(data_oracle)
# DEVICECODE = data_oracle['DEVICECODE'][0]
# print('DEVICECODE ：',DEVICECODE)
# print(data_oracle)
