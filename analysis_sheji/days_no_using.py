# coding:utf-8 
'''
created on 2019/1/4

@author:sunyihuan
'''
import xlwt
import tqdm
from utils import connect_mongodb_sheji, connect_es, day2timestamp, list_change_type

es = connect_es()
mdb = connect_mongodb_sheji()


def timeStamp2date(timeStamp):
    '''
    时间戳转化为日期
    :param timeStamp:
    :return:
    '''
    import time
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    return str(otherStyleTime).split(" ")[0]


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


def day_nums_no_using(end_time, days_nums):
    index_release = 'user_behavior_log_prod_20180723'

    uv_list = get_days_uv_list(end_time, days_nums, index_release)

    vip_list = get_vip_list(end_time)

    vip_list = list_change_type(str, vip_list)
    print("vip总人数:", len(vip_list))
    no_using_list = set(vip_list) - set(uv_list)
    return no_using_list


def Correcting_user(no_using_list, end_time, days_nums):
    wx_user = mdb.wxuser.distinct("_id", {"mobile": {"$exists": True}})
    p_user = mdb.person.distinct("uid", {"user_name": {"$exists": True, "$ne": ""}})
    o_user = mdb.wx_order.distinct("uid", {"utime": {"$lt": end_time - 86400 * days_nums}})
    no_using = set(list_change_type(str, wx_user)) & set(no_using_list) & set(list_change_type(str, o_user)) & set(
        list_change_type(str, p_user))
    return no_using


def write2excel(no_using_list):
    w = xlwt.Workbook()
    sh = w.add_sheet("未使用发型师名单", cell_overwrite_ok=True)
    sh.write(0, 0, "编号")
    sh.write(0, 1, "名字")
    sh.write(0, 2, "电话")
    sh.write(0, 3, "最近一次购习vip时间")
    sh.write(0, 4, "花费金额")
    sh.write(0, 5, "会员到期时间")
    c = 0
    for i, st in enumerate(no_using_list):

        myid = int(st)

        try:
            user = mdb.wxuser.find_one({"_id": myid})
            try:
                name = user["nickname"]
            except:
                name = mdb.person.find_one({"uid": myid})["user_name"]
            tell = user["mobile"]

            ex_time = user["expireat"]
            ex_time = timeStamp2date(ex_time)

            import pymongo
            order = mdb.wx_order.find({"uid": myid, "type": {"$ne": "mc"}, "status": 1}).sort("_id",
                                                                                              pymongo.DESCENDING).limit(
                1)
            try:
                for o in order:
                    buy_time = o["utime"]
                    price = o["price"]
                buy_time = timeStamp2date(buy_time)
            except:
                continue
            if int(tell) > 0:
                sh.write(i + 1, 0, i + 1)
                sh.write(i + 1, 1, name)  # 写入名字
                sh.write(i + 1, 2, tell)  # 写入手机号码
                sh.write(i + 1, 3, buy_time)  # 写入购买时间
                sh.write(i + 1, 4, price)  # 写入购买金额
                sh.write(i + 1, 5, ex_time)  # 写入到期时间
        except:
            print(i, myid)
            c += 1
            print(c)

    w.save("/Users/sunyihuan/Desktop/近30天未使用app名单.xls")


if __name__ == "__main__":
    end_time = "2019-1-14"
    end_time = day2timestamp(end_time)
    # no_using_list_7 = day_nums_no_using(7)
    # no_using_list_15 = day_nums_no_using(15)
    no_using_list_30 = day_nums_no_using(end_time, 30)
    no_using = Correcting_user(no_using_list_30, end_time, 30)
    print(len(no_using))
    # print("7日未登陆app人数:", len(no_using_list_7))
    # print("15日未登陆app人数:", len(no_using_list_15))
    print("30日未登陆app人数:", len(no_using_list_30))
    write2excel(no_using)
