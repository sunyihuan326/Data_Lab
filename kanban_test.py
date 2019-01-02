# coding:utf-8
'''
created on 2018/12/12

@author:sunyihuan
'''

from pymongo import MongoClient
import datetime
import time
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://baolei.shuwtech.com'],
    # http_auth=('elastic', 'passwd'),
    port=39200
)


def get_day_uv(index, gt_time, lt_time):
    body1 = {
        "size": 10000,
        "collapse": {
            "field": "page_viewer"
        },
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "action_timestamp": {
                                "gt": gt_time,  # >gt_time
                                "lt": lt_time  # <lt_time
                            }
                        }
                    },
                    {
                        "term": {
                            "business_line": "meiyezhushou"
                        }
                    }
                ],
                "should": []
            }
        },
        "sort": {
            "action_timestamp": {  # 根据action_timestamp字段升序排序
                "order": "desc"  # asc升序，desc降序
            }
        }

    }
    res = es.search(index=index, body=body1)  # 获取测试端数据

    return res["hits"]["hits"]


def seven_day_stylist(gt_time, lt_time):
    '''
    获取发型师的myid
    :return:
    '''
    index_release = 'user_behavior_log_prod_20180723'  # 线上index
    stylists = []
    res_hits = get_day_uv(index_release, gt_time, lt_time)
    for i in range(len(res_hits)):
        try:
            page_viewer = res_hits[i]["_source"]["page_viewer"]
            if page_viewer not in stylists:
                stylists.append(page_viewer)
        except:
            print("error")

    return stylists


def ts2utcdatetime(ts):
    '''
    时间戳转化为日期，支持mongodb中的日期保存
    :param ts:
    :return:
    '''
    return datetime.datetime.utcfromtimestamp(ts)


def change_type(s_data):
    '''
    转换数据类型，输出为list
    :param s_data:
    :return:
    '''
    s_data = list(map(int, s_data))
    return s_data


def changjing_data(day_time_start):
    '''
    返回某一日数据看板中的数据
    :param day_time_start: 日期，格式为："2018-12-21"
    :return:
    sheji_st：设计沟通场景日活,
    sheji_st_vip：设计沟通场景VIP日活,
    poster_st：营销拓客场景日活,
    poster_st_vip：营销拓客场景VIP日活,
    stylists：美助app日活,
    stylists_yes：美助app昨日留存, 
    stylists_vip：美助app中VIP日活
    '''
    mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                       unicode_decode_error_handler='ignore')  # 链接mongodb
    mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
    mdb = mdbs['sheji']  # 链接sheji

    start_time = day_time_start + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))

    vip_st = mdb.wxuser.distinct("_id", {"expireat": {"$gt": star_timeStamp}})  # vip列表
    vip_st = change_type(vip_st)

    poster_st = mdb.log_poster.distinct("uid",
                                        {"ctime": {"$gt": star_timeStamp, "$lt": star_timeStamp + 86400}})  # 使用海报发型师uv

    fxcl_st = mdb.log_material.distinct("uid",
                                        {"ctime": {"$gt": star_timeStamp, "$lt": star_timeStamp + 86400}})  # 使用海报发型师uv

    poster_st = set(poster_st) | set(fxcl_st)
    poster_st = change_type(poster_st)

    stylist_one = mdb.xm_hair_scheme.distinct("myid",
                                              {"utime": {"$gte": ts2utcdatetime(star_timeStamp + 0 * 86400),
                                                         "$lt": ts2utcdatetime(star_timeStamp + 86400)},
                                               "is_finish": 1})  # 完成订单发型师
    stylist_one = change_type(stylist_one)
    stylist_t = mdb.xm_good_hair.distinct("myid",
                                          {"utime": {"$gte": ts2utcdatetime(star_timeStamp + 0 * 86400),
                                                     "$lt": ts2utcdatetime(star_timeStamp + 86400)},
                                           "status": 1})  # 收藏发型的发型师
    stylist_t = change_type(stylist_t)

    sheji_st = set(stylist_one) | set(stylist_t)  # 设计沟通场景发型师日活
    sheji_st = change_type(sheji_st)

    sheji_st_vip = (set(stylist_one) | set(stylist_t)) & set(vip_st)  # 设计沟通场景发型师VIP日活

    poster_st_vip = set(vip_st) & set(poster_st)  # 使用海报发型师中VIP的人数

    stylists = seven_day_stylist(star_timeStamp, star_timeStamp + 86400)  # 美业助手app当日uv

    stylists_yestday = seven_day_stylist(star_timeStamp - 86400, star_timeStamp)  # 美业助手app昨日uv
    vip_st = list(map(str, vip_st))

    stylists_yes = set(stylists) & set(stylists_yestday)  # 次日留存人数

    stylists_vip = set(stylists) & set(vip_st)  # 美业助手app当日VIP日活

    return sheji_st, sheji_st_vip, poster_st, poster_st_vip, stylists, stylists_yes, stylists_vip


if __name__ == "__main__":
    day_time_start = "2019-1-2"
    sheji_st, sheji_st_vip, poster_st, poster_st_vip, stylists, stylists_yes, stylists_vip = changjing_data(
        day_time_start)

    print("设计沟通人数", len(sheji_st))
    print("设计沟通VIP人数", len(sheji_st_vip))
    print("使用海报人数", len(poster_st))
    print("使用海报VIP人数", len(poster_st_vip))
    print("今日uv", len(stylists))
    print("昨日留存", len(stylists_yes))
    print("今日uv_vip", len(stylists_vip))
