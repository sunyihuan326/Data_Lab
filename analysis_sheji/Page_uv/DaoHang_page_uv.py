# coding:utf-8 
'''
created on 2019/1/7

@author:sunyihuan
'''
from utils import connect_es, connect_mongodb_sheji, day2timestamp

es = connect_es()


def DaoHang_uv(index, gt_time, lt_time, current_page):
    body = {
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
                                "gt": gt_time,  # >1541779200
                                "lt": lt_time  # <=1544371200
                            }
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

    res = es.search(index=index, body=body)  # 获取测试端数据

    return res["aggregations"]['uv']['value']


def five_daohang_page_uv(index, gt_time, lt_time):
    page_uv = {}
    for current_page in ["app-001", "jin-ri-ying-xiao", "hai-bao", "ke_hu", "wo-de"]:
        page_name = "{}_uv".format(current_page)
        uv = DaoHang_uv(index, gt_time, lt_time, current_page)
        page_uv[page_name] = uv
    return page_uv


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    start_time = day2timestamp("2019-1-6")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-1-7")  # 后一天的日期，转化为后一天0点时间戳

    print(five_daohang_page_uv(index, start_time, end_time))
