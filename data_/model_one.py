import numpy as np
from outliers import smirnov_grubbs as grubbs
from Oracle_.oracle import TestOracle
from Oracle_.Traversing_database import load_data_from_orcale
from parameter_Definition import num_x1_miss,num_x2_miss,num_repeat,jump,num_zero,sliding
import pandas as pd
import copy,random
import time

#设置参数
num_of_outlier_to_dif_x8_x9 = 10 #
sliding_num = 0


def proform(data,data_list):
    repeat_num_to_wrong = 2
    error_data = [0] * len(data)
    data_repeat_temp = copy.deepcopy(data['b'])
    for i in range(len(data_repeat_temp)):
        if data_repeat_temp[i] == None:
            data_repeat_temp[i] = random.randint(10000,100000)
    df = data_repeat_temp.loc[data_repeat_temp.diff(repeat_num_to_wrong) == 0]
    df_index = list(df.index)
    for item in df_index:
        error_data[item] = 1
    # 1.2缺失
    data_missing = data[data['b'].isnull() == True]
    for item in data_missing.index:
        error_data[item] = 1
    # 1.3 and 1.4 判断跳变,为零
    for iterm_jump in range(len(data_list) - 1):
        if data_list[iterm_jump]==None:
            pass
        elif ((abs(data_list[iterm_jump + 1] - data_list[iterm_jump]) >= jump) or (
                data_list[iterm_jump] == 0.0)):
            error_data[iterm_jump] = 1
    return error_data

'''数据中断(瞬时)'''
def abnormal_x1(l_data,data):
    for item_data in range(len(data)-num_x1_miss):
        if (l_data[item_data]!=0):
            for miss in range(num_x1_miss):
                if(data.iloc[item_data+miss].isnull().values==[False]):break;
                if miss == num_x1_miss-1:l_data[item_data] = 2;
    return l_data

'''数据中断(长期)'''
def abnormal_x2(l_data,data):
    for item_data in range(len(data)-num_x2_miss):
        if (l_data[item_data] != 0):
            for miss in range(num_x2_miss):
                if (data.iloc[item_data+miss].isnull().values == [False]): break;
                if miss == num_x2_miss - 1: l_data[item_data] = 3;
    return l_data


#数据重复
def abnormal_x3(l_data,data):
    error_data = [0] * len(data)
    try:
        df = data.loc[data['b'].diff(5) == 0]
    except:
        data_repeat_temp = copy.deepcopy(data['b'])
        for i in range(len(data_repeat_temp)):
            if data_repeat_temp[i] == None:
                data_repeat_temp[i] = random.randint(10000, 100000)
        df = data.loc[data_repeat_temp.diff(5) == 0]
    df_index = list(df.index)
    for item in df_index:
        error_data[item] = 1
    if len(df) >= num_repeat-1:#重复数量到达num_repeat个才构成重复,如果没有达到num_repeat,便不用进入循环了
        for num_in_df_index in range(len(df_index)-3):
            for i in range(num_repeat-1):
                if df_index[num_in_df_index] == df_index[num_in_df_index+i]-i:pass
                else :df_index[num_in_df_index] = -1
    df_index = df_index[:len(df_index)-num_repeat+2]
    df_index_deepcopy = copy.deepcopy(df_index)
    for df_index_num in df_index:
        if df_index_num==-1:
            df_index_deepcopy.remove(-1)
    if len(df_index_deepcopy)==0:
        pass
    else :
        for item in df_index_deepcopy:
            l_data[item] = 4
    return l_data


'''数据固定偏移---检测值与实际值的差别'''
def abnormal_x4(l_data,data):
    pass
'''数据为零'''

def abnormal_x5(l_data,data):
    for item_data in range(len(data)-num_zero):
        if (l_data[item_data] != 0):
            for miss in range(num_zero):
                if (data[item_data+miss] != 0.0): break;
                if miss == num_zero - 1: l_data[item_data] = 6;
    return l_data

def sigma_(data):
    std_ = data['b'].std()
    mean_ = data['b'].mean()
    sigma_min = mean_ - 3 * std_
    sigma_max = mean_ + 3 * std_
    length_ = len(data['b'])
    len_error = 0
    for i in range(length_):
        if (data['b'][i] > sigma_max) or (data['b'][i] < sigma_min): len_error += 1
    error_end = len_error / length_
    if error_end>=0.0027:return False
    else:return True


def increase(data_list):
    part_list, above, max_above, part, persent_to_error = [], 0, 0, 20, 0.25
    length = len(data_list)
    part_len = length // part
    try:
        for i in range(part):
            part_list.append(np.mean(data_list[i * part_len:(i + 1) * part_len]))
    except:
        return False
    for i in range(part - 1):
        if part_list[i + 1] - part_list[i] > 0:
            above += 1
            max_above = max(max_above, above)
        else:
            above = 0
    if max_above / part > persent_to_error:
        return True
    else:
        return False



def func_jump_error(value):
    data_copy = value.copy()
    data_series = pd.Series(value['b'].values, index=value['b'].index)

    '''报错！！！！！！！！！'''
    try:
        temp = set(grubbs.test(data_series, alpha=0.06))
    except:return []
    all_right_data = list(temp)
    data_copy = data_copy[~data_copy['b'].isin(all_right_data)]
    return data_copy

'''数据连续增长(降低)'''
def abnormal_x6_x8(data,data_list):
    if sigma_(data)==True:return 0
    D_value = []
    for item_x6 in range(len(data_list)-1):
        if (data_list[item_x6]==None) or (data_list[item_x6+1] == None): continue
        D_value.append(abs(float(data_list[item_x6])-float(data_list[item_x6+1])))
    if len(D_value) == 0:return 0
    else:data_x6 = set(grubbs.test(D_value, alpha=0.01))
    data_x6_remove = list(set(D_value).difference(data_x6))
    if(len(data_x6_remove)>0):return 8

def residal(data):
    sum = 0.0
    mean_ = np.mean(data)
    for residal_item in data:
        if residal_item == None:continue
        sum+=(float(residal_item)-mean_)**2
    return sum

'''数据跳边'''
def abnormal_x6_x7(data,data_list):
    if sigma_(data) == True: return 0
    residal_list,standard_num = [],0
    three_sigma = 3*(data.std()[0])
    residal_list.append(three_sigma)
    for item_x6_x7 in range(1,len(data_list)-1):
        k_temp =np.var(data_list[0:item_x6_x7])*len(data_list[0:item_x6_x7])+np.var(data_list[item_x6_x7:len(data_list)-1])*len(data_list[item_x6_x7:len(data_list)-1])
        residal_list.append(k_temp)
        if k_temp<three_sigma:
            standard_num+=1
    residal_list.append(residal(data_list))
    if standard_num>0:
        return 7

'''数据抖动'''
def abnormal_x8(data):
    pass

'''离群点'''
def abnormal_x8_x9(data,data_list):
    if sigma_(data) == True: return 0
    out = func_jump_error(data)
    if len(out)<3:
        return 0
    elif len(out)<num_of_outlier_to_dif_x8_x9:
        return 9
    else:
        return 8


def main_model_one(data_act):
    result = [0.0] * 9

    '''
    !!!!!!!!!!!!!!      ATTENTION      判空处理     ATTENTION !!!!!!!!!!!!!!!!!!!
    
    等不测试的时候将下面的代码注释解除 
    同时需要修改Traversing_database.py
    '''

    # if data_act.empty==True:
    #     result[1] = 1.0
    #     print('空')
    #     return pd.DataFrame(result, index=['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9']).T
    print_range_num = 0
    columns_ = data_act.columns[0]
    data_act.rename(columns={columns_: 'b'}, inplace=True)
    data_list = data_act['b'].tolist()
    for item in range(sliding_num+1):
        data = data_act
        data.index = range(len(data))
        print_range_num+=1
        error_data = proform(data,data_list)
        v_count = data['b'].value_counts()
        if len(v_count)==0:
            result[1] = 1.0
            return pd.DataFrame(result,index = ['X1','X2','X3','X4','X5','X6','X7','X8','X9']).T
        error_x1 = abnormal_x1(error_data, data)
        result[0] = 1.0 if 2 in error_x1 else 0.0
        error_x2 = abnormal_x2(error_data, data)
        result[1] = 1.0 if 3 in error_x2 else 0.0
        error_x3 = abnormal_x3(error_data, data)
        result[2] = 1.0 if 4 in error_x3 else 0.0
        error_x5 = abnormal_x5(error_data, data_list)
        result[4] = 1.0 if 6 in error_x5 else 0.0
        if increase(data_list):result[5] = 1.0
        else:result[5] = 0.0
        if abnormal_x6_x8(data,data_list)==8:
            result[7] = 1.0
        alt = abnormal_x6_x7(data,data_list)
        if alt==7:
            result[6] = 1.0
        alt = abnormal_x8_x9(data,data_list)
        if alt==9:
            result[8] = 1.0
        elif alt==8:
            result[7] = 1.0
        if result[4]==1.0:result[2] = 0.0
        result = pd.DataFrame(result,index = ['X1','X2','X3','X4','X5','X6','X7','X8','X9']).T
    return result
