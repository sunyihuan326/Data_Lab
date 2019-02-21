# coding:utf-8 
'''
created on 2019/1/15

@author:sunyihuan
'''
from utils import connect_es, connect_mongodb_sheji, day2timestamp, timeStamp2day

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
                    ,
                    # {
                    #     "term": {
                    #         "button_index": ""
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

    res = es.search(index=index, body=body)  # 获取测试端数据

    return res["aggregations"]['uv']['value']


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    start_time0 = day2timestamp("2019-2-13")  # 当日的日期，转化为当日0点时间戳
    for i in range(7):
        start_time = start_time0 + 86400 * i
        end_time = start_time + 86400
        haibao_uv = DaoHang_uv(index, start_time, end_time, "hai-bao")
        chaoliu_uv = DaoHang_uv(index, start_time, end_time, "fa-xing-chao-liu")
        print("日期:", str(timeStamp2day(start_time + 34000)).split(" ")[0])
        print("海报访问人数：", haibao_uv)
        print("发型潮流访问人数：", chaoliu_uv)
