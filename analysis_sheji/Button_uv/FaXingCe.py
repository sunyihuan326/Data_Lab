# coding:utf-8 
'''
created on 2019/1/9

@author:sunyihuan
'''
from utils import connect_es, day2timestamp, ts2utcdatetime

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


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    start_time = day2timestamp("2019-1-9")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-1-10")  # 后一天的日期，转化为后一天0点时间戳

    faxingce_yemian_uv = faxingce_uv(index, start_time, end_time, "hairbook-001")
    print("发型册页面人数：", faxingce_yemian_uv)
    guanfang_ku_uv = button_uv(index, start_time, end_time, "007")
    print("官方发型册点击比例：{:.2%}".format(guanfang_ku_uv / faxingce_yemian_uv))
    zhuanshu_zuopin_uv = button_uv(index, start_time, end_time, "009")
    print("专属作品点击比例：{:.2%}".format(zhuanshu_zuopin_uv / faxingce_yemian_uv))
    jiahao_uv = button_uv(index, start_time, end_time, "014")
    print("+点击比例：{:.2%}".format(jiahao_uv / faxingce_yemian_uv))

    jinrifaxing_uv = button_uv(index, start_time, end_time, "jin_ri_fa_xing_geng_duo")
    print("今日发型分类点击比例：{:.2%}".format(jinrifaxing_uv / faxingce_yemian_uv))
    fengge_fenlei_uv = button_uv(index, start_time, end_time, "010")
    print("风格分类点击比例：{:.2%}".format(fengge_fenlei_uv / faxingce_yemian_uv))
    fachang_fenlei_uv = button_uv(index, start_time, end_time, "011")
    print("发长分类点击比例：{:.2%}".format(fachang_fenlei_uv / faxingce_yemian_uv))
    juandu_fenlei_uv = button_uv(index, start_time, end_time, "012")
    print("卷度分类点击比例：{:.2%}".format(juandu_fenlei_uv / faxingce_yemian_uv))
    fase_fenlei_uv = button_uv(index, start_time, end_time, "013")
    print("发色分类点击比例：{:.2%}".format(fase_fenlei_uv / faxingce_yemian_uv))

    guanfang_ce_uv = faxingce_uv(index, start_time, end_time, "hairbook-004")
    print("官方发型册页面人数：", guanfang_ce_uv)
