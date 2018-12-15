# coding:utf-8 
'''
最近7天uv，注册的时间（发型师b）
created on 2018/12/14

@author:sunyihuan
'''
import sys
import json
from elasticsearch import Elasticsearch
from tqdm import tqdm

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


def seven_day_stylist():
    index_release = 'user_behavior_log_prod_20180723'  # 线上index
    stylists = []
    for k in range(7):
        gt_time = k * 86400 + 1544112000
        lt_time = (k + 1) * 86400 + 1544112000

        res_hits = get_day_uv(index_release, gt_time, lt_time)
        print(len(res_hits))
        for i in range(len(res_hits)):
            try:
                page_viewer = res_hits[i]["_source"]["page_viewer"]
                if page_viewer not in stylists:
                    stylists.append(page_viewer)
            except:
                print("error")
        print("finish:", k)

    return stylists


# stylists = seven_day_stylist()

from pymongo import MongoClient

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji


def get_stylist_ctime(uid):
    s = mdb.wxuser.find({"_id": uid})
    s_ctime = 0
    for ss in s:
        try:
            s_ctime = ss["ctime"]
        except:
            pass

    return s_ctime


def stylist_ctime_distibution():
    stylists = seven_day_stylist()
    one_month_nums = 0
    six_month_nums = 0
    twelve_month_nums = 0
    g_year = 0

    for i in tqdm(range(len(stylists))):
        stylist = stylists[i]
        try:
            ctime = get_stylist_ctime(int(stylist))
            if ctime > 0:
                if ctime > 1542124800:
                    one_month_nums += 1
                elif ctime > 1528905600 and ctime <= 1542124800:
                    six_month_nums += 1
                elif ctime > 1513180800 and ctime <= 1528905600:
                    twelve_month_nums += 1
                else:
                    g_year += 1
        except:
            print("error:::::::::::::::{}******".format(stylist))

    return g_year, twelve_month_nums, six_month_nums, one_month_nums


if __name__ == "__main__":
    print(1)
    # g_year, twelve_month_nums, six_month_nums, one_month_nums = stylist_ctime_distibution()
    #
    # all_nums = g_year + twelve_month_nums + six_month_nums + one_month_nums
    # print("近7天总uv数：", all_nums)
    #
    # print("一年前注册：{:.2%}".format(g_year / all_nums))
    # print("6个月至一年前注册：{:.2%}".format(twelve_month_nums / all_nums))
    # print("1-6个月前注册：{:.2%}".format(six_month_nums / all_nums))
    # print("最近1个月注册：{:.2%}".format(one_month_nums / all_nums))
