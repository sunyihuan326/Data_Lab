# coding:utf-8 
'''
created on 2019/1/31

@author:sunyihuan
'''

from dianziyan.cesuan_yandan import yandan_profit
from dianziyan.cesuan_suit import shuiDian, fenCheng


def yandan_one_profit(days, yandan_frequency, he_ratio, wang_ratio):
    '''
    一个用户，假设一个烟弹使用yandan_frequency天
    扣除运费、税费、成本等各项费用的利润额
    :param days:天数
    :param yandan_frequency:烟弹更换频率，如2，即是2天更换一个烟弹
    :param he_ratio:合伙人分成比例
    :param wang_ratio:网点分成比例
    :return:days天，一个用的烟弹收益
    '''
    yandans = int(days / yandan_frequency)
    if yandans <= 4:
        one_profit = 0
    elif yandans <= 14 and yandans > 4:
        one_profit = yandan_profit(6, 4, he_ratio, wang_ratio) - 6
    elif yandans <= 34 and yandans > 14:
        one_profit = yandan_profit(14, 6, he_ratio, wang_ratio) + yandan_profit(6, 4, he_ratio, wang_ratio) - 6 * 2
    else:
        one_profit = yandan_profit(14, 6, he_ratio, wang_ratio) + yandan_profit(6, 4, he_ratio,
                                                                                wang_ratio) + yandan_profit(
            yandans - 34, 0, he_ratio, wang_ratio) - 6 * 2 - (yandans - 34) * 2

    return round(one_profit, 2)


def gan_one_profit(days, he_ratio, wang_ratio):
    '''
    烟杆收益
    假设一年2根烟杆，第一次购买使用199-100的券
    :param days: 天数
    :param he_ratio: 合伙人分成比例
    :param wang_ratio: 网点分成比例
    :return: days天，一个用户的烟杆收益
    '''
    gans = int(days * 2 / 365) + 1
    if gans <= 1:
        gans_profit = 0
    elif gans == 2:
        gans_profit = 199 - 100 - shuiDian(99, 40) - fenCheng(99, he_ratio, wang_ratio)
    else:
        gans_profit = 199 - 100 - shuiDian(99, 40) - fenCheng(99, he_ratio, wang_ratio) + (gans - 2) * (
                shuiDian(199, 40) + fenCheng(199, he_ratio, wang_ratio))
    return round(gans_profit, 2)


if __name__ == "__main__":
    days = 200
    he_ratio = 0.15  # 合伙人提成比例
    wang_ratio = 0.3  # 网点提成比例
    yandan_frequency = 3  # 一颗烟弹抽的天数
    yandan_pro = yandan_one_profit(days, yandan_frequency, he_ratio, wang_ratio)
    gans_pro = gan_one_profit(days, he_ratio, wang_ratio)
    print(yandan_pro + gans_pro)
