# coding:utf-8 
'''
created on 2018/12/11

@author:sunyihuan
'''

from pymongo import MongoClient
import datetime
import time
import xlwt
from for_yunying.hair_need_data import ts2utcdatetime, id2ObjectId

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji

w = xlwt.Workbook()
sh = w.add_sheet("need_data")
