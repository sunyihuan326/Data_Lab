# coding:utf-8 
'''
created on 2019/3/9

@author:sunyihuan
'''
from utils import connect_es, day2timestamp, connect_mongodb_sheji, list_change_type

es = connect_es()
mdb = connect_mongodb_sheji()


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


def get_uv_stylists(index, start_time, end_time):
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


def get_vip_list(start_time):
    '''
    vip 发型师uid
    :param start_time:
    :return:
    '''
    stylists = []
    vip_s = mdb.wxuser.find({"expireat": {"$gte": start_time}})

    for v in vip_s:
        uid = v["_id"]
        if uid not in stylists:
            stylists.append(uid)
    return stylists


def days_vip_uv(index, start_time, end_time):
    '''
    vip日活
    :param index:
    :param start_time:
    :param end_time:
    :return:
    '''
    uv_s = get_uv_stylists(index, start_time, end_time)
    vip_s = get_vip_list(start_time)

    vip_uv = set(list_change_type(str, uv_s)) & set(list_change_type(str, vip_s))
    return vip_uv


def days_buy_nums(start_time, end_time):
    '''
    vip购买人数
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return:
    '''
    buy_vip_nums = len(mdb.wx_order.distinct("uid", {"status": 1, "utime": {"$gte": start_time, "$lt": end_time}}))
    return buy_vip_nums


def average_uv(index, endtime, n):
    '''
    vip近n天的平均日活、VIP购买量
    :param endtime: 当前时间
    :param n: 天数
    :return:
    '''
    av_vip_uv = 0
    bus_av = 0
    for i in range(30):
        end_time = endtime - i * 86400
        start_time = end_time - 86400

        vip_uv = days_vip_uv(index, start_time, end_time)
        buy_vip_nums = days_buy_nums(start_time, end_time)

        av_vip_uv += len(vip_uv)
        bus_av += buy_vip_nums

    return int(av_vip_uv / n), int(bus_av / n)


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    # start_time = day2timestamp("2019-2-10")  # 当日的日期，转化为当日0点时间戳
    end_time0 = day2timestamp("2019-3-11")  # 后一天的日期，转化为后一天0点时间戳
    av_vip_uv, bus_av = average_uv(index, end_time0, 30)
    print(av_vip_uv, bus_av)
