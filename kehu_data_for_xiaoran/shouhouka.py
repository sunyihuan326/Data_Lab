# coding:utf-8 
'''
created on 2018/12/17

@author:sunyihuan
'''

import sys
import json
import xlwt
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://baolei.shuwtech.com'],
    # http_auth=('elastic', 'passwd'),
    port=39200
)


def get_day_uv(index):
    body1 = {
        "size": 10000,
        "collapse": {
            "field": "page_viewer"
        },
        "query": {
            "bool": {
                "must": [
                    # {
                    #     "range": {
                    #         "action_timestamp": {
                    #             "gt": gt_time,  # >gt_time
                    #             "lt": lt_time  # <lt_time
                    #         }
                    #     }
                    # },
                    {
                        "term": {
                            "business_line": "meiyezhushou"
                        }
                    },
                    {
                        "term": {
                            "current_page": "shang_chuan_ke_zhao"
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
    '''
    获取发型师的myid
    :return:
    '''
    index_release = 'user_behavior_log_prod_20180723'  # 线上index
    stylists = []
    res_hits = get_day_uv(index_release)
    for i in range(len(res_hits)):
        try:
            page_viewer = res_hits[i]["_source"]["page_viewer"]
            if page_viewer not in stylists:
                stylists.append(page_viewer)
        except:
            print("error")

    return stylists


# stylists = seven_day_stylist()


from pymongo import MongoClient

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji


def get_stylist_phone_vip(uid):
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
        try:
            s_vip_time = ss["expireat"]
            s_mobile = ss["mobile"]
            s_name = ss["nickname"]
            if s_vip_time > 1544630400:
                s_vip = "vip"
            else:
                s_vip = "非vip"

        except:
            pass
    return s_vip, s_mobile, s_name


def get_vip_stylist_list():
    '''
    生成使用售后卡功能的VIP发型师名单，及电话号码
    :return:
    '''
    stylists = seven_day_stylist()

    print("使用售后卡人数：", len(stylists))
    w = xlwt.Workbook()
    sh = w.add_sheet("发型师信息")
    sh.write(0, 0, "姓名")
    sh.write(0, 2, "电话号码")
    sh.write(0, 1, "vip")

    for i, sy in enumerate(stylists):
        sy_id = int(sy)
        s_vip, s_mobile, s_name = get_stylist_phone_vip(sy_id)
        if s_vip == "vip":
            sh.write(i + 1, 0, s_name)
            sh.write(i + 1, 1, s_vip)
            sh.write(i + 1, 2, s_mobile)

    w.save("/Users/sunyihuan/Desktop/使用售后卡发型师.xls")
