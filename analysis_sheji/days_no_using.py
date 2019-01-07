# coding:utf-8 
'''
created on 2019/1/4

@author:sunyihuan
'''
from utils import connect_mongodb_sheji, connect_es, day2timestamp, list_change_type

es = connect_es()
mdb = connect_mongodb_sheji()


def get_vip_list(start_time):
    vip_list = mdb.wxuser.distinct("_id", {"expireat": {"$gt": start_time}})
    return vip_list


def one_day_uv_list(start_time, index):
    body = {
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
                                "gt": start_time,  # >gt_time
                                "lt": start_time + 1 * 86400  # <lt_time
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
    res = es.search(index=index, body=body)  # 获取测试端数据
    res = res["hits"]["hits"]
    uv_list = []
    for i in range(len(res)):
        try:
            page_viewer = res[i]["_source"]["page_viewer"]
            if page_viewer not in uv_list:
                uv_list.append(page_viewer)
        except:
            print("error")
    return uv_list


def get_days_uv_list(end_time, day_nums, index):
    uv_days_list = []
    for i in range(day_nums):
        start_time = end_time - (i + 1) * 86400
        uv_list = one_day_uv_list(start_time, index)
        uv_days_list = set(uv_days_list) | set(uv_list)
    return uv_days_list


def day_nums_no_using(days_nums):
    index_release = 'user_behavior_log_prod_20180723'
    end_time = "2019-1-5"
    end_time = day2timestamp(end_time)
    uv_list = get_days_uv_list(end_time, days_nums, index_release)

    vip_list = get_vip_list(end_time)

    vip_list = list_change_type(str, vip_list)
    print("vip总人数",len(vip_list))
    no_using_list = set(vip_list) - set(uv_list)
    return no_using_list


if __name__ == "__main__":
    days_nums = 7
    no_using_list_7 = day_nums_no_using(7)
    no_using_list_15 = day_nums_no_using(15)
    no_using_list_30 = day_nums_no_using(30)
    print(len(no_using_list_7))
    print(len(no_using_list_15))
    print(len(no_using_list_30))
