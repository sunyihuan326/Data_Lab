# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''
from dianziyan.HuoKe import experience_net_profit


def wangdian_recommend_profits(orders):
    pro = experience_net_profit(orders, 0.08, 0.27)
    if orders < 25:
        jiangLi = 0
    elif orders == 25:
        jiangLi = 300
    else:
        jiangLi = 300 + orders * 300 * 0.02
    profits = pro - jiangLi
    return round(profits, 2)


if __name__ == "__main__":
    orders = 25

    profit = wangdian_recommend_profits(orders) - 200

    print("净利：", round(profit, 2))
    print("利润率：{:.2%}".format(profit / (orders * 300)))
