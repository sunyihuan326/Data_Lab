# coding:utf-8 
'''
created on 2019/1/17

@author:sunyihuan
'''
from sklearn.cluster import KMeans
import pandas as pd

inputfile = '/Users/sunyihuan/Desktop/xianchang_all.csv'  # 数据
outputfile = '/Users/sunyihuan/Desktop/xianchang_kmeams_result.xls'  # 数据
# data = pd.read_csv(inputfile, names=["age", 'three_court', 'face_length', 'face_sense', 'face_shape', 'skin_shade',
#                                      'natural_style', 'shape', 'hair_length', 'skin_hue', 'eyelid'],
#                    nrows=45150)  # 读取数据
data = pd.read_csv(inputfile, nrows=45150)  # 读取数据

data = data[["age", 'three_court', 'face_length', 'face_sense', 'face_shape', 'skin_shade',
             'natural_style', 'shape', 'hair_length', 'skin_hue', 'eyelid']]

# print(data)
data_zs = 1.0 * (data - data.mean()) / data.std()  # 数据标准化

k = 30
iteration = 500
model = KMeans(n_clusters=k, n_jobs=4, max_iter=iteration)  # 分为k类, 并发数4

model.fit(data_zs)  # 开始聚类

r1 = pd.Series(model.labels_).value_counts()  # 统计各个类别的数目

r2 = pd.DataFrame(model.cluster_centers_)  # 找出聚类中心

r = pd.concat([r2, r1], axis=1)  # 横向连接(0是纵向), 得到聚类中心对应的类别下的数目

r.columns = list(data.columns) + [u'类别数目']  # 重命名表头

print(r)

# 详细输出原始数据及其类别

r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)  # 详细
r.columns = list(data.columns) + [u'聚类类别']  # 重命名表头

r.to_excel(outputfile)  # 保存结果
