# coding:utf-8 
'''
created on 2019/2/13

@author:sunyihuan
'''
from dianziyan.cesuan_suit import shuiDian, fenCheng


def wangluo_Huoke(orders):
    '''
    网络合作伙伴获客利润
    :param orders: 订单量
    :return:
    '''
    sales = orders * 300
    costs = orders * (50 + 40)
    damage_nums = int((orders * 4) / 6)  # 退货量
    damage_costs = damage_nums * (10 + 4 * 10) + damage_nums * 8  # 40%退货中平台的成本
    shuidian = shuiDian(sales, costs + damage_nums * 40)
    fencheng = fenCheng(sales, 0.1, 0.27)
    freight = orders * 8
    profits = sales - costs - shuidian - fencheng - freight - damage_costs + 700

    return profits


if __name__ == "__main__":
    orders = 100  # 订单量
    print("销售额：", orders * 300)
    experience_net = round(wangluo_Huoke(orders), 2)
    print("净利润：", experience_net)
    print("平台利润率：{:.2%}".format(experience_net / (orders * 300)))
