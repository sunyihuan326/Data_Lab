# coding:utf-8 
'''
created on 2019/3/18

@author:sunyihuan
'''
# if None:
#     print(1)
# else:
#     print(2)
#
# import sys
#
#
# def fibonacci(n):
#     a, b, counters = 0, 1, 0
#     while True:
#         if counters > n:
#             return
#         yield a
#         a, b = b, a + b
#         counters += 1
#
#
# f = fibonacci(10)
# while True:
#     try:
#         print(next(f), end="   ")
#     except StopIteration:
#         sys.exit()

s = lambda x1, x2: x1 * x2
print(s(3, 4))

s0 = [3, 4, 2.0, 6, 9]
s0.pop(0)
print(s0)

import re

line = "Cats are smarter than dogs"
matchObj = re.match(r'(.*) are (.*) .* .*', line, re.M | re.I)
if matchObj:
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
else:
    print("No match!!")


