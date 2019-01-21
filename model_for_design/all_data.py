# coding:utf-8 
'''
created on 2019/1/17

@author:sunyihuan
'''
from utils import connect_mongodb_sheji, ts2utcdatetime, id2ObjectId
import xlwt
import pymongo

mdb = connect_mongodb_sheji()

# 2018年10月1日开始
wangluo_counts = mdb.xm_hair_need.find(
    {"status": 101, "source": 2, "ctime": {"$gt": ts2utcdatetime(1538323200)}}).count()

xianchang_counts = mdb.xm_hair_need.find(
    {"status": 101, "source": 1}).count()


def writeHead_wangluo(sh):
    sh.write(0, 2, "three_court")
    sh.write(0, 3, "face_length")
    sh.write(0, 4, "face_sense")
    sh.write(0, 5, "face_shape")
    sh.write(0, 6, "natural_style")
    sh.write(0, 7, "height")
    sh.write(0, 8, "weight")
    sh.write(0, 9, "hair_quantity")
    sh.write(0, 10, "like_change")
    sh.write(0, 11, "like_length")
    sh.write(0, 12, "accept_fringe")
    sh.write(0, 13, "like_rantang")
    sh.write(0, 14, "hair_care")
    sh.write(0, 15, "career")
    sh.write(0, 16, "like_dress")
    sh.write(0, 17, "like_leisure")
    sh.write(0, 18, "beauty_degree")
    sh.write(0, 19, "season")
    sh.write(0, 20, "skin_color")
    sh.write(0, 21, "skin_hue")
    sh.write(0, 22, "skin_shade")
    sh.write(0, 23, "hair_length")
    sh.write(0, 0, "id")
    sh.write(0, 1, "age")
    sh.write(0, 24, "career")


def writeHead_xianchang(sh):
    sh.write(0, 0, "id")
    sh.write(0, 1, "age")
    sh.write(0, 2, "three_court")
    sh.write(0, 3, "face_length")
    sh.write(0, 4, "face_sense")
    sh.write(0, 5, "face_shape")
    sh.write(0, 6, "skin_shade")
    sh.write(0, 7, "natural_style")
    sh.write(0, 8, "shape")
    sh.write(0, 9, "hair_length")
    sh.write(0, 10, "skin_hue")
    sh.write(0, 11, "eyelid")

    sh.write(0, 14, "hue")
    sh.write(0, 15, "center")
    sh.write(0, 16, "fringe")
    sh.write(0, 17, "texture")
    sh.write(0, 18, "length")
    sh.write(0, 19, "purity")
    sh.write(0, 20, "shade")


def write2excel_wangluo():
    wangluo = mdb.xm_hair_need.find(
        {"status": 101, "source": 2, "ctime": {"$gt": ts2utcdatetime(1538323200)}}).sort("_id", pymongo.DESCENDING)

    w = xlwt.Workbook()
    sh = w.add_sheet("wangluo_design0", cell_overwrite_ok=True)
    writeHead_wangluo(sh)
    for i, l in enumerate(wangluo):
        if i > 65530:
            break
        else:
            try:
                id = str(l["_id"])
                age = l["hair_info"]["age"]
                sh.write(i + 1, 0, id)
                sh.write(i + 1, 1, age)
                sh.write(i + 1, 2, l["hair_info"]["three_court"])
                sh.write(i + 1, 3, l["hair_info"]["face_length"])
                sh.write(i + 1, 4, l["hair_info"]["face_sense"])
                sh.write(i + 1, 5, l["hair_info"]["face_shape"])
                sh.write(i + 1, 6, l["hair_info"]["natural_style"])
                sh.write(i + 1, 7, l["hair_info"]["height"])
                sh.write(i + 1, 8, l["hair_info"]["weight"])
                sh.write(i + 1, 20, l["hair_info"]["skin_color"])
                sh.write(i + 1, 21, l["hair_info"]["skin_hue"])
                sh.write(i + 1, 22, l["hair_info"]["skin_shade"])
                sh.write(i + 1, 23, l["hair_info"]["hair_length"])
                sh.write(i + 1, 24, l["hair_info"]["career"])

                sh.write(i + 1, 10, l["hair_info"]["like_change"])
                sh.write(i + 1, 11, l["hair_info"]["like_length"])
                sh.write(i + 1, 12, l["hair_info"]["accept_fringe"])
                sh.write(i + 1, 13, l["hair_info"]["like_rantang"])
                sh.write(i + 1, 14, l["hair_info"]["hair_care"])
                sh.write(i + 1, 15, l["hair_info"]["career"])
                sh.write(i + 1, 16, l["hair_info"]["like_dress"])
                sh.write(i + 1, 17, l["hair_info"]["like_leisure"])
                sh.write(i + 1, 18, l["hair_info"]["beauty_degree"])
                sh.write(i + 1, 19, l["hair_info"]["season"])

                sh.write(i + 1, 9, l["hair_info"]["hair_quantity"])
            except:
                pass

    w.save("/Users/sunyihuan/Desktop/wangluo.xls")


def write2excel_xianchang():
    xianchang = mdb.xm_hair_need.find(
        {"status": 101, "source": 1}).sort("_id", pymongo.DESCENDING)

    w = xlwt.Workbook()
    sh = w.add_sheet("xianchang_design0", cell_overwrite_ok=True)
    writeHead_xianchang(sh)
    for i, l in enumerate(xianchang):
        if i > 65530:
            break
        else:
            try:
                id = str(l["_id"])
                info = l["hair_info"]
                age = info["age"]
                natural_style = info["natural_style"]
                if "eyelid" in info.keys():
                    eyelid = 1
                else:
                    eyelid = 0

                scheme = mdb.xm_hair_scheme.find_one({"need_id": l["_id"]})
                feature = scheme["principle"]["feature"]
                hue = feature["hue"]
                center = feature["center"]
                fringe = feature["fringe"]
                texture = feature["texture"]
                length = feature["length"]
                purity = feature["purity"]
                shade = feature["shade"]

                sh.write(i + 1, 0, id)
                sh.write(i + 1, 1, age)
                sh.write(i + 1, 2, info["three_court"])
                sh.write(i + 1, 3, info["face_length"])
                sh.write(i + 1, 4, info["face_sense"])
                sh.write(i + 1, 5, info["face_shape"])
                sh.write(i + 1, 6, info["skin_shade"])
                sh.write(i + 1, 7, natural_style)
                sh.write(i + 1, 8, info["shape"])
                sh.write(i + 1, 9, info["hair_length"])
                sh.write(i + 1, 10, info["skin_hue"])
                sh.write(i + 1, 11, eyelid)

                sh.write(i + 1, 14, hue)
                sh.write(i + 1, 15, center)
                sh.write(i + 1, 16, fringe)
                sh.write(i + 1, 17, texture)
                sh.write(i + 1, 18, length)
                sh.write(i + 1, 19, purity)
                sh.write(i + 1, 20, shade)
            except:
                print(i)

    w.save("/Users/sunyihuan/Desktop/xianchang_all.xls")


if __name__ == "__main__":
    print("网络设计总单数：", wangluo_counts)
    print("现在设计总单数：", xianchang_counts)
    print("总单数：", wangluo_counts + xianchang_counts)

    # write2excel_wangluo()
    write2excel_xianchang()
