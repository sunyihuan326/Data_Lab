# coding:utf-8 
'''
created on 2019/1/11

@author:sunyihuan
'''
from sklearn import datasets

iris = datasets.load_iris()  # 导入数据集
X = iris.data  # 获得其特征向量
y = iris.target  # 获得样本label

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

from sklearn.neural_network import MLPClassifier

model = MLPClassifier(activation='relu', solver='adam', alpha=0.0001)

model.fit(X_train, y_train)

res = model.predict(X_test)
acc = 0
for i in range(len(res)):
    if res[i] == y_test[i]:
        acc += 1.0 / len(res)

print(acc)
