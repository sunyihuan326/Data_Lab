# coding:utf-8 
'''
created on 2018/12/11

@author:sunyihuan
'''
import sys
import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['http://baolei.shuwtech.com'],
    # http_auth=('elastic', 'passwd'),
    port=39200
)


def es_search(index, business_version="", button_index="", current_page=""):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "business_version": business_version
                        }
                    }
                    ,
                    {
                        "term": {
                            "button_index": button_index
                        }
                    }
                    ,
                    {
                        "term": {
                            "current_page": current_page
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

    res = es.search(index=index, body=body, size=10000)  # 获取测试端数据
    res_hits = res["hits"]["hits"]
    print(len(res_hits))

    print(res)


if __name__ == "__main__":
    index_release = 'user_behavior_log_prod_20180723'  # 线上index
    index_dev = 'user_behavior_log_dev_20180723'  # 测试index

    business_version = "V4.8.0"
    button_index = "li_ji_gou_mai"
    current_page = "fa_lang_ying_xiao_luo_di"

    es_search(index_dev, business_version, button_index, current_page)
