# coding:utf-8 
'''
created on 2019/1/30

@author:sunyihuan
'''
from dianziyan.cesuan_suit import fenCheng, shuiDian


def yandan_profit(buy_nums, give_nums, he_ratio, wang_ratio):
    '''
    烟弹利润
    :param buy_nums: 实际支付数量
    :param give_nums: 赠送数量
    :return:
    '''
    sales = buy_nums * 35
    costs = (buy_nums + give_nums) * 10
    fencheng = fenCheng(sales, he_ratio, wang_ratio)
    shui = shuiDian(sales, costs)
    profit = sales - costs - fencheng - shui - 8
    return profit

#
# if __name__ == "__main__":
#     he_ratio = 0.15  # 合伙人提成比例
#     wang_ratio = 0.3  # 网点提成比例
#     print(yandan_profit(7, 3, he_ratio, wang_ratio))
