import numpy as np
from outliers import smirnov_grubbs as grubbs
from Oracle_.oracle import TestOracle
from fault_.fault_describe import univariate
import pandas as pd
from datetime import datetime,timedelta
import copy,time



def load_data_from_orcale(day_step = 30,startData = '2020-03-11'):
    '''从数据库中获取数据'''
    # connect参数  用户名、密码、host地址：端口、服务名
    # DianliuHuganqi,TaiguanYali,JubuFangdian,Video,Pic,Ganta = 0,0,0,0,0,0
    test_oracle=TestOracle('mw_app','app','127.0.0.1','1521','DBORCALE')


    '''不同监测类型，对应的数据还没有找到，到时候需要改的数据为：
    
    MONITORINGDATATABLE
    
    替换为应有的数据就行。
    '''



    '''查数据'''
    sql_select = 'select DEVICECODE,TYPENAME,MONITORINGDATATABLE from BHV_DEVICE'
    data_oracle= test_oracle.select(sql_select)
    for i in data_oracle:
        '''
        print('表名称***********************************************************:')
        print(i['MONITORINGDATATABLE'])
        print('应该取的监测类型*****************************：')
        print(univariate[i['TYPENAME']])
        '''

        if univariate[i['TYPENAME']]=='none':
            # print('{}           表中不存在数据'.format(i['TYPENAME']))
            continue
        try:
            aDay = timedelta(days=day_step)
            date_1 = startData;date_one=datetime.strptime(date_1,"%Y-%m-%d")
            date_2 = date_one-aDay;date_2=date_2.strftime("%Y-%m-%d")
            # sql_select_two = "select {} from {} t where t.RESAVE_TIME between date '{}' and date '{}' order by t.RESAVE_TIME and where t.DEVICECODE = '{}'"
            sql_select_two = "select {} from {} t where t.DEVICECODE = '{}' and t.RESAVE_TIME between date '{}' and date '{}' order by t.RESAVE_TIME asc"
            sql_select_two = sql_select_two.format(univariate[i['TYPENAME']],i['MONITORINGDATATABLE'],i['DEVICECODE'],date_2,date_1)
            data_oracle_two = pd.DataFrame(test_oracle.select(sql_select_two))
            if data_oracle_two.empty==True:
                pass
                #print('{}表为空'.format(univariate[i['TYPENAME']]))
            else:
                print('表名称***********************************************************:')
                print(i['MONITORINGDATATABLE'])
                print('应该取的监测类型*****************************：')
                print(univariate[i['TYPENAME']])
                # yield data_oracle_two
                yield {"DeviceCode":i['DEVICECODE'],"MonitorTypeName":i['TYPENAME'],"Date":date_1,"data":data_oracle_two}
                pass
                #print(data_oracle_two)
                #print('***********************')
        except:
            pass

            #print("设备标号为{}，监测类型为{}，数据库表为{}，发生故障".format(i['DEVICECODE'],i['TYPENAME'],i['MONITORINGDATATABLE']))
    # break
# print(data_oracle)
# DEVICECODE = data_oracle['DEVICECODE'][0]
# print('DEVICECODE ：',DEVICECODE)
# print(data_oracle)

