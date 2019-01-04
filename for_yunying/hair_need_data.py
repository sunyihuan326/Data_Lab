# coding:utf-8 
'''
查询网络设计订单量，发型师方案完成量等
created on 2018/12/6

@author:sunyihuan
'''

from pymongo import MongoClient
import datetime
import time
from bson.objectid import ObjectId
import xlwt
from utils import connect_mongodb_sheji, connect_es, day2timestamp, id2ObjectId, ts2utcdatetime, list_change_type

mdb = connect_mongodb_sheji()  # 链接sheji


def b_schemes(start_time):
    '''
    b端发型师订单完成量
    :param start_time: 当日时间，格式为时间戳
    :return: 这一天中的已完成订单量（needs_finish_nums）、已完成中网络设计订单量（needs_finish_wangluo）、已完成中现场设计订单量（needs_finish_xianchang），
             未完成订单量（needs_not_finish_nums）、未完成中网络设计订单量（needs_not_finish_wangluo）、未完成中现场设计订单量（needs_not_finish_xianchang）
    '''
    needs_finish = mdb.xm_hair_scheme.find({"is_finish": 1, "ctime": {"$gte": ts2utcdatetime(start_time),
                                                                      "$lt": ts2utcdatetime(
                                                                          start_time + 86400)}})

    needs_not_finish = mdb.xm_hair_scheme.find({"is_finish": 0, "ctime": {"$gte": ts2utcdatetime(start_time),
                                                                          "$lt": ts2utcdatetime(
                                                                              start_time + 86400)}})

    needs_finish_nums = needs_finish.count()
    needs_not_finish_nums = needs_not_finish.count()
    needs_finish_wangluo = 0
    needs_finish_xianchang = 0
    needs_not_finish_wangluo = 0
    needs_not_finish_xianchang = 0

    for n_f in needs_finish:
        need_id = id2ObjectId(n_f["need_id"])
        needs_p = mdb.xm_hair_need.find({"_id": need_id})
        for n in needs_p:
            if n["source"] == 2:
                needs_finish_wangluo += 1
            else:
                needs_finish_xianchang += 1

    for n_f in needs_not_finish:
        need_id = id2ObjectId(n_f["need_id"])
        needs_p = mdb.xm_hair_need.find({"_id": need_id})
        for n in needs_p:
            if n["source"] == 2:
                needs_not_finish_wangluo += 1
            else:
                needs_not_finish_xianchang += 1
    return needs_finish_nums, needs_finish_wangluo, needs_finish_xianchang, needs_not_finish_nums, needs_not_finish_wangluo, needs_not_finish_xianchang


#
w = xlwt.Workbook()
sh = w.add_sheet("need_data")


def get_hair_need_nums(day_time, n):
    '''
    查询从day_time开始，n天的数据量，并写入excel表格中
    :param day_time:开始的日期，格式为："2018-11-07"，str类型
    :param n:要查询的天数，格式为：30，int类型
    :return:
    '''
    star_timeStamp = day2timestamp(day_time)

    sh.write(0, 0, "日期")
    sh.write(0, 1, "网络设计总数(已经成功提交)")
    sh.write(0, 2, "网络设计拼团成功总数")
    sh.write(0, 3, "网络设计付费总单数")
    sh.write(0, 4, "网络设计免费总单数（已经成功提交）")
    sh.write(0, 5, "网络设计方案查看量")
    sh.write(0, 6, "网络设计超时订单量")

    sh.write(0, 8, "发型师方案完成量")
    sh.write(0, 9, "发型师方案完成量--网络设计")
    sh.write(0, 10, "发型师方案完成量--现场设计")
    sh.write(0, 11, "发型师方案未完成量")
    sh.write(0, 12, "发型师方案未完成量--网络设计")
    sh.write(0, 13, "发型师方案未成量--现场设计")

    for i in range(n):
        star_timeStamp_new = i * 86400 + star_timeStamp

        # 网络客总订单量
        needs = mdb.xm_hair_need.find(
            {"source": 2, "status": {"$gte": 100}, "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                                                             "$lt": ts2utcdatetime(
                                                                 star_timeStamp_new + 86400)}}).count()
        # 网络客拼团成功订单量
        needs_pintuan = mdb.xm_hair_need.find(
            {"source": 2, "status": {"$gte": 100}, "group": 1, "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                                                                         "$lt": ts2utcdatetime(
                                                                             star_timeStamp_new + 86400)}}).count()
        # 网络客付费订单量
        needs_fufei = mdb.xm_hair_need.find(
            {"source": 2, "status": {"$gte": 100}, "depth_price": {"$gt": 0},
             "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                       "$lt": ts2utcdatetime(
                           star_timeStamp_new + 86400)}}).count()

        needs_mianfei = mdb.xm_hair_need.find(
            {"source": 2, "status": {"$gte": 100}, "depth_price": 0,
             "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                       "$lt": ts2utcdatetime(
                           star_timeStamp_new + 86400)}}).count()
        # 网络客免费订单量
        needs_mianfei1 = mdb.xm_hair_need.find(
            {"source": 2, "status": {"$gte": 100}, "depth_price": {"$exists": False},
             "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                       "$lt": ts2utcdatetime(
                           star_timeStamp_new + 86400)}}).count()
        # 网络客方案被查看量
        needs_chakan = mdb.xm_hair_need.find(
            {"source": 2, "status": {"$gte": 100}, "is_check": 1, "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                                                                            "$lt": ts2utcdatetime(
                                                                                star_timeStamp_new + 86400)}}).count()
        # 网络客超时订单量
        needs_chaoshi = mdb.xm_hair_need.find(
            {"source": 2, "status": 104, "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                                                   "$lt": ts2utcdatetime(
                                                       star_timeStamp_new + 86400)}}).count()

        timeArray = time.localtime(star_timeStamp_new)
        otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        sh.write(i + 1, 0, str(otherStyleTime).split(" ")[0])
        sh.write(i + 1, 1, needs)
        sh.write(i + 1, 2, needs_pintuan)
        sh.write(i + 1, 3, needs_fufei)
        sh.write(i + 1, 4, int(needs_mianfei + needs_mianfei1))
        sh.write(i + 1, 5, needs_chakan)
        sh.write(i + 1, 6, needs_chaoshi)

        # 发型师订单数据
        needs_finish_nums, needs_finish_wangluo, needs_finish_xianchang, needs_not_finish_nums, needs_not_finish_wangluo, needs_not_finish_xianchang = b_schemes(
            star_timeStamp_new)

        sh.write(i + 1, 8, needs_finish_nums)
        sh.write(i + 1, 9, needs_finish_wangluo)
        sh.write(i + 1, 10, needs_finish_xianchang)
        sh.write(i + 1, 11, needs_not_finish_nums)
        sh.write(i + 1, 12, needs_not_finish_wangluo)
        sh.write(i + 1, 13, needs_not_finish_xianchang)

        print("finish", i)

    w.save("/Users/sunyihuan/Desktop/need_data—_{}.xls".format(day_time))


# get_hair_need_nums("2018-11-10", 30)


def days_one_week_stylists_info(day_time):
    '''
    近7天完成订单发型师名单
    :param day_time: 开始时间，格式为："2018-11-07"，str类型
    :return:
    '''
    w = xlwt.Workbook()
    star_timeStamp = day2timestamp(day_time)
    for i in range(7):
        star_timeStamp_new = i * 86400 + star_timeStamp
        needs_finish = mdb.xm_hair_scheme.find({"is_finish": 1, "ctime": {"$gte": ts2utcdatetime(star_timeStamp_new),
                                                                          "$lt": ts2utcdatetime(
                                                                              star_timeStamp_new + 86400)}})
        wangluo_stylist = []
        for n_f in needs_finish:
            need_id = id2ObjectId(n_f["need_id"])
            needs_p = mdb.xm_hair_need.find({"_id": need_id})
            for n in needs_p:
                if n["source"] == 2:
                    if n["myid"] not in wangluo_stylist:
                        wangluo_stylist.append(n["myid"])

        timeArray = time.localtime(star_timeStamp_new)
        otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        otherStyleTime = otherStyleTime.split(" ")[0]
        sheet_name = otherStyleTime.split("--")[0] + otherStyleTime.split("--")[1] + otherStyleTime.split("--")[2]
        sh = w.add_sheet("stylist_{}".format(sheet_name))
        sh.write(0, 0, "姓名")
        sh.write(0, 1, "手机号码")
        sh.write(0, 2, "剪发价格")
        sh.write(0, 3, "发廊地址")

        for i, k in enumerate(wangluo_stylist):
            try:
                s_p = mdb.person.find({"uid": k})

                for s__ in s_p:
                    if s__["user_name"] != "":
                        sh.write(i + 1, 0, s__["user_name"])
                        sh.write(i + 1, 1, s__["mobile"])
                        sh.write(i + 1, 2, s__["cut_price"])
                        sh.write(i + 1, 3, s__["salon_position"])
            except:
                print(k)
    w.save("/Users/sunyihuan/Desktop/已完成网络设计订单发型师名单（近7天）.xls")


days_one_week_stylists_info("2018-12-03")
