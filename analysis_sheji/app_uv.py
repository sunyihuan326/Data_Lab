# coding:utf-8 
'''
created on 2019/3/9

@author:sunyihuan
'''
from utils import connect_es, day2timestamp

es = connect_es()


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
                                "gte": gt_time,  # >gt_time
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


def get_stylists(index, start_time, end_time):
    stylists = []
    for i in range(24):
        t = int(start_time + ((end_time - start_time) / 24) * i)
        t_ = int(t + (end_time - start_time) / 24)
        res_hits = get_day_uv(index, t, t_)
        for i in range(len(res_hits)):
            try:
                page_viewer = res_hits[i]["_source"]["page_viewer"]
                if page_viewer not in stylists:
                    stylists.append(page_viewer)
            except:
                print("error")
    return stylists


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    start_time = day2timestamp("2019-3-8")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-3-9")  # 后一天的日期，转化为后一天0点时间戳
    #
    # print(get_day_uv(index, 1551801600, 1551798000))

    app_uv = get_stylists(index, start_time, end_time)
    print(len(app_uv))
