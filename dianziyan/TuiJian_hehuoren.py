# coding:utf-8 
'''
created on 2019/2/12

@author:sunyihuan
'''


def hehuoren_recommend(recommend_nums):
    '''
    合伙人推荐合伙人
    :param recommend_nums: 推荐成功人数
    :return:
    '''
    YaJin = 5000
    cost = 10 * 100 + 4 * 40 + 60 * 10  # 产品成本
    freight = 10  # 运费
    profit = YaJin - cost - freight  # 每成功一个合伙人利润
    profits = recommend_nums * profit
    return profits


print(hehuoren_recommend(2))
