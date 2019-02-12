# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''
butie_level_1 = 50  # 成交一单
butie_level_2_ratio = 40  # [2,10）每成交一单的奖励
butie_level_3 = 100  # 满25单奖励
butie_level_4 = 300  # 50单奖励
butie_level_5 = 500  # 满100单奖励
butie_level_6 = 1000  # 满200单奖励


def shuiDian(sales, cost):
    '''
    总税额
    :param sales: 销售额
    :param cost: 成本
    :return:
    '''
    # 销项税
    xiao_shui = (sales / 1.16) * 0.16
    # 进项税
    jin_shui = (cost / 1.16) * 0.16
    return round(xiao_shui - jin_shui, 2)


def fenCheng(sales, he_ratio, wang_ratio):
    '''
    总的分成，包括合伙人分成和网点分成
    :param sales: 销售额
    :return:
    '''
    # 合伙人分成
    hehuoren_fencheng = sales * he_ratio
    # 网点分成
    wangdian_fencheng = sales * wang_ratio
    return round(hehuoren_fencheng + wangdian_fencheng, 2)


def experience_profit(orders, he_ratio, wang_ratio):
    '''
    体验装平台利润
    :param orders: 订单量
    :return:profit_all：毛利润
    '''
    sales = orders * 300
    costs = orders * (50 + 4 * 10)
    fencheng = fenCheng(sales, he_ratio, wang_ratio)
    shui = shuiDian(sales, costs)
    profit_all = sales - costs - fencheng - shui
    return profit_all


def wangdian_reward_money(orders):
    '''
    网点现金补贴
    :param orders: 订单量
    :return: 补贴金额
    '''
    if orders == 1:
        butie = butie_level_1
    elif orders >= 2 and orders <= 10:
        butie = (orders - 1) * butie_level_2_ratio + butie_level_1
    elif orders > 10 and orders < 25:
        butie = 9 * butie_level_2_ratio + butie_level_1
    elif orders >= 25 and orders < 50:
        butie = butie_level_1 + 9 * butie_level_2_ratio + butie_level_3
    elif orders >= 50 and orders < 100:
        butie = butie_level_1 + 9 * butie_level_2_ratio + butie_level_3 + butie_level_4
    elif orders >= 100 and orders < 200:
        butie = butie_level_1 + 9 * butie_level_2_ratio + butie_level_3 + butie_level_4 + butie_level_5
    elif orders >= 200:
        butie = butie_level_1 + 9 * butie_level_2_ratio + butie_level_3 + \
                butie_level_4 + butie_level_5 + butie_level_6
    else:
        butie = 0

    return butie


def experience_net_profit(orders, he_ratio, wang_ratio):
    '''
    净利润，扣除折损、运费，其中折损退货率40%，退货平台成本为产品成本及运费
    :param orders: 订单量
    :return:
    '''
    experience_pro = experience_profit(orders, he_ratio, wang_ratio)  # 毛利润
    freight = orders * 2  # 运费
    print("毛利：", round(experience_pro - freight, 2))
    damage_nums = int((orders * 4) / 6)  # 退货量
    damage_costs = damage_nums * (10 + 4 * 10) + damage_nums * 2  # 40%退货中平台的成本
    print("退货成本：", damage_costs)
    wangdian_re_money = wangdian_reward_money(orders)  # 奖励金总额，500元月奖励金额
    # wangdian_re_money = 0
    # print("奖励金:", round(wangdian_re_money + int(orders / 15) * 200, 2))
    jianglijin = round(wangdian_re_money, 2)
    print("奖励金:", jianglijin)
    net_pro = experience_pro - freight - damage_costs - jianglijin
    return round(net_pro, 2)


if __name__ == "__main__":
    he_ratio = 0.1  # 合伙人提成比例
    wang_ratio = 0.27  # 网点提成比例
    orders = 15  # 订单量
    yue = 200  # 月奖励金额
    print("销售额：", orders * 300)
    experience_net = round(experience_net_profit(orders, he_ratio, wang_ratio), 2) - yue
    print("净利润：", experience_net)
    print("平台利润率：{:.2%}".format(experience_net / (orders * 300)))
