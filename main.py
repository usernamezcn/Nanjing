import sys
sys.path.append('F:\Reliability_Evaluation')
from fault_.fault_describe import X, S
from fault_.des import SS
from data_.model_one import main_model_one
from bayes_.bayes_model import main_model_two
from Oracle_.Traversing_database import load_data_from_orcale
from fuzzy_.fuzzy_model import weight, W_weight, s_mat_weight
from parameter_Definition import operation_cycles
from Oracle_.oracle import TestOracle
from fault_.fault_describe import univariate,univariate_dist
from Oracle_.Insert_to_orcale import Ins2Orc
from print_.to_pic import plt2pic
import numpy as np
import pandas as pd
import datetime, time, os,io,re
import schedule
import configparser

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)  # 输出全部元素

init_end_result = [0.0] * 17
init_end_result = pd.DataFrame(init_end_result).T
init_end_result.columns = ['S1_0.0', 'S2_0.0', 'S3_0.0', 'S4_0.0', 'S5_0.0', 'S6_0.0', 'S7_0.0', 'S8_0.0',
                           'S9_0.0', 'S10_0.0', 'S11_0.0', 'S12_0.0', 'S13_0.0', 'S14_0.0', 'S15_0.0', 'S16_0.0',
                           'S17_0.0']
init_result = pd.DataFrame([0.0] * 9, index=['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9']).T
init_result_dict = {'0': 1.0, '1': 0.0, '2': 0.0}

'''
operation_cycles 
输电线路在线监测装置可靠性评估周期。有四种取值：0--立即执行、1--每月执行一次、2--每周执行一次、3--每天执行一次。
'''


class Logger(object):
    def __init__(self, filename="Default.log", path="./"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.terminal = sys.stdout
        self.log = open(os.path.join(path, filename), "a", encoding='utf8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

# 如果消除注释则会，运行批量数据，才会显示日志
# sys.stdout = Logger('test_log.log')

def config():
    cf = configparser.ConfigParser()
    cf.read('F:/Reliability_Evaluation/config.ini')
    return cf.get('time_setting','day'),cf.get('time_setting','clock')
    pass

def main():
    for i in load_data_from_orcale():
        broken_reason = []
        broken_result = []  # 用来存放异常/故障的原因，S1-S17
        model_one_temp = 0
        data_act = i['data']


        data_act = data_act.rolling(window=5, win_type='gaussian', center=True).mean(std=0.5)  # 平滑操作


        Monitoring_type_parameter = i['Monitoring_type_parameter']
        # print(Monitoring_type_parameter)
        DEVICECODE = i['DeviceCode']
        result = main_model_one(data_act,Monitoring_type_parameter)

        result_cp = result.__deepcopy__()
        for i in range(9):
            if result.iloc[0, i] == 1.0: model_one_temp = 1;break;
        if model_one_temp == 0:  #如果没有任何装置异常，直接退出循环
            Ins2Orc.insert_(state=0, b_r='正常', result_dict=init_result_dict, DEVICECODE=DEVICECODE,
                            result_cp=result_cp, end_result_cp=init_end_result, broken_reason='无')

            continue

        '''画图进行确认'''
        plt2pic(data_act)


        '''模型一的输出'''

        print('模型一的输出结果----数据中存在的异常模式：',end=' ')
        for i in result.T.index:
            # print(result[i].values[0])  #输出的是 0 or 1
            if result[i].values[0] == 1.0:
                broken_result.append(X[i])
                print(X[i],' ',i,end=' ')
        print()



        '''模型二的输出'''
        end_result = main_model_two(result)
        '''
        if result.values[0].tolist()==[0]*9:
            end_result = pd.DataFrame([0]*17,index=['S1_0.0', 'S2_0.0', 'S3_0.0', 'S4_0.0', 'S5_0.0', 'S6_0.0', 'S7_0.0', 'S8_0.0',
                                       'S9_0.0', 'S10_0.0', 'S11_0.0', 'S12_0.0', 'S13_0.0', 'S14_0.0', 'S15_0.0',
                                       'S16_0.0',
                                       'S17_0.0']).T
        '''

        end_result_cp = end_result.__deepcopy__()
        max_value = max(end_result.values[0])

        for i in end_result.columns:
            if float(max_value) == float(end_result[i]):
                broken_reason.append(S[i])
        result_dict = {}  # 用来存放模型三的结果

        print('len(end_result)',len(end_result))
        for i in range(len(end_result)):

            columns = ['S3_0.0', 'S7_0.0', 'S8_0.0', 'S9_0.0', 'S10_0.0', 'S11_0.0', 'S12_0.0',
                       'S13_0.0', 'S14_0.0', 'S15_0.0', 'S16_0.0', 'S17_0.0']
            end_result = end_result[columns]
            w_weight = W_weight(s_mat_weight, end_result.loc[i].values)
            result = np.dot(w_weight, weight)
            result = result * 100
            result_ = pd.DataFrame(result, index=['正常', '异常', '故障'], columns=['result'])
            result_dict = {'0': round(result[0], 4), '1': round(result[1], 4), '2': round(result[2], 4)}

            state = max(result_dict, key=lambda x: result_dict[x])

        broken_result = ','.join(broken_result)  # 取出列表中的所有元素
        broken_reason = ','.join(broken_reason)


        '''模型三结果存入数据库'''
        Ins2Orc.insert_(state=state, b_r=broken_result, result_dict=result_dict, DEVICECODE=DEVICECODE,
                        result_cp=result_cp,
                        end_result_cp=end_result_cp, broken_reason=broken_reason)
        # time.sleep(5)


if __name__ == '__main__':
    num_day_, clock = config()
    num_day_ = num_day_.replace(' ', '')
    num_day = []
    [num_day.append(int(i)) for i in re.split('[,:]', num_day_)]
    if operation_cycles == 0:
        main()
    elif operation_cycles == 1:
        num_day = num_day[:1]
        if (datetime.datetime.now().day in num_day) and (str(datetime.datetime.now().time())[:5] == clock):
            main()
    elif operation_cycles == 2:
        if (datetime.datetime.now().day in num_day) and (str(datetime.datetime.now().time())[:5] == clock):
            main()
    elif operation_cycles == 3:
        if str(datetime.datetime.now().time())[:5] == clock:
            main()
    else:
        pass
    # schedule.every().day.at(clock).do(main)   #如果需要修改时间点的话可以在这里修改。
    while True:
        schedule.run_pending()
