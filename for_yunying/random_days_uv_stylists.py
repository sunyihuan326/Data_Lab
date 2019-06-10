# coding:utf-8 
'''

5月10日到6月10日，随机25天均使用app的发型师id列表

created on 2019/6/10

@author:sunyihuan
'''
from utils import connect_es
import random

es = connect_es()


def one_day_uv_list(start_time, index):
    '''
    每日uv列表，获取发型师的id
    :param start_time: 开始时间，一般为1天的0点
    :param index: es链接的index
    :return:
    '''
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


def get_stylists():
    '''
    获取发型师列表
    :return: uv_st：发型师列表,list格式
    '''
    index = 'user_behavior_log_prod_20180723'  # 线上index
    alist = random.sample(range(1, 30), 25)
    s_time_0 = 1560096000 - alist[0] * 86400 - 86400
    uv_st = one_day_uv_list(s_time_0, index)

    for k in range(len(alist[1:])):
        s_time = 1560096000 - alist[k + 1] * 86400 - 86400
        uv_s = one_day_uv_list(s_time, index)

        uv_st = list(set(uv_st) & set(uv_s))

    return uv_st

# uv_stylists = get_stylists()
# print(len(uv_stylists))
# print(uv_stylists)
