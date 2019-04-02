# coding:utf-8 
'''
生成电子烟产品的条形码，用于包装盒上
created on 2019/4/1

@author:sunyihuan
'''


def sum_list(l):
    '''
    list求和
    :param l:
    :return:
    '''
    s = 0
    for ll in l:
        s += int(ll)
    return s


def all_nums(nums_12):
    '''
    获取完整条形码
    :param nums_12: 条形码前12位
    :return: 完整条形码
    '''
    if len(str(nums_12)) != 12:
        print("输入非12位数字")
        return None
    else:
        nums_12 = str(nums_12)
        # 奇数位
        nums_odd = nums_12[::2]
        # 偶数位
        nums_even = nums_12[1::2]

        odd_s = sum_list(nums_odd)
        even_s = sum_list(nums_even)
        return str(nums_12) + str((10 - (odd_s + 3 * even_s) % 10) % 10)


if __name__ == "__main__":
    nums = [693307300001, 693307300002, 693307300003, 693307300004, 693307300005, 693307300006, 693307300007,
            693307300008, 693307300009, 693307300010, 693307300011]

    for n in nums:
        print("前12位:{}    完整码：{}".format(n, all_nums(n)))
