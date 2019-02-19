# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''
from dianziyan.FuGou_yanDan import shuiDian


def users_recommend_costs(recommend_user_nums):
    '''
    v1.0
    用户推荐用户奖励烟弹成本
    :param recommend_user_nums: 推荐成功人数
    :return:
    '''
    if recommend_user_nums == 1:
        costs = 3 * 10  # 一次快递发货，奖励5个烟弹
    elif recommend_user_nums == 2:
        costs = (3 + 5) * 10  # 二次快递发货，奖励15个烟弹
    elif recommend_user_nums >= 3:
        costs = (3 + 5 + 8) * 10  # 三次快递发货，奖励30个烟弹
    else:
        costs = 0
    return costs


def users_recommend_costs2(recommend_user_nums):
    '''
    v2.0
    用户推荐用户奖励烟弹成本
    :param recommend_user_nums: 推荐成功人数
    :return:
    '''
    if recommend_user_nums > 0:
        costs = recommend_user_nums * 8 * 10 + recommend_user_nums * 8
    # if recommend_user_nums >= 1 and recommend_user_nums <= 5:
    #     costs = recommend_user_nums * 10 * 10 + recommend_user_nums * 8  # 一次快递发货，奖励5个烟弹
    # elif recommend_user_nums >= 6 :
    #     costs = 5 * 10 * 10 + (recommend_user_nums - 5) * 10 * 10 + recommend_user_nums * 8  # 二次快递发货，奖励15个烟弹
    # elif recommend_user_nums > 10 and recommend_user_nums <= 20:
    #     costs = 5 * 5 * 10 + 5 * 10 * 10 + (recommend_user_nums - 10) * 15 * 10 + recommend_user_nums * 8
    # elif recommend_user_nums > 20:
    #     costs = 5 * 5 * 10 + 5 * 10 * 10 + 10 * 15 * 10 + 20 * 8
    else:
        costs = 0
    return costs


def users_recommend_profits(recommend_user_nums):
    '''
    用户推荐用户利润
    :param recommend_user_nums: 推荐成功数量
    :return:
    '''
    sales = recommend_user_nums * 300  # 销售额
    costs = users_recommend_costs(recommend_user_nums) + recommend_user_nums * 90  # 推荐成功成本
    Tui_cost = (3 - recommend_user_nums) * (10 + 4 * 10)  # 推荐失败成本
    all_costs = costs + Tui_cost
    freight = 3 * 8  # 运费,包含被推荐者3次套装运费和推荐者3次奖励烟弹运费
    print("成本：", round(all_costs + freight, 2))
    profits = sales - all_costs - shuiDian(sales, costs) - freight  # 扣税后利润
    return profits


if __name__ == "__main__":
    recommend_user_nums = 1
    print("推荐成交人数：", recommend_user_nums)
    pro = users_recommend_profits(recommend_user_nums)
    print("利润：", round(pro, 2))
    print("利润率：{:.2%}".format(pro / (recommend_user_nums * 300)))
    # print(shuiDian(300, 100))
