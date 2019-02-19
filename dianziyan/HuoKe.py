# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''
butie_level_1 = 80  # 成交一单
butie_level_2 = 100  # 满5单奖励
butie_level_3 = 100  # 满10单奖励
butie_level_4 = 200  # 满15单奖励
butie_level_5 = 300  # 满25单奖励
butie_level_6 = 500  # 满50单奖励
butie_level_7 = 1000  # 满100单奖励


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
    shui = shuiDian(sales-fencheng, costs)
    profit_all = sales - costs - fencheng - shui
    return profit_all


def wangdian_reward_money(orders):
    '''
    网点现金补贴
    :param orders: 订单量
    :return: 补贴金额
    '''
    if orders >= 1 and orders < 5:
        butie = butie_level_1
    elif orders >= 5 and orders < 10:
        butie = butie_level_1 + butie_level_2
    elif orders >= 10 and orders < 15:
        butie = butie_level_1 + butie_level_2 + butie_level_3
    elif orders >= 15 and orders < 25:
        butie = butie_level_1 + butie_level_2 + butie_level_3 + butie_level_4
    elif orders >= 25 and orders < 50:
        butie = butie_level_1 + butie_level_2 + butie_level_3 + butie_level_4 + butie_level_5
    elif orders >= 50 and orders < 100:
        butie = butie_level_1 + butie_level_2 + butie_level_3 + \
                butie_level_4 + butie_level_5 + butie_level_6
    elif orders >= 100:
        butie = butie_level_1 + butie_level_2 + butie_level_3 + \
                butie_level_4 + butie_level_5 + butie_level_6 + butie_level_7
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
    # print("毛利：", round(experience_pro - freight, 2))
    damage_nums = int((orders * 4) / 6)  # 退货量
    damage_costs = damage_nums * (10 + 4 * 10) + damage_nums * 2  # 40%退货中平台的成本
    # print("退货成本：", damage_costs)
    wangdian_re_money = wangdian_reward_money(orders)  # 奖励金总额，500元月奖励金额
    # wangdian_re_money = 0
    # print("奖励金:", round(wangdian_re_money + int(orders / 15) * 200, 2))
    jianglijin = round(wangdian_re_money, 2)
    # print("奖励金:", jianglijin)
    net_pro = experience_pro - freight - damage_costs - jianglijin
    return round(net_pro, 2), jianglijin


if __name__ == "__main__":
    he_ratio = 0.12  # 合伙人提成比例
    wang_ratio = 0.27  # 网点提成比例
    # orders = 25  # 订单量
    # print("销售额：", orders * 300)
    # experience_net, jianglijin = experience_net_profit(orders, he_ratio, wang_ratio)
    # print("净利润：", experience_net)
    # print("平台利润率：{:.2%}".format(experience_net / (orders * 300)))
    import xlwt

    w = xlwt.Workbook()
    sh = w.add_sheet("利润")
    sh.write(0, 0, "成交单数")
    sh.write(0, 1, "销售额")
    sh.write(0, 2, "奖励金")
    sh.write(0, 3, "利润")
    sh.write(0, 4, "利润率")

    for orders in range(1, 101):
        # orders = 100  # 订单量
        # print("销售额：", orders * 300)
        experience_net, jianglijin = experience_net_profit(orders, he_ratio, wang_ratio)
        if orders in [1, 5, 10, 15, 25, 50, 100]:
            print("单数：{}   ，净利润：{}".format(orders, experience_net))
            print("平台利润率：{:.2%}".format(experience_net / (orders * 300)))
        sh.write(orders, 0, orders)
        sh.write(orders, 1, orders * 300)
        sh.write(orders, 2, jianglijin)
        sh.write(orders, 3, round(experience_net, 2))
        sh.write(orders, 4, "{:.2%}".format(experience_net / (orders * 300)))
    w.save("/Users/sunyihuan/Desktop/JiangLiJin0.xls")
