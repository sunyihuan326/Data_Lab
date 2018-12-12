# coding:utf-8 
'''
created on 2018/12/12

@author:sunyihuan
'''


def dict_sorted(d):
    d_new = sorted(d.items(), key=lambda item: item[1], reverse=True)
    return d_new


d = {"ddd": 2, "345": 89, "43dfs": 3}

a = dict_sorted(d)
print(a[0][0])