# coding:utf-8 
'''
created on 2019/1/3

@author:sunyihuan
'''

import xlwt
from utils import connect_es, connect_mongodb_sheji, ts2utcdatetime, day2timestamp

mdb = connect_mongodb_sheji()  # 链接sheji


def get_card_nums(star_timeStamp, end_timStamp):
    '''
    售后卡生成情况，生成数量、被领取量
    :param star_timeStamp:开始时间，时间戳
    :param end_timStamp:结束时间，时间戳
    :return:
    all_cards_nums：完成的售后卡数量
    coustomer_get_cards_nums：被顾客领取的数量
    '''
    all_cards_nums = mdb.customer_card_after.find({"ctime": {"$gt": ts2utcdatetime(star_timeStamp),
                                                             "$lt": ts2utcdatetime(end_timStamp)},
                                                   "status": 101}).count()
    coustomer_get_cards_nums = mdb.customer_card_after.find({"ctime": {"$gt": ts2utcdatetime(star_timeStamp),
                                                                       "$lt": ts2utcdatetime(end_timStamp)},
                                                             "status": 101, "is_get": 1}).count()
    return all_cards_nums, coustomer_get_cards_nums


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
            s_name = mdb.person.find_one({"uid": uid})["user_name"]
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
    w = xlwt.Workbook()
    sh = w.add_sheet("发型师信息")

    day_time_start = "2019-1-10"
    star_timeStamp0 = day2timestamp(day_time_start)
    print(star_timeStamp0)
    for k in range(7):
        star_timeStamp = star_timeStamp0 + k * 86400

        stylists = get_stylists(star_timeStamp)

        print("使用售后卡人数：", len(stylists))
        print(stylists)

        import datetime
        dateArray = datetime.datetime.utcfromtimestamp(star_timeStamp + 36000)
        otherStyleTime = dateArray.strftime("%Y--%m--%d")

        sh.write(0, 4 * k + 0, otherStyleTime)

        sh.write(1, 4 * k + 0, "姓名")
        sh.write(1, 4 * k + 1, "电话号码")
        sh.write(1, 4 * k + 2, "vip")

        for i, sy in enumerate(stylists):
            sy_id = int(sy)
            s_vip, s_mobile, s_name = get_stylist_phone_vip(sy_id, star_timeStamp)

            if s_vip == "vip":
                sh.write(i + 2, 4 * k + 0, s_name)
                sh.write(i + 2, 4 * k + 2, s_vip)
                sh.write(i + 2, 4 * k + 1, s_mobile)

    w.save("/Users/sunyihuan/Desktop/使用售后卡发型师.xls")


if __name__ == "__main__":
    # get_vip_stylist_list()
    start_time = "2019-1-27"
    end_time = "2019-1-28"
    start_time = day2timestamp(start_time)
    end_time = day2timestamp(end_time)
    all_cards_nums, coustomer_get_cards_nums = get_card_nums(start_time, end_time)
    print("售后卡总数量：", all_cards_nums)
    print("被领取数量：", coustomer_get_cards_nums)
