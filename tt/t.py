# coding:utf-8 
'''
created on 2019/4/20

@author:sunyihuan
'''
import time

now = time.time()
l = now - 15 * 86400
r = now - 14 * 86400

i = 1554483600
if i > l and i < r:
    print("1")
else:
    print("00000")
