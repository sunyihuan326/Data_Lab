# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''
from dianziyan.FuGou_yanDan import shuiDian


def users_recommend_costs(recommend_user_nums):
    if recommend_user_nums == 1:
        costs = 5 * 10 + 8
    elif recommend_user_nums == 2:
        costs = (5 + 10) * 10 + 8
    elif recommend_user_nums >= 3:
        costs = (5 + 10 + 15) * 10 + 8
    else:
        costs = 0
    return costs


def users_recommend_profits(recommend_user_nums):
    sales = recommend_user_nums * 300
    costs = users_recommend_costs(recommend_user_nums) + recommend_user_nums * 90 + recommend_user_nums * 8
    profits = sales - costs - shuiDian(sales, costs)
    return profits


if __name__ == "__main__":
    recommend_user_nums = 3
    print("推荐成交人数：", recommend_user_nums)
    pro = users_recommend_profits(recommend_user_nums)
    print("利润：", pro)
    print("利润率：{:.2%}".format(pro / (recommend_user_nums * 300)))
