# coding:utf-8 
'''
网点年收益计算

created on 2019/3/28

@author:sunyihuan
'''


def month_profit(m_num):
    '''
    第m_num月的总收益
    :param m_num:
    :return:
    '''
    # 烟弹复购收益
    s = 0
    for j in range(m_num):
        s += 100 * 0.6 * 0.23 * 350 * (pow(0.7, m_num - j) * pow(0.9, j))
    # 烟杆收益
    for j in range(m_num):
        s += 100 * 0.6 * 0.23 * 300 * (pow(0.9, j))
    return s


def all_profit(m):
    '''
    m个月的收益总额
    :param m:  月份
    :return: 第m月的收益总额
    '''
    pro = 0
    for i in range(1, m + 1):
        m_pro = month_profit(i)
        pro += m_pro
    return pro


for i in range(1, 13):
    print("第{0}月，当月收益额：{1:.2f}".format(i, month_profit(i)))
