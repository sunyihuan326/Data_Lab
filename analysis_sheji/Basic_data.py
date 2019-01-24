# coding:utf-8 
'''
created on 2018/12/5

@author:sunyihuan
'''

import time
from utils import ts2utcdatetime, connect_mongodb_sheji, connect_es, day2timestamp

mdb = connect_mongodb_sheji()  # 链接sheji


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
    star_timeStamp = day2timestamp(start_time)
    end_timeStamp = day2timestamp(end_time)

    vip_nums = mdb.wxuser.find({"expireat": {"$gte": star_timeStamp}}).count()
    mobile_nums = mdb.wxuser.find({"mobile": {"$gte": "1"}}).count()
    buy_vip_nums = len(mdb.wx_order.distinct("uid", {"status": 1}))
    one_month_expire = mdb.wxuser.find({"expireat": {"$gte": star_timeStamp, "$lt": end_timeStamp}}).count()
    return mobile_nums, buy_vip_nums, vip_nums, one_month_expire


def orders_nums(start_time, end_time):
    '''
    销售额
    :param start_time:
    :param end_time:
    :return:
    '''
    oders = mdb.wx_order.find(
        {"status": 1, "type": {"$in": ['v3', 'v1', 'v12']},
         "utime": {"$gte": start_time, "$lt": end_time}})
    amounts = 0
    type = {}
    for o in oders:
        amounts += o["price"]
        typ = o["type"]
        if typ not in type.keys():
            type[typ] = 1
        else:
            type[typ] = type[typ] + 1
    return amounts, type


if __name__ == "__main__":
    # start_time = "2018-1-1"
    # end_time = "2019-1-1"
    # mobile_nums, buy_vip_nums, vip_nums, one_month_expire = basic_data(start_time, end_time)
    # print("已存入手机号码人数： ", mobile_nums)
    # print("购买过VIP人数： ", buy_vip_nums)
    # print("当前VIP人数： ", vip_nums)
    # print("一个月内到期的人数： ", one_month_expire)
    #
    # t_count = twice_buy_vip()
    # print("二次购买人数： ", t_count)
    amounts, type = orders_nums(1514736000, 1546272000)
    print(
        amounts
    )
    # platform = ["wx", "ios", "android", "myzsvip"]
    # for p in platform:
    #     amounts, type = orders_nums(1514736000, 1546272000)
    #     print("{}销售额： %.2f".format(p) % amounts)
    #     print("销售类型：", type)
