# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''

from dianziyan.cesuan_yandan import yandan_profit
from dianziyan.cesuan_suit import shuiDian, fenCheng


def yandan_one_profit(nums_buys, nums_gives, he_ratio, wang_ratio):
    '''
    一个用户，假设一个烟弹使用yandan_frequency天
    扣除运费、税费、成本等各项费用的利润额
    :param nums_buys:实际支付数量
    :param nums_gives:赠送数量
    :param he_ratio:合伙人分成比例
    :param wang_ratio:网点分成比例
    :return:烟弹收益
    '''
    one_profit = yandan_profit(nums_buys, nums_gives, he_ratio, wang_ratio)

    return round(one_profit, 2)


if __name__ == "__main__":
    # he_ratio = 0.1  # 合伙人提成比例
    # wang_ratio = 0.27  # 网点提成比例
    he_ratio = 0  # 合伙人提成比例
    wang_ratio = 0  # 网点提成比例
    nums_buys = 10  # 实际支付数量
    nums_gives = 0  # 赠送数量

    yandan_pro = yandan_one_profit(nums_buys, nums_gives, he_ratio, wang_ratio)
    print(yandan_pro)
    print(nums_buys*35)
    print("利润率：{:.2%}".format(yandan_pro / (nums_buys * 35)))
    print("折扣率：{:.2%}".format(nums_buys / (nums_buys + nums_gives)))
