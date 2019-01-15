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


mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji

if __name__ == "__main__":
    day_time_start = "2018-12-21"
    start_time = day_time_start + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))
    wx_or = mdb.wx_order.find({"status": 1, "utime": {"$gt": 1546272000}})
    amount = 0
    for wx in wx_or:
        amount += int(wx["price"])
    print(amount)

    # vip_st = mdb.wxuser.distinct("_id", {"expireat": {"$gt": star_timeStamp}})  # vip列表
    #
    # poster_st = mdb.log_poster.distinct("uid",
    #                                     {"ctime": {"$gt": star_timeStamp, "$lt": star_timeStamp + 86400}})  # vip列表
    #
    # stylist_one = mdb.xm_hair_scheme.distinct("myid",
    #                                           {"utime": {"$gte": ts2utcdatetime(star_timeStamp + 0 * 86400),
    #                                                      "$lt": ts2utcdatetime(star_timeStamp + 86400)},
    #                                            "is_finish": 1})  # 完成订单发型师
    # stylist_t = mdb.xm_good_hair.distinct("myid",
    #                                       {"utime": {"$gte": ts2utcdatetime(star_timeStamp + 0 * 86400),
    #                                                  "$lt": ts2utcdatetime(star_timeStamp + 86400)},
    #                                        "status": 1})  # 收藏发型的发型师
    #
    # sheji_st = set(stylist_one) | set(stylist_t)
    # sheji_st_vip = (set(stylist_one) | set(stylist_t)) & set(vip_st)
    # print("设计沟通人数", len(sheji_st))
    # print("设计沟通VIP人数", len(sheji_st_vip))
    #
    # poster_st_vip = set(vip_st) & set(poster_st)
    # print("使用海报人数", len(poster_st))
    # print("使用海报VIP人数", len(poster_st_vip))
    #
    # stylists = seven_day_stylist(star_timeStamp, star_timeStamp + 86400)
    # stylists_yestday = seven_day_stylist(star_timeStamp - 86400, star_timeStamp)
    #
    # vip_st = list(map(str, vip_st))
    # print("今日uv", len(stylists))
    # print("昨日留存", len(set(stylists) & set(stylists_yestday)))
    #
    # print("今日uv_vip", len(set(stylists) & set(vip_st)))
    from sklearn.neural_network import MLPClassifier
    MLPClassifier()