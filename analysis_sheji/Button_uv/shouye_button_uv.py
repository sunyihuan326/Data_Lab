# coding:utf-8 
'''
created on 2019/1/7

@author:sunyihuan
'''
from utils import connect_es, day2timestamp

es = connect_es()


def shouye_button_uv(index, gt_time, lt_time, button_index):
    '''
    首页中头部七个按钮的点击uv
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
    start_time = day2timestamp("2019-1-13")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-1-14")  # 后一天的日期，转化为后一天0点时间戳

    xian_chang_uv = shouye_button_uv(index, start_time, end_time, "002")
    print("现场设计uv：", xian_chang_uv)
    fa_xing_ce_uv = shouye_button_uv(index, start_time, end_time, "003")
    print("发型册uv：", fa_xing_ce_uv)
    shou_hou_ka_uv = shouye_button_uv(index, start_time, end_time, "shou_hou")
    print("售后卡uv：", shou_hou_ka_uv)

    jin_ri_fa_xin_uv = shouye_button_uv(index, start_time, end_time, "jin_ri_fa_xing")
    print("今日发型uv：", jin_ri_fa_xin_uv)
    wo_de_fang_an_uv = shouye_button_uv(index, start_time, end_time, "wo_de_fang_an")
    print("我的方案uv：", wo_de_fang_an_uv)
    she_ji_da_sai_uv = shouye_button_uv(index, start_time, end_time, "she_ji_da_sai")
    print("设计大赛uv：", she_ji_da_sai_uv)
    tui_jian_hai_bao_uv = shouye_button_uv(index, start_time, end_time, "tui_jian_hai_bao")
    print("推荐海报uv：", tui_jian_hai_bao_uv)
