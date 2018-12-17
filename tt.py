# coding:utf-8 
'''
created on 2018/12/12

@author:sunyihuan
'''


def dict_sorted(d):
    d_new = sorted(d.items(), key=lambda item: item[1], reverse=True)
    return d_new


#
# d = {"ddd": 2, "345": 89, "43dfs": 3}
#
# a = dict_sorted(d)
a = 2889 + 1665 + 1433 + 1100 + 500 + 4812 + 2000 + 2000 + 700 * 2 + 3700 + 1500 + 14340
print(a)
