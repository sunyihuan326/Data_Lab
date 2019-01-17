# coding:utf-8 
'''
created on 2019/1/16

@author:sunyihuan
'''
from utils import connect_mongodb_sheji, day2timestamp, timeStamp2day, ts2utcdatetime, list_change_type

mdb = connect_mongodb_sheji()


def scheme_static(start_time):
    scheme = mdb.xm_hair_scheme.find({"is_finish": 1, "finish_time": {"$gt": start_time}})
    print(scheme.count())
    sc_f = {}
    sc_name = {}
    for sc in scheme:
        feature = sc["principle"]["feature"]

        fs = ""
        for f in feature.keys():
            fs = fs + f + str(feature[f])
        if fs not in sc_f.keys():
            sc_f[fs] = 1
        else:
            sc_f[fs] += 1

        name = sc["principle"]["name"]
        if name not in sc_name.keys():
            sc_name[name] = 1
        else:
            sc_name[name] += 1

    return sc_f, sc_name


def write2excel(name):
    import xlwt
    w = xlwt.Workbook()
    sh = w.add_sheet("name")
    sh.write(0, 0, "name")
    sh.write(0, 1, "count")
    for i in range(len(name)):
        sh.write(i + 1, 0, name[i][0])
        sh.write(i + 1, 1, name[i][1])
    w.save("/Users/sunyihuan/Desktop/scheme_name.xls")


if __name__ == "__main__":
    start_time = day2timestamp("2018-10-01")
    sc_f, sc_name = scheme_static(ts2utcdatetime(start_time))
    sc = sorted(sc_f.items(), key=lambda x: x[1], reverse=True)
    name = sorted(sc_name.items(), key=lambda x: x[1], reverse=True)
    print(sc)
    print(name)
    # for sn in sc_name.keys():
    #     print(sn.split("心")[1])
    fa_count = {}
    for ss in sc_name.keys():
        fachang = ss.split("心")[1]
        if fachang not in fa_count.keys():
            fa_count[fachang] = sc_name[ss]
        else:
            fa_count[fachang] += sc_name[ss]
    fa_count = sorted(fa_count.items(), key=lambda x: x[1], reverse=True)
    print(fa_count)

    # write2excel(name)
