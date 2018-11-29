# coding:utf-8 
'''
created on 2018/11/29

@author:sunyihuan
'''
from pymongo import MongoClient
import time
from bson.objectid import ObjectId
import xlwt

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji

vote = mdb.design_game_vote.find({"myid": 140296, "ctime": {"$gte": 1543420800}})
w = xlwt.Workbook()
sh = w.add_sheet("vote_time")
v_count = {}
for v in vote:
    t = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(v["ctime"]))
    t = t.split(":")[0] + ":" + t.split(":")[1]
    if t not in v_count.keys():
        v_count[t] = 1
    else:
        v_count[t] = v_count[t] + 1

for i, k in enumerate(v_count.keys()):
    sh.write(i + 1, 0, k)
    sh.write(i + 1, 1, v_count[k])

w.save("/Users/sunyihuan/Desktop/100.xls")

# import matplotlib.pyplot as plt
#
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title('Scatter Plot')
# plt.xlabel('time')
# plt.ylabel('votes')
# ax1.scatter(v_count.keys(), v_count.values(), c='r', marker='s')
# plt.show()
