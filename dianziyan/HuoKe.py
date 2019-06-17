# coding:utf-8 
'''
网点托客平台利润计算

created on 2019/2/12

@author:sunyihuan
'''




'''
奖励金设置
'''
butie_level_1 = 100  # 成交一单
butie_level_2 = 100  # 满5单奖励
butie_level_3 = 200  # 满10单奖励
butie_level_4 = 300  # 满15单奖励
butie_level_5 = 500  # 满25单奖励
butie_level_6 = 1000  # 满50单奖励
butie_level_7 = 2000  # 满100单奖励


def shuiDian(sales, cost):
    '''
    总税额
    :param sales: 销售额
    :param cost: 成本
    :return:
    '''
    # 销项税
    xiao_shui = (sales / 1.13) * 0.13
    # 进项税
    jin_shui = (cost / 1.13) * 0.13
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
    shui = shuiDian(sales - fencheng, costs)
    profit_all = sales - costs - fencheng - shui
    return profit_all


def damage_costs(orders, return_rate, free_quota):
    '''
    退款退货成本
    :param orders: 成交订单量
    :param orders: 退货率
    :param orders: 免费体验券数量
    :return: damage_costs退款退货平台的总成本
    '''
    damage_orders = int(orders * return_rate / (1 - return_rate))  # 退货量
    if damage_orders > free_quota:
        buy_quotas = damage_orders - free_quota
    else:
        buy_quotas = 0
    print(buy_quotas)

    damage_costs = damage_orders * (10 + 4 * 10 + 6) - buy_quotas * 20  # 退货平台成本
    return damage_costs


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
    freight = orders * 6  # 运费
    # print("毛利：", round(experience_pro - freight, 2))
    damage_cost = damage_costs(orders, 0.4, 30)  # 40%退货率、30个体验名额
    print("退货成本：", damage_cost)
    wangdian_re_money = wangdian_reward_money(orders)  # 奖励金总额
    # wangdian_re_money = 0
    # print("奖励金:", round(wangdian_re_money + int(orders / 15) * 200, 2))
    jianglijin = round(wangdian_re_money, 2)
    print("奖励金:", jianglijin)
    net_pro = experience_pro - freight - damage_cost - jianglijin
    return round(net_pro, 2), jianglijin


def JiangLiJin_result2excel():
    '''
    奖励金奖励后，平台利润写入excel表格
    :return:
    '''
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
    w.save("/Users/sunyihuan/Desktop/JiangLiJin_final.xls")


if __name__ == "__main__":
    he_ratio = 0.12  # 合伙人提成比例
    wang_ratio = 0.23  # 网点提成比例
    orders = 100  # 订单量
    print("销售额：", orders * 300)
    experience_net, jianglijin = experience_net_profit(orders, he_ratio, wang_ratio)
    print("净利润：", experience_net)
    print("平台利润率：{:.2%}".format(experience_net / (orders * 300)))
    JiangLiJin_result2excel()
    # print(shuiDian(300-105,90))
