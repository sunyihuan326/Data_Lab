# coding:utf-8 
'''
专属作品页面中按钮uv统计
created on 2019/1/9

@author:sunyihuan
'''
from utils import connect_es, connect_mongodb_sheji, day2timestamp, ts2utcdatetime, list_change_type

mdb = connect_mongodb_sheji()
es = connect_es()


def zhuanShu_search(index, gt_time, lt_time):
    body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "action_timestamp": {
                                "gte": gt_time,  # >1541779200
                                "lt": lt_time  # <=1544371200
                            }
                        }
                    }
                    ,
                    {
                        "term": {
                            "current_page": "hairbook-003"
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

    return res["hits"]["hits"]


def uv_stylist(start_time, end_time):
    index = 'user_behavior_log_prod_20180723'  # 线上index
    res = zhuanShu_search(index, start_time, end_time)
    stylists = []
    for i in range(len(res)):
        try:
            page_viewer = res[i]["_source"]["page_viewer"]
            if page_viewer not in stylists:
                stylists.append(page_viewer)
        except:
            print(i)
    return stylists


def shangchuan_stylists(start_time, end_time):
    return mdb.xm_exclusive_products.distinct("myid", {"status": 1,
                                                       "utime": {"$gte": ts2utcdatetime(start_time),
                                                                 "$lt": ts2utcdatetime(end_time)}})


if __name__ == "__main__":
    start_time = day2timestamp("2019-1-1")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-1-9")  # 后一天的日期，转化为后一天0点时间戳
    uv_stylists_ = uv_stylist(start_time, end_time)
    shangchuan_stylists_uv = shangchuan_stylists(start_time, end_time)

    uv_stylists_ = list_change_type(int, uv_stylists_)
    shangchuan_stylists_uv = list_change_type(int, shangchuan_stylists_uv)

    print("作品上传页uv：", len(uv_stylists_))
    print("完成上传作品人数：", len(shangchuan_stylists_uv))

    print("作品上传页中完成上传的人数：", len(set(uv_stylists_) & set(shangchuan_stylists_uv)))

    print(set(shangchuan_stylists_uv) - set(uv_stylists_) & set(shangchuan_stylists_uv))
