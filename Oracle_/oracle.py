#  coding=utf-8
import cx_Oracle
from datetime import timedelta,datetime
import pandas as pd
import os
import json
import time
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
"""python version 3.7"""

class TestOracle(object):
    def __init__(self,user = 'mw_app',pwd = 'app',ip = '192.168.2.200',port = '1521',sid = 'ORCL'):
        self.connect=cx_Oracle.connect(user+"/"+pwd+"@"+ip+":"+port+"/"+sid)
        self.cursor=self.connect.cursor()

    def select_between_data_n(self,date_1,n):
        aDay = timedelta(days=n)
        str2date=datetime.strptime(date_1,"%Y-%m-%d")#把字符类型转换成datetime.datetime类型 否则无法+aDay
        date_2=str2date-aDay
        date_2=date_2.strftime("%Y-%m-%d") ##把datetime类型转换成str类型

        sql_between = 'select DEVICECODE,EQUAL_ICETHICKNESS,RESAVE_TIME from CMST_ICETHICKNESS where CMST_ICETHICKNESS.RESAVE_TIME between date\'%s\'and date\'%s\' order by RESAVE_TIME asc'%(date_2,date_1)
        self.cursor.execute(sql_between)
        data = self.cursor.fetchall() #取出所有数据  fetch取
        data = pd.DataFrame(data)##重新排列字典 key值在上方  index在第一列   具体功能见草稿
        return data


    def select_by_data(self,date_1,n,content,here,condition):
        aDay = timedelta(days=n)
        str2date=datetime.strptime(date_1,"%Y-%m-%d")#把字符类型转换成datetime.datetime类型 否则无法+aDay
        date_2=str2date-aDay
        date_2=date_2.strftime("%Y-%m-%d") ##把datetime类型转换成str类型
        sql_between = "select {} from {} t where t.RESAVE_TIME between date '{}' and date '{}' order by RESAVE_TIME and where t.DEVICECODE='{}'"
        sql_between = sql_between.format(content,here,date_2,date_1,condition)
        self.cursor.execute(sql_between)
        data = self.cursor.fetchall() #取出所有数据  fetch取
        data = pd.DataFrame(data)##重新排列字典 key值在上方  index在第一列   具体功能见草稿
        return data

    """处理数据二维数组，转换为json数据返回"""
    def select(self,sql):
        list=[]
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        col_name=self.cursor.description
        for row in result:
            dict={}
            for col in range(len(col_name)):
                key=col_name[col][0]
                value=row[col]
                dict[key]=value
            list.append(dict)
        # js = json.dumps(list, ensure_ascii=False, indent=2, separators=(',', ':'))
        # return js
        return list
    def disconnect(self):
        self.cursor.close()
        self.connect.close()
    def insert(self,sql,list_param):
        try:
            self.cursor.executemany(sql,list_param)
            self.connect.commit()
            # print("插入成功")
        except Exception as e:
            print('CRSB' + e)
        finally:
            self.disconnect()
    def update(self,sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()

        except Exception as e:
            print(e)
        finally:
            self.disconnect()
    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            print("delete ok")
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


# if __name__ =="__main__":
#     # 'mw_app/app@127.0.0.1:1521/ORACLE'
#     test_oracle=TestOracle('mw_app','app','127.0.0.1','1521','ORACLE')
#     # time = to_date('2007-12-28 10:07:24', 'yyyy-mm-dd hh24:mi:ss')
#     # param=[('30M00000059982619','(正常：0.3；异常：0.5；故障：0.2)','异常',time.strftime("%Y/%m/%D %H:%M:%S")),]
#     param = [('30M00000059982610', '(正常：0.1；异常：0.7；故障：0.2)', '异常',), ]
#     try:
#         '''查数据'''
#         sql_select = 'select DEVICECODE,EQUAL_ICETHICKNESS,RESAVE_TIME from CMST_ICETHICKNESS'
#         data = test_oracle.select(sql_select)
#         print(data)
#     except:
#         print('查询失败')
#     try:
#         '''插入数据'''
#         # sql_insert = 'insert into MODEL3_RESULT(DEVICECODE, STATE_PROBABILITY,DEVICECODE_STATE,DETECTION_TIME )values(:1,:2,:3,:4)'
#         sql_insert = 'insert into MODEL3_RESULT(DEVICECODE, STATE_PROBABILITY,DEVICECODE_STATE )values(:1,:2,:3)'
#         test_oracle.insert(sql_insert, param)
#     except:
#         print('插入失败')
    #test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values(:1,:2,:3,:4)",param)#也可以下面这样解决orc-1036非法变量问题
    # test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values(:ENAME,:JOB,:SAL,:COMM)",param)
    # test_oracle1=TestOracle('SCOTT','pipeline','127.0.0.1','1521','orcl')
    # test_oracle1.delete("delete from bonus where ENAME='ss1' or ENAME='ww1'")
    # test_oracle3=TestOracle('SCOTT','pipeline','127.0.0.1','1521','orcl')

