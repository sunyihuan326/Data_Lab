# coding:utf-8 
'''
created on 2019/1/3

@author:sunyihuan
'''
import datetime


# 时间戳转化为日期，支持mongodb中的日期保存
def ts2utcdatetime(ts):
    '''
    时间戳转化为日期，支持mongodb中的日期保存
    :param ts:
    :return:
    '''
    return datetime.datetime.utcfromtimestamp(ts)


# 链接mongodb（仅可以查询，不能删除、修改、插入）
def connect_mongodb_sheji():
    '''
    链接mongodb（仅可以查询，不能删除、修改、插入）
    :return:
    '''
    from pymongo import MongoClient

    mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                       unicode_decode_error_handler='ignore')  # 链接mongodb
    mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
    mdb = mdbs['sheji']  # 链接sheji
    return mdb


# 链接es
def connect_es():
    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        ['http://baolei.shuwtech.com'],
        # http_auth=('elastic', 'passwd'),
        port=39200
    )
    return es


# id 转换objectid
def id2ObjectId(_id):
    from bson.objectid import ObjectId
    if not _id:
        return _id

    if isinstance(_id, ObjectId):
        return _id
    if str(_id).isdigit():
        return int(_id)
    else:
        return ObjectId(_id)


# 日期转换成时间戳
def day2timestamp(day_time_start):
    '''
    日期转换成时间戳
    :param day_time_start: 日期，格式为：2019-1-1
    :return:
    '''
    import time
    start_time = day_time_start + " 00:00:00"
    start_timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    star_timeStamp = int(time.mktime(start_timeArray))
    return star_timeStamp


def list_change_type(typ, s_data):
    '''
    转换数据类型，输出为list
    :param typ:要转换的目标类型，如：int、str
    :param s_data:
    :return:
    '''
    s_data = list(map(typ, s_data))
    return s_data


def timeStamp2day(timeStamp):
    '''
    时间戳转成日期
    :param timeStamp: 时间戳
    :return:
    '''
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
    return otherStyleTime  # 2013--10--10 15:40:00


def get_stylist_phone_vip(uid, star_timeStamp):
    '''
    获取发型师电话号码和VIP信息
    :param uid:
    :return:
    '''
    mdb = connect_mongodb_sheji()
    s = mdb.wxuser.find({"_id": uid})
    s_vip = "非vip"
    s_mobile = ""
    s_name = ""
    for ss in s:
        s_vip_time = ss["expireat"]
        s_mobile = ss["mobile"]
        print(s_mobile)
        try:
            s_name = ss["nickname"]
        except:
            s_name = mdb.person.find_one({"uid": uid})["user_name"]
        if s_vip_time > star_timeStamp:
            s_vip = "vip"
        else:
            s_vip = "非vip"

    return s_vip, s_mobile, s_name


def stylists_2_excel(stylists, star_timeStamp, save_file_name):
    '''
    生成发型师名单，及电话号码,并存储在save_file_name中
    :param stylists:发型师列表
    :param star_timeStamp:时间戳，判断是否为vip
    :param save_file_name:保存文件名称
    :return:
    '''
    import xlwt
    w = xlwt.Workbook()
    sh = w.add_sheet("发型师信息")
    sh.write(0, 0, "姓名")
    sh.write(0, 2, "电话号码")
    sh.write(0, 1, "vip")

    for i, sy in enumerate(stylists):
        sy_id = int(sy)
        s_vip, s_mobile, s_name = get_stylist_phone_vip(sy_id, star_timeStamp)
        sh.write(i + 1, 0, s_name)
        sh.write(i + 1, 1, s_vip)
        sh.write(i + 1, 2, s_mobile)

    w.save(save_file_name)
