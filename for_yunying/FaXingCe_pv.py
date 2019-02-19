# coding:utf-8 
'''
created on 2019/2/13

@author:sunyihuan
'''
from utils import connect_es, day2timestamp, ts2utcdatetime, timeStamp2day

es = connect_es()


def faxingce_uv(index, gt_time, lt_time, current_page):
    '''
    发型册页面uv
    :param index:
    :param gt_time:
    :param lt_time:
    :return:
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


def button_uv(index, gt_time, lt_time, button_index):
    '''
    发型师各按钮的点击uv
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
                            "button_index": button_index
                        }
                    }
                    ,
                    {
                        "term": {
                            "current_page": "hairbook-001"
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


def write2excel(index, end_time, days, current_page):
    import xlwt
    w = xlwt.Workbook()
    sh = w.add_sheet("发型册访问人数")
    sh.write(0, 0, "日期")
    sh.write(0, 1, "访问人数")
    end_time0 = day2timestamp(end_time)
    for i in range(days):
        end_time = end_time0 - i * 86400
        faxingce_yemian_uv = faxingce_uv(index, end_time - 86400, end_time, current_page)
        day_time = str(timeStamp2day(end_time - 43000)).split(" ")[0]
        sh.write(i + 1, 0, day_time)
        sh.write(i + 1, 1, faxingce_yemian_uv)

    w.save("/Users/sunyihuan/Desktop/发型册访问人数.xls")


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    # start_time = day2timestamp("2019-1-9")  # 当日的日期，转化为当日0点时间戳
    # 后一天的日期，转化为后一天0点时间戳
    end_time = "2019-2-13"

    write2excel(index, end_time, 30, "hairbook-001")
    faxingce_yemian_uv = faxingce_uv(index, 1549900800 - 86400, 1549900800, "hairbook-001")
    print(faxingce_yemian_uv)
