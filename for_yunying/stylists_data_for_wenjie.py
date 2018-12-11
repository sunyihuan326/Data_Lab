# coding:utf-8 
'''
created on 2018/12/11

@author:sunyihuan
'''

from pymongo import MongoClient
import datetime
import time

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji

stylists_kehus = len(mdb.xm_relation.distinct("myid"))
kehus = mdb.xm_relation.find().count()
kehus_distinct = len(mdb.xm_relation.distinct("cid"))
stylists_kehu_renzheng = len(mdb.xm_relation.distinct("myid", {"cert_status": 1}))
kehus_renzheng = len(mdb.xm_relation.distinct("cid", {"cert_status": 1}))

print("有客户的发型师数量:", stylists_kehus)
print("有进行客户好友认证的发型师数量:", stylists_kehu_renzheng)
print("有多少已认证的客户数量:", kehus_renzheng)
print("总客户数量:", kehus_distinct)
print("有客户的发型师平均有多少个客户数量=总客户数量/有客户的发型师数量：", float(kehus_distinct / stylists_kehus))
