# coding:utf-8 
'''
created on 2019/3/2

@author:sunyihuan
'''
from utils import connect_es, day2timestamp

es = connect_es()


def shidai_page_uv(index, gt_time, lt_time, button_index):
    '''
    试戴访问
    :param index: 数据库名称
    :param gt_time: 时间区间下限
    :param lt_time:  时间区间上限
    :param button_index: 按钮名称
    :return:button_index在该时间段内的uv数
    '''

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
                            "current_page": "fa-xing-shi-dai"
                        }
                    },
                    {
                        "term": {
                            "button_index": button_index
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


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    start_time = day2timestamp("2019-3-1")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-3-2")  # 后一天的日期，转化为后一天0点时间戳

    huanyihuan_uv = shidai_page_uv(index, start_time, end_time, "huan_yi_huan")

    fenxiang_uv = shidai_page_uv(index, start_time, end_time, "fen_xiang_gui_mi")

    print(huanyihuan_uv)
    print(fenxiang_uv)
