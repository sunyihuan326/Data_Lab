# coding:utf-8 
'''
created on 2018/12/11

@author:sunyihuan
'''

from pymongo import MongoClient
import datetime
import time
import xlwt
from for_yunying.hair_need_data import ts2utcdatetime, id2ObjectId

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji


def dict_sorted(d):
    d_new = sorted(d.items(), key=lambda item: item[1], reverse=True)
    return d_new


def get_n_range(stylists):
    if len(stylists) >= 100:
        n_r = 100
    else:
        n_r = len(stylists)
    return n_r


def get_finished_stylist_list(day_time):
    '''
    自2018-11-11开始
    近30天完成订单用户中，完成订单次数前100排名（名字/电话/剪发价位/地址）
    近30天完成订单用户中，完成订单次数前100排名（名字/电话/剪发价位/地址）
    :return:day_time：开始日期，格式 "2018-11-11"
    '''
    w = xlwt.Workbook()
    sh_wangluo = w.add_sheet("网络设计")
    sh_xianchang = w.add_sheet("现场设计")

    # day_time = "2018-11-11"
    start_time = day_time + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))
    needs_finish = mdb.xm_hair_scheme.find({"is_finish": 1, "ctime": {"$gte": ts2utcdatetime(star_timeStamp),
                                                                      "$lt": ts2utcdatetime(
                                                                          star_timeStamp + 30 * 86400)}})

    wangluo_stylist = {}
    xianchang_stylist = {}
    for n_f in needs_finish:
        need_id = id2ObjectId(n_f["need_id"])
        needs_p = mdb.xm_hair_need.find({"_id": need_id})
        for n in needs_p:
            my_id = n["myid"]
            if n["source"] == 2:
                if my_id not in wangluo_stylist.keys():
                    wangluo_stylist[my_id] = 1
                else:
                    wangluo_stylist[my_id] += 1

            elif n["source"] == 1:
                if my_id not in xianchang_stylist.keys():
                    xianchang_stylist[my_id] = 1
                else:
                    xianchang_stylist[my_id] += 1

    wangluo_stylist = dict_sorted(wangluo_stylist)
    xianchang_stylist = dict_sorted(xianchang_stylist)

    wangluo_n = get_n_range(wangluo_stylist)
    xianchang_n = get_n_range(xianchang_stylist)

    sh_wangluo.write(0, 0, "姓名")
    sh_wangluo.write(0, 1, "手机号码")
    sh_wangluo.write(0, 2, "剪发价格")
    sh_wangluo.write(0, 3, "发廊地址")
    sh_wangluo.write(0, 4, "单数")
    for i in range(wangluo_n):
        my_id = wangluo_stylist[i][0]
        my_nums = wangluo_stylist[i][1]
        sh_wangluo.write(i + 1, 4, my_nums)
        try:
            s_p = mdb.person.find({"uid": my_id})
            for s__ in s_p:
                if s__["user_name"] != "":
                    sh_wangluo.write(i + 1, 1, s__["mobile"])
                    sh_wangluo.write(i + 1, 0, s__["user_name"])
                    sh_wangluo.write(i + 1, 2, s__["cut_price"])
                    sh_wangluo.write(i + 1, 3, s__["salon_position"])
        except:
            print(my_id)

    sh_xianchang.write(0, 0, "姓名")
    sh_xianchang.write(0, 1, "手机号码")
    sh_xianchang.write(0, 2, "剪发价格")
    sh_xianchang.write(0, 3, "发廊地址")
    sh_xianchang.write(0, 4, "单数")
    for i_ in range(xianchang_n):
        my_id__ = xianchang_stylist[i_][0]
        my_nums_ = xianchang_stylist[i_][1]
        sh_xianchang.write(i_ + 1, 4, my_nums_)
        try:
            s_p = mdb.person.find({"uid": my_id__})
            for s__ in s_p:
                if s__["user_name"] != "":
                    sh_xianchang.write(i_ + 1, 0, s__["user_name"])
                    sh_xianchang.write(i_ + 1, 1, s__["mobile"])
                    sh_xianchang.write(i_ + 1, 2, s__["cut_price"])
                    sh_xianchang.write(i_ + 1, 3, s__["salon_position"])
        except:
            print(my_id__)
    w.save("/Users/sunyihuan/Desktop/{}近30天完成订单发型师名单（前100）.xls".format(day_time))


if __name__ == "__main__":
    # get_finished_stylist_list()
    day_time = "2018-11-26"
    get_finished_stylist_list(day_time)
