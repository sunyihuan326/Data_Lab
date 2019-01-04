# coding:utf-8 
'''
created on 2019/1/3

@author:sunyihuan
'''

import xlwt
from utils import connect_es, connect_mongodb_sheji, ts2utcdatetime, day2timestamp

mdb = connect_mongodb_sheji()  # 链接sheji


def get_stylists(star_timeStamp):
    stylists = mdb.customer_card_after.distinct("myid",
                                                {"ctime": {"$gt": ts2utcdatetime(star_timeStamp + 0 * 86400),
                                                           "$lt": ts2utcdatetime(star_timeStamp + 86400)},
                                                 "status": 101})

    return stylists


def get_stylist_phone_vip(uid, star_timeStamp):
    '''
    获取发型师电话号码和VIP信息
    :param uid:
    :return:
    '''
    s = mdb.wxuser.find({"_id": uid})
    s_vip = "非vip"
    s_mobile = ""
    s_name = ""
    for ss in s:
        s_vip_time = ss["expireat"]
        s_mobile = ss["mobile"]
        print(s_mobile)
        try:
            s_name = ss["nickname"]
        except:
            pass
        if s_vip_time > star_timeStamp:
            s_vip = "vip"
        else:
            s_vip = "非vip"

    return s_vip, s_mobile, s_name


def get_vip_stylist_list():
    '''
    生成使用售后卡功能的VIP发型师名单，及电话号码
    :return:
    '''
    day_time_start = "2019-1-2"
    star_timeStamp = day2timestamp(day_time_start)

    stylists = get_stylists(star_timeStamp)

    print("使用售后卡人数：", len(stylists))
    print(stylists)
    w = xlwt.Workbook()
    sh = w.add_sheet("发型师信息")
    sh.write(0, 0, "姓名")
    sh.write(0, 2, "电话号码")
    sh.write(0, 1, "vip")

    for i, sy in enumerate(stylists):
        sy_id = int(sy)
        s_vip, s_mobile, s_name = get_stylist_phone_vip(sy_id, star_timeStamp)
        if s_vip == "vip":
            sh.write(i + 1, 0, s_name)
            sh.write(i + 1, 1, s_vip)
            sh.write(i + 1, 2, s_mobile)

    w.save("/Users/sunyihuan/Desktop/使用售后卡发型师.xls")


if __name__ == "__main__":
    get_vip_stylist_list()
