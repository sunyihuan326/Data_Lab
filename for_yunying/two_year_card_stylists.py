# coding:utf-8 
'''

购买两次年卡发型师

created on 2019/6/10

@author:sunyihuan
'''

from utils import connect_es, connect_mongodb_sheji, list_change_type
import xlwt

mdb = connect_mongodb_sheji()


def timeStamp2date(timeStamp):
    '''
    时间戳转化为日期
    :param timeStamp:
    :return:
    '''
    import time
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    return str(otherStyleTime).split(" ")[0]


def buy_2_year_cards_stylists():
    '''
    购买年卡排名，输出发型师id及购买次数
    :return:
    '''
    orders = mdb.wx_order.find(
        {"status": 1, "type": {"$in": ['v12']}})
    orders_count = {}
    for p in orders:
        try:
            u_id = p["uid"]
            if u_id not in orders_count.keys():
                orders_count[u_id] = 1
            else:
                orders_count[u_id] += 1
        except:
            pass
    return orders_count


orders_counts = buy_2_year_cards_stylists()
orders_counts = sorted(orders_counts.items(), key=lambda x: x[1], reverse=True)

orders_counts = orders_counts[:50]

# vip的stylist id
vip_st_list = [orders_counts[i][0] for i in range(len(orders_counts))]
vip_st_list = list_change_type(str, list(vip_st_list))

# 获取近一个月25日使用app的id
from for_yunying.random_days_uv_stylists import get_stylists

uv_st_list = list(get_stylists())


def write2excel():
    w = xlwt.Workbook()
    sh = w.add_sheet("购买多次发型师名单", cell_overwrite_ok=True)
    sh.write(0, 0, "编号")
    sh.write(0, 1, "名字")
    sh.write(0, 2, "购买次数")
    sh.write(0, 3, "电话")
    sh.write(0, 4, "最近一次购习vip时间")
    sh.write(0, 5, "花费金额")
    sh.write(0, 6, "会员到期时间")

    c = 0
    for i in range(len(orders_counts)):

        myid = int(orders_counts[i][0])

        try:
            user = mdb.wxuser.find_one({"_id": myid})
            try:
                name = user["nickname"]
            except:
                name = mdb.person.find_one({"uid": myid})["user_name"]
            tell = user["mobile"]

            ex_time = user["expireat"]
            ex_time = timeStamp2date(ex_time)

            import pymongo
            order = mdb.wx_order.find({"uid": myid, "type": {"$ne": "mc"}, "status": 1}).sort("_id",
                                                                                              pymongo.DESCENDING).limit(
                1)
            try:
                for o in order:
                    buy_time = o["utime"]
                    price = o["price"]
                buy_time = timeStamp2date(buy_time)
            except:
                continue
            if int(tell) > 0:
                sh.write(i + 1, 0, i + 1)
                sh.write(i + 1, 1, name)  # 写入名字
                sh.write(i + 1, 2, orders_counts[i][1])
                sh.write(i + 1, 3, tell)  # 写入手机号码
                sh.write(i + 1, 4, buy_time)  # 写入购买时间
                sh.write(i + 1, 5, price)  # 写入购买金额
                sh.write(i + 1, 6, ex_time)  # 写入到期时间
        except:
            print(i, myid)
            c += 1
            print(c)

    w.save("/Users/sunyihuan/Desktop/购买多次发型师名单.xls")

write2excel()
