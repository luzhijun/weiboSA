#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:37:45 2016

@author: Trucy
"""
import pickle

with open('data.pl', 'rb') as f:
    data = pickle.load(f)

tAdmin = data['admin']
tPrice = data['price']
tTag = data['tag']

# text="#上海租房#来微博上问一下，上海有人要租房子的么，我租了一整套，四室的，精装修，两个卫生间，一个大厨房，一个小厨房，两个洗衣机，小区环境还不错的。还有两个单间出租，在浦东张江，孙建 申城佳苑 要也是后期的话可以来旁蹭听小班课[哆啦A梦花心] 一间2000左右 @上海租房"
#text="徐家汇天钥桥路南天大楼有房出租： 要求： 1，作息正常，正常白天上下班人士。2，爱干净的女生，限住1人。 3，租金2400，出租三室中其中一间，面积25平米左右。 4. 联系人：张先生，137-6193-9178 @上海租房无中介 @上海租房 @上海租房无中介联盟 @房天下上海租房"
# text="#上海租房# 求租上海浦东惠南两室户整租，最好在地铁站附近，预算两千一下。长租啊@上海租房 @上海租房无中介 @上海租房无中介联盟 @上海非中介租房"
#text="上海浦东新区12号线金京路门口的房子，三室两厅一卫，有厨房可做饭，客餐厅沙发都有，是个温馨的小家，@上海租房 有一间次卧转租1750元一个月，希望找一个爱干净的朋友，男女不限，随时欢迎来看房，房子是翻新过的，床，柜子都很新，有兴趣的朋友可以私信我哦"
#text="求租一室户，要能做饭的，刚毕业的情侣 正经工作 会爱护房子，求租离静安寺地铁30分钟左右的房子，最好离地铁站比较近的，加班党晚上比较晚下班[泪][泪][泪]拜托有房源的联系我，先谢了@上海租房 @互助租房"
text = '上海租房#来微博上问一下，上海有人要租房子的么，我租了一整套，四室的，精装修，两个卫生间，一个大厨房，一个小厨房，两个洗衣机，小区环境还不错的。还有两个单间出租，在浦东张江，孙建路 申城佳苑 要也是后期的话可以来旁蹭听小班课[哆啦A梦花心] 一间2000左右'
i = 0
location = []  # 存储行政区
price = []  # 存储价格
rent = True  # 出租
while i < len(text):
    if tPrice.has_keys_with_prefix(text[i]):  # 优先匹配价格
        j = i
        i += 1
        # 正向最大匹配
        while i < len(text) and tPrice.has_keys_with_prefix(text[j:i + 1]):
            i += 1
        print('p', text[j:i], tAdmin.keys(text[j:i]))
        if text[j:i] in tPrice.keys(text[j:i]):  # 价格转换成数字
            if ord(text[j]) > 60:
                price.append(tPrice[text[j:i]])
            else:
                price.append(int(text[j:i]))
            continue
        else:  # 未匹配，去尝试匹配地点
            i = j
    if tAdmin.has_keys_with_prefix(text[i]):  # 匹配地点
        j = i
        i += 1
        # 正向最大匹配
        while i < len(text) and tAdmin.has_keys_with_prefix(text[j:i + 1]):
            i += 1

        print('a', text[j:i], tAdmin.keys(text[j:i]))
        if text[j:i] in tAdmin.keys(text[j:i]):
            location.append(text[j:i])
            print('匹配成功', text[i])
            continue
        else:  # 未匹配，去尝试匹配租房还是求房
            i = j
    if rent and tTag.has_keys_with_prefix(text[i]):  # 未匹配过的情况下匹配租房还是求房
        j = i
        i += 1
        # 正向最大匹配
        while i < len(text) and tTag.has_keys_with_prefix(text[j:i + 1]):
            i += 1
        print('t', text[j:i], tAdmin.keys(text[j:i]))
        if text[j:i] in tTag.keys(text[j:i]):
            rent = False
        else:  # 未匹配，去尝试匹配租房还是求房
            i = j + 1
    else:
        i += 1

print(location)
print(price)
print(rent)
