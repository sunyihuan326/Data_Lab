# coding:utf-8 
'''
created on 2018/11/10

@author:sunyihuan
'''
from pymongo import MongoClient
import time
from bson.objectid import ObjectId

mdbs = MongoClient('dds-bp1c30e6691173a41935-pub.mongodb.rds.aliyuncs.com', 3717,
                   unicode_decode_error_handler='ignore')  # 链接mongodb
mdbs.admin.authenticate('root', 'mongo2018Swkj', mechanism='SCRAM-SHA-1')  # 账号密码认证
mdb = mdbs['sheji']  # 链接sheji


# c_ =mdb.person.find({"level": {'$ne': ""}}).count()
# print(c_)

# id 转换objectid
def id2ObjectId(_id):
    if not _id:
        return _id

    if isinstance(_id, ObjectId):
        return _id
    if str(_id).isdigit():
        return int(_id)
    else:
        return ObjectId(_id)


def get_cut_styles_distribution():
    '''
    获得各风格的人数
    :return: 各风格的总数，
    风格有：
    【"沙宣风格", "标榜风格", "日式风格", "托尼盖风格", "短发匠人", "染烫高手"，"创意剪发"，"韩式造型"，"私人定制"，"欧美造型"，"经典剪裁"】
    对应标签为：sx,bb,rs,tng,df,tr,cyj,hs,srdz,omzx,jdjc
    计数标签为：sx_count,bb_count,rs_count,tng_count,df_count,tr_count,cyj_count,hs_count,srdz_count,omzx_count,jdjc_count
    '''

    sx_count = 0
    bb_count = 0
    rs_count = 0
    tng_count = 0
    df_count = 0
    tr_count = 0
    cyj_count = 0
    hs_count = 0
    srdz_count = 0
    omzx_count = 0
    jdjc_count = 0
    sx = "沙宣风格"
    bb = "标榜风格"
    rs = "日式风格"
    tng = "托尼盖风格"
    df = "短发匠人"
    tr = "染烫高手"
    cyj = "创意剪发"
    hs = "韩式造型"
    srdz = "私人定制"
    omzx = "欧美造型"
    jdjc = "经典剪裁"
    c_ = mdb.person.find({"work_year": {'$gt': "0"}})
    for s in c_:
        if sx in s["cut_styles"]:
            sx_count += 1
        if bb in s["cut_styles"]:
            bb_count += 1
        if rs in s["cut_styles"]:
            rs_count += 1
        if tng in s["cut_styles"]:
            tng_count += 1
        if df in s["cut_styles"]:
            df_count += 1
        if tr in s["cut_styles"]:
            tr_count += 1
        if cyj in s["cut_styles"]:
            cyj_count += 1
        if jdjc in s["cut_styles"]:
            jdjc_count += 1
        if hs in s["cut_styles"]:
            hs_count += 1
        if srdz in s["cut_styles"]:
            srdz_count += 1
        if omzx in s["cut_styles"]:
            omzx_count += 1

    cut_styles = [sx_count, bb_count, rs_count, tng_count, df_count, tr_count, cyj_count, hs_count,
                  srdz_count, omzx_count, jdjc_count]
    return cut_styles


def get_work_years_distribution():
    '''
    :return: work_years_count：每个工作年限的人数
    '''
    work_years_count = {}
    stylists = mdb.person.find({"work_year": {'$gt': "0"}})
    for s in stylists:
        wy = s["work_year"]
        if wy not in work_years_count.keys():
            work_years_count[wy] = 1
        else:
            work_years_count[wy] = work_years_count[wy] + 1

    return work_years_count


def work_years_numbers(work_years_count):
    '''
    输出各工作年限段总人数
    :param work_years_count: 每工作年限的人数，由get_work_years_distribution()获得
    :return:
    count_13：1-3年的人数
    count_45：4-5年的人数
    count_69：6-9年的人数
    count_1015：10-15年的人数
    count_1625：16-25年的人数
    count_2645：25-45年的人数
    count_46：46年以上的人数
    '''
    count_13 = 0
    count_45 = 0
    count_69 = 0
    count_1015 = 0
    count_1625 = 0
    count_2645 = 0
    count_46 = 0
    for k in work_years_count.keys():
        if int(k) > 0 and int(k) <= 3:
            count_13 = count_13 + work_years_count[k]
        elif int(k) > 3 and int(k) <= 5:
            count_45 += work_years_count[k]
        elif int(k) > 5 and int(k) <= 9:
            count_69 += work_years_count[k]
        elif int(k) > 10 and int(k) <= 15:
            count_1015 += work_years_count[k]
        elif int(k) > 16 and int(k) <= 25:
            count_1625 += work_years_count[k]
        elif int(k) > 25 and int(k) <= 45:
            count_2645 += work_years_count[k]
        else:
            count_46 += work_years_count[k]
    return count_13, count_45, count_69, count_1015, count_1625, count_2645, count_46


def get_slon_and_stylists():
    '''
    获取发廊和对应发型师总数
    :return: slons_count：发廊数，stylists_count：发型师总数
    '''
    slon_and_stylists = mdb.salon_relation.find({"status": 1})
    slon_stylist = {}
    for ss in slon_and_stylists:
        slons = str(ss["sid"])
        if slons not in slon_stylist.keys():
            slon_stylist[slons] = 1
        else:
            slon_stylist[slons] = slon_stylist[slons] + 1
    slons_count = len(slon_stylist.keys())
    stylists_count = sum(slon_stylist.values())
    return slons_count, stylists_count


def levels_distribution():
    leves_count = {}
    stylists = mdb.person.find({"level": {'$ne': ""}})
    for s in stylists:
        level_s = s["level"]
        if level_s not in leves_count.keys():
            leves_count[level_s] = 1
        else:
            leves_count[level_s] = leves_count[level_s] + 1
    return leves_count


def work_start_time_distribution():
    work_start_count = {}
    stylists = mdb.person.find({"work_start": {'$ne': ""}})
    for s in stylists:
        w_s = s["work_start"]
        if w_s not in work_start_count.keys():
            work_start_count[w_s] = 1
        else:
            work_start_count[w_s] = work_start_count[w_s] + 1
    return work_start_count


def work_end_time_distribution():
    work_end_count = {}
    stylists = mdb.person.find({"work_end": {'$ne': ""}})
    for s in stylists:
        w_s = s["work_end"]
        if w_s not in work_end_count.keys():
            work_end_count[w_s] = 1
        else:
            work_end_count[w_s] = work_end_count[w_s] + 1
    return work_end_count


def work_time_distribution():
    work_end_count = {}
    stylists = mdb.person.find({"work_end": {'$ne': ""}, "work_start": {'$ne': ""}})
    for s in stylists:
        try:
            w_s_s = s["work_start"]
            w_e_s = s["work_end"]
            work_time = str(int(w_e_s.split(":")[0]) - int(w_s_s.split(":")[0]))
            if work_time not in work_end_count.keys():
                work_end_count[work_time] = 1
            else:
                work_end_count[work_time] = work_end_count[work_time] + 1
        except:
            print(s["work_start"])
    return work_end_count
