# coding:utf-8 
'''
烟弹复购收益

created on 2019/4/12

@author:sunyihuan
'''


def profit(start_nums, f_rate, month_nums):
    '''
    第month_nums个月烟弹复购的销售额
    :param start_nums:默认每月新用户人数
    :param f_rate:复购率
    :param month_nums:月份
    :return:pro：第month_nums月烟弹复购额
    '''
    pro = 0
    for i in range(month_nums):
        p = start_nums * 300 * pow(f_rate, i + 1)
        # print(i + 1, p)
        pro += p
    return pro


if __name__ == "__main__":
    start_nums = 3000
    f_rate = 0.5
    all_pro = 0
    month_nums = 8
    # p = profit(start_nums, f_rate, month_nums) * 0.33
    # print(p)
    for k in range(month_nums + 1):
        p = profit(start_nums, f_rate, k) * 0.33
        print(k + 1, p)
        all_pro += p
    print(all_pro)
