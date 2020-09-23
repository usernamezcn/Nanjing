import cx_Oracle
from datetime import timedelta,datetime
from Oracle_.oracle import TestOracle
import pandas as pd
import datetime
from fault_.des import SS
import os
import json
import time
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




class Ins2Orc(object):
    def __init__(self,user,pwd,ip,port,sid):
        self.connect=cx_Oracle.connect(user+"/"+pwd+"@"+ip+":"+port+"/"+sid)
        self.cursor=self.connect.cursor()

    def insert_(state,b_r,result_dict,DEVICECODE,result_cp,end_result_cp,broken_reason):
        # test_oracle = TestOracle('mw_app', 'app', '127.0.0.1', '1521', 'DBORCALE')
        test_oracle = TestOracle('mw_app', 'app', '192.168.2.200', '1521', 'ORCL')
        # param=[('30M00000059982619','(正常：0.3；异常：0.5；故障：0.2)','异常',time.strftime("%Y/%m/%D %H:%M:%S")),]
        param = [
            (DEVICECODE, datetime.datetime.now(), state, b_r, result_dict['0'], result_dict['1'], result_dict['2'],broken_reason), ]
        param_1 = [
            (DEVICECODE, datetime.datetime.now(), int(result_cp.iloc[0, 0]), int(result_cp.iloc[0, 1]),
             int(result_cp.iloc[0, 2]),
             int(result_cp.iloc[0, 3]),
             int(result_cp.iloc[0, 4]), int(result_cp.iloc[0, 5]), int(result_cp.iloc[0, 6]), int(result_cp.iloc[0, 7]),
             int(result_cp.iloc[0, 8])), ]
        param_2 = [
            (DEVICECODE, datetime.datetime.now(), float(end_result_cp.iloc[0, 0]), float(end_result_cp.iloc[0, 1]),
             float(end_result_cp.iloc[0, 2]), float(end_result_cp.iloc[0, 3]), float(end_result_cp.iloc[0, 4]) \
                 , float(end_result_cp.iloc[0, 5]), float(end_result_cp.iloc[0, 6]), float(end_result_cp.iloc[0, 7]),
             float(end_result_cp.iloc[0, 8]), float(end_result_cp.iloc[0, 9]) \
                 , float(end_result_cp.iloc[0, 10]), float(end_result_cp.iloc[0, 11]), float(end_result_cp.iloc[0, 12]),
             float(end_result_cp.iloc[0, 13]), float(end_result_cp.iloc[0, 14]) \
                 , float(end_result_cp.iloc[0, 15]), float(end_result_cp.iloc[0, 16]),
             SS['S1'], SS['S2'], SS['S3'], SS['S4'], SS['S5'], SS['S6'], SS['S7'], SS['S8'],
             SS['S9'], SS['S10'], SS['S11'], SS['S12'], SS['S13'], SS['S14'], SS['S15'],
             SS['S16'], SS['S17']), ]
        sql_insert = 'insert into BHT_DEVICE_STATUS(DEVICECODE,TIME,DEVICE_STATUS,BROKEN_RESULT,STATUS_0,STATUS_1,STATUS_2,BROKEN_REASON)values(:1,:2,:3,:4,:5,:6,:7,:8)'
        sql_insert_1 = 'insert into BHT_DEVICE_MIDDLE_PARTONE(DEVICECODE,TIME,DEVICE_OBNORMAL_X1,DEVICE_OBNORMAL_X2,DEVICE_OBNORMAL_X3,DEVICE_OBNORMAL_X4,DEVICE_OBNORMAL_X5,DEVICE_OBNORMAL_X6,DEVICE_OBNORMAL_X7,DEVICE_OBNORMAL_X8,DEVICE_OBNORMAL_X9)values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)'
        sql_insert_2 = 'insert into BHT_DEVICE_MIDDLE_PARTTWO(DEVICECODE,TIME,DEVICE_FAULT_S1,DEVICE_FAULT_S2,DEVICE_FAULT_S3,DEVICE_FAULT_S4,DEVICE_FAULT_S5,DEVICE_FAULT_S6,DEVICE_FAULT_S7,DEVICE_FAULT_S8,DEVICE_FAULT_S9,\
                                    DEVICE_FAULT_S10,DEVICE_FAULT_S11,DEVICE_FAULT_S12,DEVICE_FAULT_S13,DEVICE_FAULT_S14,DEVICE_FAULT_S15,DEVICE_FAULT_S16,DEVICE_FAULT_S17,\
                                    DEVICE_FAULT_S1_DATA_RESULT,DEVICE_FAULT_S2_DATA_RESULT,DEVICE_FAULT_S3_DATA_RESULT,DEVICE_FAULT_S4_DATA_RESULT,DEVICE_FAULT_S5_DATA_RESULT, \
                                   DEVICE_FAULT_S6_DATA_RESULT,DEVICE_FAULT_S7_DATA_RESULT,DEVICE_FAULT_S8_DATA_RESULT,DEVICE_FAULT_S9_DATA_RESULT,DEVICE_FAULT_S10_DATA_RESULT,\
                                   DEVICE_FAULT_S11_DATA_RESULT,DEVICE_FAULT_S12_DATA_RESULT,DEVICE_FAULT_S13_DATA_RESULT,DEVICE_FAULT_S14_DATA_RESULT,DEVICE_FAULT_S15_DATA_RESULT,\
                                   DEVICE_FAULT_S16_DATA_RESULT,DEVICE_FAULT_S17_DATA_RESULT)values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21\
                                   ,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35,:36)'

        # param = [(DEVICECODE, state, b_r, result_dict['0'], result_dict['1'], result_dict['2']), ]
        try:
            '''插入数据'''
            # sql_insert = 'insert into BHT_DEVICE_STATUS(DEVICECODE,DEVICE_STATUS,BROKEN_RESULT,STATUS_0,STATUS_1,STATUS_2)values(:1,:3,:4,:5,:6,:7)'
            print('最终表插入成功')
            test_oracle.insert(sql_insert, param)
        except:
            print('最终表插入失败')
        test_oracle = TestOracle('mw_app', 'app', '192.168.2.200', '1521', 'ORCL')
        try:
            test_oracle.insert(sql_insert_1, param_1)
            print('中间表一插入成功')
        except:
            print('中间表一插入失败')
        test_oracle = TestOracle('mw_app', 'app', '192.168.2.200', '1521', 'ORCL')
        try:
            test_oracle.insert(sql_insert_2, param_2)
            print('中间表二插入成功')
        except:
            print('中间表二插入失败')


