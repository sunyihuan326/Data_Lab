# coding:utf-8 
'''
created on 2018/12/5

@author:sunyihuan
'''
from pymongo import MongoClient
import time
from bson.objectid import ObjectId

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji


def twice_buy_vip():
    '''
    二次及以上购买vip人数
    :return:
    '''

    orders = mdb.wx_order.find({"status": 1})
    orders_count = {}
    t_count = 0
    for p in orders:
        try:
            u_id = p["uid"]
            if u_id not in orders_count.keys():
                orders_count[u_id] = 1
            else:
                orders_count[u_id] += 1
        except:
            pass
    for k in orders_count.keys():
        if orders_count[k] > 1:
            t_count += 1
    return t_count


def basic_data(start_time="2018-12-5", end_time="2019-01-01"):
    '''
    :param time_time:
    :return:
    '''
    start_time = start_time + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))

    end_time = end_time + " 23:59:59"
    end_timeArray = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    end_timeStamp = int(time.mktime(end_timeArray))

    vip_nums = mdb.wxuser.find({"expireat": {"$gte": star_timeStamp}}).count()
    mobile_nums = mdb.wxuser.find({"mobile": {"$gte": "1"}}).count()
    buy_vip_nums = len(mdb.wx_order.distinct("uid", {"status": 1}))
    print("已存入手机号码数： ", mobile_nums)
    print("购买过VIP人数： ", buy_vip_nums)
    print("当前VIP人数： ", vip_nums)
    one_month_expire = mdb.wxuser.find({"expireat": {"$gte": star_timeStamp, "$lt": end_timeStamp}}).count()
    print("一个月内到期的人数： ", one_month_expire)


if __name__ == "__main__":
    start_time = "2018-12-5"
    end_time = "2019-1-5"
    basic_data(start_time, end_time)

    t_count = twice_buy_vip()
    print("二次购买人数： ", t_count)
