import numpy as np
from outliers import smirnov_grubbs as grubbs
from Oracle_.oracle import TestOracle
from Oracle_.Traversing_database import load_data_from_orcale
from parameter_Definition import num_x1_miss,num_x2_miss,num_repeat,jump,num_zero,sliding
import pandas as pd
import copy,random
import time

'''从数据库中获取数据
# connect参数  用户名、密码、host地址：端口、服务名
test_oracle=TestOracle('mw_app','app','127.0.0.1','1521','DBORCALE')
print("连接成功")
try:
    sql_select = 'select DEVICECODE,EQUAL_ICETHICKNESS,RESAVE_TIME from CMST_ICETHICKNESS'
    data_oracle= pd.DataFrame(test_oracle.select(sql_select))
    DEVICECODE = data_oracle['DEVICECODE'][0]
    # print('DEVICECODE ：',DEVICECODE)
    # print(data_oracle)
except:
    print("数据查询失败")
'''

#设置参数
num_of_outlier_to_dif_x8_x9 = 10 #

# sliding_num = len(data_act) - sliding
sliding_num = 0
# num_need_repeat = 4



'''提前将数据进行处理，find重复、缺失跳变、为零的数据标记为异常数据'''
'''error_data作为返回值，当erro_data==1时代表存在以上异常情况中的一种或多种'''
def proform(data,data_list):
    '''数据重复,需要有几个重复,才会构成装置故障'''
    repeat_num_to_wrong = 2
    error_data = [0] * len(data)#创建一个和data等长的数组,用于标记是否存在装置故障,
    # data_repeat = data['b'].diff(repeat_num_to_wrong)
    '''当相同的数据存在n个或n个以上时，给第一个赋零
    但是并不能代表长期或短期中断,具体还需要下面的方法判定'''
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
#l_data是标记数据是否发生故障的list

'''数据中断(瞬时)'''
def abnormal_x1(l_data,data):# l_data即proform返回的error_data
    for item_data in range(len(data)-num_x1_miss):
        if (l_data[item_data]!=0):
            for miss in range(num_x1_miss):
                if(data.iloc[item_data+miss].isnull().values==[False]):break;#如果非空直接跳出循环
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
    #data_repeat = data['b'].diff(2)
    try:
        df = data.loc[data['b'].diff(5) == 0]
    except:
        data_repeat_temp = copy.deepcopy(data['b'])
        for i in range(len(data_repeat_temp)):
            if data_repeat_temp[i] == None:
                data_repeat_temp[i] = random.randint(10000, 100000)
        df = data.loc[data_repeat_temp.diff(5) == 0]
    df_index = list(df.index)
    # print(df_index)
    for item in df_index:
        error_data[item] = 1
    # print('error_data',df_index)
    if len(df) >= num_repeat-1:#重复数量到达num_repeat个才构成重复,如果没有达到num_repeat,便不用进入循环了
        for num_in_df_index in range(len(df_index)-3):
            for i in range(num_repeat-1):
                if df_index[num_in_df_index] == df_index[num_in_df_index+i]-i:pass
                else :df_index[num_in_df_index] = -1
    # print(df_index)
    df_index = df_index[:len(df_index)-num_repeat+2]
    # print(df_index)
    df_index_deepcopy = copy.deepcopy(df_index)
    for df_index_num in df_index:
        if df_index_num==-1:
            df_index_deepcopy.remove(-1)
    # print(l_data)
    if len(df_index_deepcopy)==0:
        pass
        # print('没有重复值')
    else :
        for item in df_index_deepcopy:
            l_data[item] = 4
            #l_data[item_data] = (l_data[item_data]-1)*10+2;
        # print(df_index_deepcopy)
    return l_data


'''数据固定偏移---检测值与实际值的差别'''
def abnormal_x4(l_data,data):
    pass

'''数据为零'''
def abnormal_x5(l_data,data):
    for item_data in range(len(data)-num_zero):
        if (l_data[item_data] != 0):#如果存在故障
            for miss in range(num_zero):
                if (data[item_data+miss] != 0.0): break;
                if miss == num_zero - 1: l_data[item_data] = 6;#如果存在连续num_zero个0,则赋6
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
    if error_end>=0.0027:return False  #越小越严谨
    else:return True


def increase(data_list):
    part_list,above,max_above,part,persent_to_error = [],0,0,20,0.25
    length = len(data_list)
    part_len = length//part
    try:
        for i in range(part):
            part_list.append(np.mean(data_list[i*part_len:(i+1)*part_len]))
    except:
        return False
    for i in range(part-1):
        if part_list[i+1]-part_list[i]>0:
            above+=1
            max_above = max(max_above,above)
        else:
            above = 0
    if (max_above/part)>persent_to_error:
        return True
    else:
        return False




def func_jump_error(value):
    #value是单维的数据


    # return list(temp)
    data_copy = value.copy()
    data_series = pd.Series(value['b'].values, index=value['b'].index)

    '''报错！！！！！！！！！'''
    try:
        temp = set(grubbs.test(data_series, alpha=0.01))
    except:return []
    # print(temp)
    # all_right_data = func_jump_error((data_series))
    all_right_data = list(temp)
    for item_right in all_right_data:
        data_copy = data_copy[~data_copy['b'].isin([item_right])]
    # print(data_copy)  # data_copy 表示离群点
    # jump_error = set(value) - set(list(grubbs.test(value,alpha=0.01)))
    # return list(jump_error)
    return data_copy

'''数据连续增长(降低)'''
def abnormal_x6_x8(data,data_list):
    #两者的共同点
    if sigma_(data)==True:return 0
    # if data.std().values[0]<data.mean().values[0]*0.2:#如果存在的短时连续突增或突降小于某个值，则不进行x6,x8判定
    #     return 0
    #两者的区分
    D_value = []
    for item_x6 in range(len(data_list)-1):
        if (data_list[item_x6]==None) or(data_list[item_x6+1] == None):continue
        D_value.append(abs(float(data_list[item_x6])-float(data_list[item_x6+1])))
    if len(D_value) == 0:return 0
    else:data_x6 = set(grubbs.test(D_value, alpha=0.01))
    data_x6_remove = list(set(D_value).difference(data_x6))
    if(len(data_x6_remove)>0):return 8
    #else:return 6         #但是我感觉这个只能适用于某一个范围，不能适用于整个窗口，至少不能存在一个就判定为抖动

def residal(data):#求残差
    sum = 0.0
    mean_ = np.mean(data)
    for residal_item in data:
        # print(type(float(residal_item)))
        if residal_item == None:continue
        sum+=(float(residal_item)-mean_)**2
    return sum
    pass

'''数据跳边'''
def abnormal_x6_x7(data,data_list):

    # if data.std().values[0]<data.mean().values[0]*0.2:#如果存在的短时连续突增或突降小于某个值，则不进行x6,x8判定
    #     return 0
    if sigma_(data) == True: return 0
    # print(data)
    # start2 = time.time()
    residal_list,standard_num = [],0
    three_sigma = 3*(data.std()[0])
    residal_list.append(three_sigma)
    # start3 = time.time()
    # print('x6_x7中的时间消耗2', start3 - start2)
    for item_x6_x7 in range(1,len(data_list)-1):
        k_temp = residal(data_list[0:item_x6_x7])+residal(data_list[item_x6_x7:len(data_list)-1])
        residal_list.append(k_temp)
        if k_temp<three_sigma:
            standard_num+=1
    # start4 = time.time()
    # print('x6_x7中的时间消耗3', start4 - start3)
    residal_list.append(residal(data_list))
    if standard_num>0:
        return 7

'''数据抖动'''
def abnormal_x8(data):
    pass

'''离群点'''
def abnormal_x8_x9(data,data_list):
    '''
    data_copy = data.copy()
    data_series = pd.Series(data['b'].values,index = data['b'].index)
    all_right_data = func_jump_error((data_series))
    for item_right in all_right_data:
        data_copy = data_copy[~data_copy['b'].isin([item_right])]
    print(data_copy)#data_copy 表示离群点
    '''
    if sigma_(data) == True: return 0
    out = func_jump_error(data)
    if len(out)<3:
        return 0
    elif len(out)<num_of_outlier_to_dif_x8_x9:
        return 9
    else:
        return 8
    pass


'''error_x1到5是list类型，value(元素）-1，代表发生的故障类型'''

#导入数据
# data_act = pd.read_csv('../ice.csv', header=None)

def main_model_one(data_act):
    result = [0.0] * 9
    print_range_num = 0
    columns_ = data_act.columns[0]
    data_act.rename(columns={columns_: 'b'}, inplace=True)
    data_list = data_act['b'].tolist()
    for item in range(sliding_num+1):#滑动窗口大小设置，正式算法接近完成的时候将对data进行限定。
        data = data_act
        data.index = range(len(data))#更改index,
        print_range_num+=1
        error_data = proform(data,data_list)
        '''空值的处理'''
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
        if abnormal_x6_x8(data,data_list)==8:
            result[7] = 1.0
        alt = abnormal_x6_x7(data,data_list)
        if alt==7:
            result[6] = 1.0
        elif alt==6:
            result[5] = 1.0
        alt = abnormal_x8_x9(data,data_list)
        if alt==9:
            result[8] = 1.0
        elif alt==8:
            result[7] = 1.0
        result = pd.DataFrame(result,index = ['X1','X2','X3','X4','X5','X6','X7','X8','X9']).T
        if result.iloc[0, 4] == 1.0:
            result.iloc[0, 2] = 0.0
    return result
