# coding:utf-8 
'''
created on 2018/12/5

@author:sunyihuan
'''

from utils import ts2utcdatetime, connect_mongodb_sheji, connect_es, day2timestamp

mdb = connect_mongodb_sheji()  # 链接sheji


def twice_buy_vip():
    '''
    二次及以上购买vip人数
    :return:
    '''
    orders = mdb.wx_order.find(
        {"status": 1, "type": {"$in": ['v12']}})
    orders_count = {}
    t_count = 0
    t_uid = []
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
            t_uid.append(k)
    return t_count, t_uid


def basic_data(start_time=1546272000, end_time=1548691200):
    '''
    基本数据查询
    :param start_time:起始时间，时间戳
    :param end_time:终止时间，时间戳
    :return:
    '''

    vip_nums = mdb.wxuser.find({"expireat": {"$gte": start_time}}).count()
    mobile_nums = mdb.wxuser.find({"mobile": {"$gte": "1"}}).count()
    buy_vip_nums = len(mdb.wx_order.distinct("uid", {"status": 1}))
    one_month_expire = mdb.wxuser.find({"expireat": {"$gte": start_time, "$lt": end_time}}).count()
    return mobile_nums, buy_vip_nums, vip_nums, one_month_expire


def orders_nums(start_time, end_time, platform=["wx", "ios", "android", "myzsvip"]):
    '''
    会员销售额
    :param start_time:开始时间
    :param end_time:结束时间
    :param platform:支付平台
    :return:
    '''
    # oders = mdb.wx_order.find(
    #     {"status": 1, "type": {"$in": ['v3', 'v1', 'v12', "v6_zs", "extension"]}, 'platform': {"$in": platform},
    #      "utime": {"$gte": start_time, "$lt": end_time}})
    oders = mdb.wx_order.find(
        {"status": 1, "type": {"$in": ['v3', 'v1', 'v12', "v6_zs", "extension"]},
         "utime": {"$gte": start_time, "$lt": end_time}})
    amounts = 0
    type = {}
    for o in oders:
        amounts += o["price"]
        try:
            uid = o["uid"]
            u = mdb.wxuser.find_one({"_id": uid})
            if "inline" in u.keys():
                if u["inline"] == 1:
                    amounts -= o["price"]
            typ = o["type"]
            if typ not in type.keys():
                type[typ] = 1
        except:
            print(o)
        else:
            type[typ] = type[typ] + 1
    return amounts, type


if __name__ == "__main__":
    start_time = "2019-3-1"
    end_time = "2019-3-31"
    start_time = day2timestamp(start_time)
    print(start_time)
    end_time = day2timestamp(end_time)
    print(end_time)
    #
    # mobile_nums, buy_vip_nums, vip_nums, one_month_expire = basic_data(start_time, end_time)
    # print("已存入手机号码人数： ", mobile_nums)
    # print("购买过VIP人数： ", buy_vip_nums)
    # print("当前VIP人数： ", vip_nums)
    # print("一个月内到期的人数： ", one_month_expire)
    #
    #
    # t_count, t_uid = twice_buy_vip()
    # print("二次购买人数： ", t_count)
    # print(t_uid)

    amounts, type = orders_nums(start_time, end_time)
    print("销售额： %.2f" % amounts)
