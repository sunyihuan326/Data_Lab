# coding:utf-8 
'''
created on 2019/1/29

@author:sunyihuan
'''


def get_star(wangdian_nums):
    '''
    合伙人星级
    :param wangdian_nums:
    :return:
    '''
    if wangdian_nums >= 2 and wangdian_nums < 10:
        star = 2
    elif wangdian_nums >= 10 and wangdian_nums < 20:
        star = 3
    elif wangdian_nums >= 20 and wangdian_nums < 50:
        star = 4
    elif wangdian_nums >= 50 and wangdian_nums < 100:
        star = 5
    elif wangdian_nums >= 100:
        star = 100
    else:
        star = 1

    return star


def wangdian_butie(orders):
    '''
    网点提成
    :param orders:
    :return:
    '''
    if orders == 1:
        butie = 100
    elif orders >= 2 and orders <= 10:
        butie = (orders - 1) * 40 + 100
    elif orders >= 15 and orders < 25:
        butie = 300 + 100 + 9 * 40
    elif orders >= 25 and orders < 50:
        butie = 500 + 300 + 100 + 9 * 40
    elif orders >= 50 and orders < 100:
        butie = 1000 + 500 + 300 + 100 + 9 * 40
    elif orders >= 100:
        butie = 2000 + 1000 + 500 + 300 + 100 + 9 * 40
    else:
        butie = 0

    return butie


def yonghu_yantan_pingheng(dan_nums):
    if dan_nums == 10:
        pingeng = 5 * 35 * pingTai_lirun - 5 * 9
    elif dan_nums == 30:
        pingeng = 20 * 35 * pingTai_lirun - 5 * 9 + 5 * 35 * pingTai_lirun - 5 * 9
    else:
        pingeng = dan_nums * 35 * pingTai_lirun - 20 * 35 * pingTai_lirun - 5 * 9 + 5 * 35 * pingTai_lirun - 5 * 9
    return pingeng


def pingheng_day(days):
    orders = days * 3
    butie = wangdian_butie(orders) + int(days / 30) * 500
    print("补贴：", butie)
    lirun = pingTai_lirun * orders * 300
    print("利润：", lirun)
    return lirun - butie


if __name__ == "__main__":
    pingTai_lirun = 0.08
