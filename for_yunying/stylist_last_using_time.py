# coding:utf-8 
'''
created on 2019/3/22

@author:sunyihuan
'''
from utils import connect_mongodb_sheji, connect_es, timeStamp2day

mdb = connect_mongodb_sheji()
es = connect_es()


def get_uid(mobile):
    '''
    获取该手机号码的uid
    :param mobile:
    :return:
    '''
    uid = mdb.wxuser.find_one({"mobile": str(mobile)})
    return uid["_id"]


def desc_using(index, uid):
    body = {
        "size": 100,
        "query": {
            "term": {
                "page_viewer": uid
            }
        },
        "sort": {
            "action_timestamp": {  # 根据action_timestamp字段升序排序
                "order": "desc"  # asc升序，desc降序
            }
        }

    }

    res = es.search(index=index, body=body)  # 获取测试端数据
    return res["hits"]["hits"]


def last_using_time(index, mobile):
    uid = get_uid(mobile)
    t = desc_using(index, uid)
    t = t[0]['_source']['action_timestamp']
    return timeStamp2day(t + 28800)


if __name__ == "__main__":
    index = 'user_behavior_log_prod_20180723'  # 线上index
    print(last_using_time(index, 15700070500))
