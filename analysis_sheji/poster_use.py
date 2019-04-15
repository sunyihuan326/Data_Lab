# coding:utf-8 
'''
海报使用人数
created on 2018/11/22

@author:sunyihuan
'''
from utils import connect_mongodb_sheji, connect_es, ts2utcdatetime, day2timestamp

mdb = connect_mongodb_sheji()  # 链接sheji


def poster_uv_everyday(day_time):
    '''
    海报使用次数、人数
    :param day_time:某一天，格式为："2018-11-21"
    :return: posters_pv：海报使用次数, poster_uv：海报使用人数
    '''

    star_timeStamp = day2timestamp(day_time)

    posters = mdb.log_poster.distinct("uid",
                                      {"ctime": {"$gte": star_timeStamp, "$lt": star_timeStamp + 86400}})  # 使用海报的uid
    poster_uv = len(posters)  # 海报使用人数

    posters_pv = mdb.log_poster.find(
        {"ctime": {"$gte": star_timeStamp, "$lt": star_timeStamp + 86400}}).count()  # 海报使用次数

    return posters_pv, poster_uv


# print(poster_uv_everyday('2018-11-23'))


def poster_uv_everyday_distribution(day_time):
    '''
    海报使用次数、人数
    :param day_time:某一天，格式为："2018-11-21"
    :return: posters_pv：海报使用次数, poster_uv：海报使用人数
    '''

    star_timeStamp = day2timestamp(day_time)

    posters = mdb.log_poster.find({"ctime": {"$gte": star_timeStamp, "$lt": star_timeStamp + 86400}})
    posters_types_count = {}
    temp_count = 0
    for p in posters:
        temp_id = p["temp_id"]
        temp = mdb.temp_poster.find({"_id": temp_id})
        for t in temp:
            try:
                if t["sub_type"] not in posters_types_count.keys():
                    posters_types_count[t["sub_type"]] = 1
                else:
                    posters_types_count[t["sub_type"]] += 1
            except:
                temp_count += 1
    print(temp_count)

    return posters_types_count


def get_everday_poster_using(day_time):
    '''
    log_poster_count中计算uv、pv
    :param day_time: 要查询的天数
    :return:
    '''
    posters = mdb.log_poster_count.find({"datenum": day_time})
    p_uv = 0
    p_pv = 0
    for p in posters:
        p_uv += p["users"]
        p_pv += p["takes"]
    return p_uv, p_pv


def poster_using_time():
    '''
    海报使用时间分布
    '''

    import time
    posters_pv = mdb.log_poster.find({"ctime": {"$gte": 1514736000}})
    posters_time_using = {}
    for p in posters_pv:
        p_time = p["ctime"]
        p_time_str = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(p_time))
        p_time_ = str(p_time_str.split(":")[0]).split(" ")[-1]
        if str(p_time_) not in posters_time_using.keys():
            posters_time_using[p_time_] = 1
        else:
            posters_time_using[p_time_] += 1

    return posters_time_using


def data_bar(data_classes, data_value, data_label):
    import matplotlib.pyplot as plt
    plt.bar(data_classes, data_value, label=data_label)
    plt.legend()

    plt.xlabel('time')
    plt.ylabel('value')
    plt.show()


# print(poster_uv_everyday_distribution("2019-3-31"))
# print(poster_uv_everyday("2019-3-31"))

print(get_everday_poster_using("20190331"))
#
# poster_using_time = poster_using_time()
# data_classes = poster_using_time.keys()
# data_value = poster_using_time.values()
# data_label = "poster_using_time"
# data_bar(data_classes, data_value, data_label)
