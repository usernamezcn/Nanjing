import sys
sys.path.append('F:\GNanjing')
import pickle
import os
from pgmpy.models import BayesianModel
from pgmpy.estimators import ParameterEstimator,MaximumLikelihoodEstimator,BayesianEstimator
from pgmpy.inference import VariableElimination
import pandas as pd


def main_model_two(result):
    if os.path.exists('bayes_/bayes_model.model'):
        f = open('bayes_/bayes_model.model', 'rb')  # 二进制，只读方式打开
        s = f.read()
        model2 = pickle.loads(s)
        pre_data = result
        pre_result = model2.predict_probability(pre_data)
        for i in pre_result.columns:  # 将数据由正常的概率改为，故障的概率
            pre_result[i].values[0] = 1 - pre_result[i].values[0]
        end_result = pd.DataFrame(pre_result,
                                  columns=['S1_0.0', 'S2_0.0', 'S3_0.0', 'S4_0.0', 'S5_0.0', 'S6_0.0', 'S7_0.0',
                                           'S8_0.0',
                                           'S9_0.0', 'S10_0.0', 'S11_0.0', 'S12_0.0', 'S13_0.0', 'S14_0.0', 'S15_0.0',
                                           'S16_0.0',
                                           'S17_0.0'])
        print('故障的类型及概率：\n', end_result)
        return end_result

    data = pd.read_csv('bayes_/read_data.csv')
    pre_data = result
    model2 = BayesianModel([('X8', 'S8'), ('X9', 'S9'), ('X1', 'S10'), ('X1', 'S12')
                           , ('X2', 'S10'), ('X2', 'S11'), ('X2', 'S13'), ('X3', 'S14')
                           , ('X4', 'S15'), ('X5', 'S16'), ('X6', 'S17'), ('X6', 'S7')
                           , ('X7', 'S7'), ('S10', 'S1'), ('S11', 'S1'), ('S12', 'S2')
                           , ('S13', 'S2'), ('X2', 'S3'), ('S14', 'S4'), ('S15', 'S4')
                           , ('S16', 'S4'), ('S17', 'S4'), ('S8', 'S5'), ('S9', 'S5')
                           , ('S1', 'S6'), ('S2', 'S6'), ('S3', 'S6'), ('S4', 'S6')
                           , ('S5', 'T'), ('S6', 'T'), ('S7', 'T')])
    model2.fit(data, estimator=BayesianEstimator)
    s = pickle.dumps(model2)
    with open('bayes_/bayes_model.model','wb+') as f:#二进制方式写入
        f.write(s)
    pre_result = model2.predict_probability(pre_data)
    for i in pre_result.columns: #将数据由正常的概率改为，故障的概率
        pre_result[i].values[0] = 1-pre_result[i].values[0]
    end_result = pd.DataFrame(pre_result,columns=['S1_0.0','S2_0.0','S3_0.0','S4_0.0','S5_0.0','S6_0.0','S7_0.0','S8_0.0',
                                    'S9_0.0','S10_0.0','S11_0.0','S12_0.0','S13_0.0','S14_0.0','S15_0.0','S16_0.0',
                                    'S17_0.0'])
    print('故障的类型及概率：\n', end_result)
    return end_result



