import numpy as np
from To_he import smirnov_grubbs as grubbs



num_of_outlier_to_dif_x8_x9 = 10 #
sliding_num = 0



def sigma_(data):
    std_ = data['b'].std()
    mean_ = data['b'].mean()
    sigma_min = mean_ - 3 * std_
    sigma_max = mean_ + 3 * std_
    length_ = len(data['b'])
    len_error = 0
    try:
        for i in range(length_):
            if (data['b'][i] > sigma_max) or (data['b'][i] < sigma_min): len_error += 1
    except:
        return True
    error_end = len_error / length_
    if error_end>=0.0027:return False  #越小越严谨,
    else:return True


'''数据连续增长(降低)'''
def abnormal_x6_x8(data,data_list):
    if sigma_(data)==True:return 0
    D_value = []
    for item_x6 in range(len(data_list)-1):
        if (data_list[item_x6]==None) or(data_list[item_x6+1] == None):continue
        D_value.append(abs(float(data_list[item_x6])-float(data_list[item_x6+1])))
    if len(D_value) == 0:return 0
    else:data_x6 = set(grubbs.test(D_value, alpha=0.01))
    data_x6_remove = list(set(D_value).difference(data_x6))
    if(len(data_x6_remove)>0):return 8
    else:return 6

def residal(data):
    sum = 0.0
    mean_ = np.mean(data)
    for residal_item in data:
        if residal_item == None:continue
        sum+=(float(residal_item)-mean_)**2
    return sum



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
    if max_above/part>persent_to_error:
        return True
    else:
        return False


def abnormal_x6_x7(data,data_list):
    if sigma_(data) == True: return 0
    residal_list,standard_num = [],0
    three_sigma = 3*(data.std()[0])
    residal_list.append(three_sigma)
    for item_x6_x7 in range(1,len(data_list)-1):
        k_temp = residal(data_list[0:item_x6_x7])+residal(data_list[item_x6_x7:len(data_list)-1])
        residal_list.append(k_temp)
        if k_temp<three_sigma:
            standard_num+=1
    residal_list.append(residal(data_list))
    if (standard_num==0) and (increase(data_list)):
        return 6
    else:
        return 7









def main_model_one(data_act):
    columns_ = data_act.columns[0]
    data_act.rename(columns={columns_: 'b'}, inplace=True)
    data_list = data_act['b'].tolist()
    data = data_act
    data.index = range(len(data))
    if abnormal_x6_x7(data,data_list)==6:
    # if (abnormal_x6_x8(data,data_list)==6) and (abnormal_x6_x7(data,data_list)==6):
        return True
    else:return False
