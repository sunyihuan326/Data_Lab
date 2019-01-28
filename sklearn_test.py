# coding:utf-8 
'''
created on 2019/1/11

@author:sunyihuan
'''
from sklearn import datasets
import pandas as pd

# iris = datasets.load_iris()  # 导入数据集
# X = iris.data  # 获得其特征向量
# y = iris.target  # 获得样本label

inputfile = '/Users/sunyihuan/Desktop/xianchang_all.csv'  # 数据

# data = pd.read_csv(inputfile, names=["age", 'three_court', 'face_length', 'face_sense', 'face_shape', 'skin_shade',
#                                      'natural_style', 'shape', 'hair_length', 'skin_hue', 'eyelid'],
#                    nrows=45150)  # 读取数据
data = pd.read_csv(inputfile, nrows=45150)  # 读取数据

data_x = data[["age", 'three_court', 'face_length', 'face_sense', 'face_shape', 'skin_shade',
               'natural_style', 'shape', 'hair_length', 'skin_hue', 'eyelid']]
# data_y = data[["hue", 'center', 'fringe', 'texture', 'length', 'purity', 'shade']]
data_y = data[["fringe"]]
# print(data_x.shape)
# print(data_y.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.1, random_state=42)
# print(X_train.shape)
# print(X_test.shape)
# print(y_train.shape)
# print(y_test.shape)


from sklearn.neural_network import MLPClassifier

model = MLPClassifier(hidden_layer_sizes=(50, 50, 50, 30), activation='relu', solver='adam', max_iter=3000,alpha=0.001)

model.fit(X_train, y_train)

# res = model.predict(X_test)
print(model.score(X_test, y_test))
print(model.classes_)
# print(acc)
