# coding:utf-8 
'''
created on 2018/12/11

@author:sunyihuan
'''
import sys
import json
from utils import connect_mongodb_sheji, connect_es

es = connect_es()


def distinct_es_search(index, business_version="", button_index="", current_page=""):
    body1 = {
        "size": 0,
        "aggs": {
            "uv": {
                "cardinality": {
                    "field": "page_viewer"
                }
            }
        },
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "action_timestamp": {
                                "gt": "1541779200",  # >1541779200
                                "lt": "1544371200"  # <=1544371200
                            }
                        }
                    },

                    {
                        "term": {
                            "business_version": business_version
                        }
                    }
                    ,
                    # {
                    #     "term": {
                    #         "button_index": button_index
                    #     }
                    # }
                    # ,
                    # {
                    #     "term": {
                    #         "current_page": current_page
                    #     }
                    # }
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

    return res["aggregations"]


def es_search(index, business_version="", button_index="", current_page=""):
    body1 = {
        "size": 0,
        "aggs": {
            "pv": {
                "cardinality": {
                    "field": "_id"
                }
            }
        },
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "action_timestamp": {
                                "gt": "1541779200",  # >1541779200
                                "lt": "1544371200"  # <=1544371200
                            }
                        }
                    },
                    {
                        "term": {
                            "business_version": business_version
                        }
                    }
                    # ,
                    # {
                    #     "term": {
                    #         "button_index": button_index
                    #     }
                    # }
                    # ,
                    # {
                    #     "term": {
                    #         "current_page": current_page
                    #     }
                    # }
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

    return res["aggregations"]


if __name__ == "__main__":
    index_release = 'user_behavior_log_prod_20180723'  # 线上index
    index_dev = 'user_behavior_log_dev_20180723'  # 测试index

    business_version = "V4.6.0"
    # button_index = "li_ji_gou_mai"
    # current_page = "fa_lang_ying_xiao_luo_di"

    res_uv = distinct_es_search(index_release, business_version)
    res_hits = es_search(index_release, business_version)

    print(res_uv)
    print(res_hits)
