# coding:utf-8 
'''
created on 2018/11/10

@author:sunyihuan
'''
from pymongo import MongoClient

mongo_path = "dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com"
client = MongoClient(mongo_path, 3717)
db = client.sheji
