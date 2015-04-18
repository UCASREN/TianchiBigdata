# coding=utf-8

__author__ = 'jinyu'

# brand
# sold,sold_user{user,count}
# cart,cart_user[]
# fav,fav_user[]
# click,click_user[]

import os
from util import *


buy_behaviour_type = '4'
cart_behaviour_type = '3'
favorite_behaviour_type = '2'
click_behaviour_type = '1'
delimiter = ','

basic_feature_behaviour = {'1':['sold_times','sold_user','user_first_sold_time'],
                           '2':['cart_times','cart_user','user_first_cart_time'],
                           '3':['favor_times','favor_user','user_first_cart_time'],
                           '4':['click_times','click_user','user_first_cart_time']}

def initial_item_features(item_features):

    ###基础属性
    for basic_features in basic_feature_behaviour.values():
        item_features[basic_features[0]] = 0    #xxx_times # 销量 # 购物车量 # 收藏量 # 点击量
        item_features[basic_features[1]] = {}   #xxx_user {user，count} # 购物车用户 # 消费用户
        item_features[basic_features[2]] = {}   #user_first_xxx_time


    item_features['user'] = []
    item_features['eachday_behavior_counts']= {}  # 每天行为总数 {time:[0,1,2,3]}++++++++++

    ###扩展属性
    item_features['lastday_behavior_counts'] = []  # 最后一天行为次数++++++++
    item_features['total_user'] = 0.0   # 总用户数
    item_features['total_cart_people'] = 0.0    # 总购物车人数
    item_features['total_buy_people'] = 0.0     # 总购买人数
    item_features['total_favor_people'] = 0.0   # 总收藏人数
    item_features['total_click_people'] = 0.0   # 总收藏人数
    item_features['multiple_buy_user'] = 0.0    # 多次购买的用户数
    item_features['once_click_user'] = 0.0  # 只点击过一次的用户数
    item_features['careful_user'] = 0.0 # 不在初次访问品牌时购买的订单数 ???????



def extract_items_features(train_file_path):
    # 按商品id排序
    generate_sortedfile(train_file_path, "sorted_by_item-" + train_file_path, 1)

    train_file = open("sorted_by_item-" + train_file_path)
    items_features_file = open("items_featurers.csv", 'w')

    item_features = {}
    item_features = initial_item_features(item_features)
    # 输出栏位名
    # item_features = get_other_basic_item_features(item_features)
    # items_features_file.write("item_id" + "," + get_features_key(item_features) + "\n")


    pre_item_id = train_file.readline().split(delimiter)[1]  # 获取第一行的item_id
    train_file.seek(0)
    for line in train_file:
        user_id, item_id, behavior_type, user_geohash, item_category, time, date = line.split(delimiter)

        # 如果前一个物品pre_item_id和读取到的item_id不一样则输出当前item_features并置空
        if not item_id == pre_item_id:
            item_features = get_other_basic_item_features(item_features)  # 获取用户其他特征
            items_features_file.write(pre_item_id + "," + get_item_features_str(item_features) + "\n")  # 输出当前item_features
            item_features = initial_item_features(item_features)  # 初始化置空item_features

        item_features['user'].append(user_id)

        xxx_times = basic_feature_behaviour[behavior_type][0]
        xxx_user  = basic_feature_behaviour[behavior_type][1]
        user_xxx_first_time  = basic_feature_behaviour[behavior_type][2]
        item_features[xxx_times] += 1
        item_features[xxx_user][user_id] = item_features[xxx_user].get(user_id, 0) + 1
        if user_id not in item_features[user_xxx_first_time]:
            item_features[user_xxx_first_time][user_id] = time


        pre_item_id = item_id

    item_features = get_other_basic_item_features(item_features)
    # print item_features
    #  输出最后一个item_features到文件并重新初始化item_features
    items_features_file.write(pre_item_id + "," + get_item_features_str(item_features) + "\n")

    train_file.close()
    items_features_file.close()


def get_other_basic_item_features(item_features):
    for count in item_features['sold_user'].values():
        if count > 2:
            item_features['multiple_buy_user'] += 1
    for count in item_features['click_user'].values():
        if count == 1:
            item_features['once_click_user'] += 1

    item_features['total_buy_people'] = float(len(set(item_features['sold_user'].keys())))
    item_features['total_cart_people'] = float(len(set(item_features['cart_user'])))
    item_features['total_click_people'] = float(len(set(item_features['click_user'].keys())))
    item_features['total_favor_people'] = float(len(set(item_features['favor_user'])))
    item_features['total_user'] = float(len(set(item_features['user'])))

    item_features['sold_per_cart'] = item_features['sold_times'] / (item_features['cart_times'] + 1)
    item_features['sold_per_favorite'] = item_features['sold_times'] / (item_features['favor_times'] + 1)
    item_features['sold_per_click'] = item_features['sold_times'] / (item_features['click_times'] + 1)
    item_features['people_buy_per_cart'] = item_features['total_buy_people'] / (item_features['total_cart_people'] + 1)
    item_features['people_buy_per_favorite'] = item_features['total_buy_people'] / (item_features['total_favor_people'] + 1)
    item_features['people_buy_per_click'] = item_features['total_buy_people'] / (item_features['total_click_people'] + 1)

    # 比值特征
    item_features['comeback_rate'] = item_features['multiple_buy_user'] / (item_features['total_buy_people'] + 1)
    item_features['jump_rate'] = item_features['once_click_user'] / (item_features['total_user'] + 1)
    item_features['active_rate'] = item_features['multiple_buy_user'] / (item_features['total_user'] + 1)
    item_features['average_buy'] = item_features['sold_times'] / (item_features['total_user'] + 1)
    item_features['average_cart'] = item_features['cart_times'] / (item_features['total_user'] + 1)
    item_features['average_click'] = item_features['click_times'] / (item_features['total_user'] + 1)
    item_features['average_favor'] = item_features['favor_times'] / (item_features['total_user'] + 1)

    return item_features


def get_item_features_str(item_features):
    item_features_str = ''
    for k, v in item_features.iteritems():
        if (type(v) is not types.ListType) and (type(v) is not types.DictType):
            item_features_str += str(v) + ','
    return item_features_str


path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\source'
os.chdir(path)  # change dir to '~/files'
train_file_path = "train_filtered_unknownitem_tianchi_mobile_recommend_train_user.csv"
extract_items_features(train_file_path)
