# coding:utf-8 
'''
created on 2019/1/7

@author:sunyihuan
'''
from utils import connect_es, day2timestamp, timeStamp2day

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


def shouye_page_uv(index, gt_time, lt_time, current_page):
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


def save2excel(end_time):
    '''
    首页各按钮访问人数写入excel
    :param end_time: 截止时间，类型为时间戳
    :return:
    '''
    import xlwt

    w = xlwt.Workbook()
    sh = w.add_sheet("首页按钮访问")
    end_time0 = end_time
    sh.write(0, 0, "日期")
    sh.write(0, 1, "首页访问人数")
    sh.write(0, 2, "现场设计点击人数")
    sh.write(0, 3, "发型册点击人数")
    sh.write(0, 4, "售后卡点击人数")
    sh.write(0, 5, "今日发型点击人数")
    sh.write(0, 6, "设计大赛点击人数")
    sh.write(0, 7, "推荐海报点击人数")
    sh.write(0, 8, "我的方案点击人数")
    for i in range(22):
        end_time = end_time0 - i * 86400
        start_time = end_time - 86400

        shouye_uv = shouye_page_uv(index, start_time, end_time, "app-001")

        xian_chang_uv = shouye_button_uv(index, start_time, end_time, "002")
        fa_xing_ce_uv = shouye_button_uv(index, start_time, end_time, "003")
        shou_hou_ka_uv = shouye_button_uv(index, start_time, end_time, "shou_hou")

        jin_ri_fa_xin_uv = shouye_button_uv(index, start_time, end_time, "jin_ri_fa_xing")
        wo_de_fang_an_uv = shouye_button_uv(index, start_time, end_time, "wo_de_fang_an")
        she_ji_da_sai_uv = shouye_button_uv(index, start_time, end_time, "she_ji_da_sai")
        tui_jian_hai_bao_uv = shouye_button_uv(index, start_time, end_time, "tui_jian_hai_bao")

        sh.write(i + 1, 0, str(timeStamp2day(end_time - 43000)).split(" ")[0])
        sh.write(i + 1, 1, shouye_uv)
        sh.write(i + 1, 2, xian_chang_uv)
        sh.write(i + 1, 3, fa_xing_ce_uv)
        sh.write(i + 1, 4, shou_hou_ka_uv)
        sh.write(i + 1, 5, jin_ri_fa_xin_uv)
        sh.write(i + 1, 6, she_ji_da_sai_uv)
        sh.write(i + 1, 7, tui_jian_hai_bao_uv)
        sh.write(i + 1, 8, wo_de_fang_an_uv)
    w.save("/Users/sunyihuan/Desktop/首页按钮访问人数.xls")


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    start_time = day2timestamp("2019-3-6")  # 当日的日期，转化为当日0点时间戳
    end_time = day2timestamp("2019-3-7")  # 后一天的日期，转化为后一天0点时间戳

    shouye_uv = shouye_page_uv(index, start_time, end_time, "app-001")

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
