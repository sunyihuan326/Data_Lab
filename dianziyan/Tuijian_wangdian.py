# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''
from dianziyan.HuoKe import experience_net_profit


def wangdian_recommend_profits(orders):
    pro = experience_net_profit(orders, 0.1, 0.27)
    if orders < 15:
        jiangLi = 0
    elif orders == 15:
        jiangLi = 500
    else:
        jiangLi = 500 + orders * 300 * 0.02
    profits = pro - jiangLi
    return round(profits, 2)


if __name__ == "__main__":
    orders =100

    profit = wangdian_recommend_profits(orders)

    print("净利：", round(profit, 2))
    print("利润率：{:.2%}".format(profit / (orders * 300)))
