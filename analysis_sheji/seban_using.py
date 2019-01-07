# coding:utf-8 
'''
created on 2019/1/7

@author:sunyihuan
'''
from utils import connect_mongodb_sheji, connect_es, id2ObjectId, day2timestamp, ts2utcdatetime, list_change_type

mdb = connect_mongodb_sheji()
stylists_color_disk = mdb.xm_good_colour_disk.distinct("myid", {"status": 101})
print("完成色板设置总人数：", len(stylists_color_disk))

star_timeStamp = day2timestamp("2019-1-7")
vip_st = mdb.wxuser.distinct("_id", {"expireat": {"$gt": star_timeStamp}})  # vip列表
stylists_color_disk_vip = set(stylists_color_disk) & set(vip_st)
print("完成色板设置VIP总人数：", len(stylists_color_disk_vip))

# "brand_id"=100001 伊诺雅；"brand_id"=100002﻿欧莱雅；"brand_id"=100005﻿﻿施华蔻；
# "brand_id"=﻿100004 威娜；"brand_id"=﻿100005 ﻿资生堂

stylists_color_yny = mdb.xm_good_colour_disk.distinct("myid", {"status": 101, "brand_id": 100001})
print("选择伊诺雅设置总人数：", len(stylists_color_yny))
stylists_color_oly = mdb.xm_good_colour_disk.distinct("myid", {"status": 101, "brand_id": 100002})
print("选择欧莱雅设置总人数：", len(stylists_color_oly))
stylists_color_shk = mdb.xm_good_colour_disk.distinct("myid", {"status": 101, "brand_id": 100003})
print("选择施华蔻设置总人数：", len(stylists_color_shk))
stylists_color_wn = mdb.xm_good_colour_disk.distinct("myid", {"status": 101, "brand_id": 100004})
print("选择威娜设置总人数：", len(stylists_color_wn))
stylists_color_zst = mdb.xm_good_colour_disk.distinct("myid", {"status": 101, "brand_id": 100005})
print("选择资生堂设置总人数：", len(stylists_color_zst))

