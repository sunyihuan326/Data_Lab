# coding:utf-8 
'''
created on 2018/11/22

@author:sunyihuan
'''
from pymongo import MongoClient
import time
from bson.objectid import ObjectId

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji


def poster_uv_everyday(day_time):
    '''
    海报使用次数、人数
    :param day_time:某一天，格式为："2018-11-21"
    :return: posters_pv：海报使用次数, poster_uv：海报使用人数
    '''
    start_time = day_time + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))

    end_time = day_time + " 23:59:59"
    end_timeArray = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    end_timeStamp = int(time.mktime(end_timeArray))

    posters = mdb.log_poster.distinct("uid", {"ctime": {"$gte": star_timeStamp, "$lt": end_timeStamp}})  # 使用海报的uid
    poster_uv = len(posters)  # 海报使用人数

    posters_pv = mdb.log_poster.find({"ctime": {"$gte": star_timeStamp, "$lt": end_timeStamp}}).count()  # 海报使用次数

    return posters_pv, poster_uv


print(poster_uv_everyday('2018-11-22'))
