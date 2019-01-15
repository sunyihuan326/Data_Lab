# coding:utf-8 
'''
created on 2019/1/3

@author:sunyihuan
'''
import datetime


# 时间戳转化为日期，支持mongodb中的日期保存
def ts2utcdatetime(ts):
    '''
    时间戳转化为日期，支持mongodb中的日期保存
    :param ts:
    :return:
    '''
    return datetime.datetime.utcfromtimestamp(ts)


# 链接mongodb（仅可以查询，不能删除、修改、插入）
def connect_mongodb_sheji():
    '''
    链接mongodb（仅可以查询，不能删除、修改、插入）
    :return:
    '''
    from pymongo import MongoClient

    mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                       unicode_decode_error_handler='ignore')  # 链接mongodb
    mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
    mdb = mdbs['sheji']  # 链接sheji
    return mdb


# 链接es
def connect_es():
    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        ['http://baolei.shuwtech.com'],
        # http_auth=('elastic', 'passwd'),
        port=39200
    )
    return es


# id 转换objectid
def id2ObjectId(_id):
    from bson.objectid import ObjectId
    if not _id:
        return _id

    if isinstance(_id, ObjectId):
        return _id
    if str(_id).isdigit():
        return int(_id)
    else:
        return ObjectId(_id)


# 日期转换成时间戳
def day2timestamp(day_time_start):
    '''
    日期转换成时间戳
    :param day_time_start: 日期，格式为：2019-1-1
    :return:
    '''
    import time
    start_time = day_time_start + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))
    return star_timeStamp


def list_change_type(typ, s_data):
    '''
    转换数据类型，输出为list
    :param typ:要转换的目标类型，如：int、str
    :param s_data:
    :return:
    '''
    s_data = list(map(typ, s_data))
    return s_data


def timeStamp2day(timeStamp):
    '''
    时间戳转成日期
    :param timeStamp: 时间戳
    :return:
    '''
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    return otherStyleTime  # 2013--10--10 15:40:00
