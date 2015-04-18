# coding=utf-8

__author__ = 'jinyu'


import os

delimiter = ','
buy_behaviour_type = '4'

users_features = {}
items_features = {}
labels = {}


# 生成训练矩阵
def generate_matrix(uipairs_features_file_path):
    uipairs_features_file = open(uipairs_features_file_path)
    matrix_file = open("matrix.csv", 'w')

    for line in uipairs_features_file:

        line_entrys = line.split(delimiter)
        user_id = line_entrys[0]
        item_id = line_entrys[1]

        if item_id in items_features:
            matrix_line = delimiter.join(line_entrys[:-1]) + "," + \
                          users_features[user_id] + "," + \
                          items_features[item_id] + "," + \
                          get_label_by_uipair(user_id, item_id) + "\n"
            matrix_file.write(matrix_line)

    matrix_file.close()
    uipairs_features_file.close()


def load_users_features(users_features_file_path):
    users_features_file = open(users_features_file_path)

    for line in users_features_file:
        line_entrys = line.split(delimiter)
        user_id = line_entrys[0]
        user_features = line_entrys[1:-1]
        users_features[user_id] = delimiter.join(user_features)
    print "load users_features completed"
    users_features_file.close()


def load_items_features(items_features_file_path):
    items_features_file = open(items_features_file_path)

    for line in items_features_file:
        line_entrys = line.split(delimiter)
        item_id = line_entrys[0]
        item_features = line_entrys[1:-1]
        items_features[item_id] = delimiter.join(item_features)

    print "load items_features completed"
    items_features_file.close()


def load_labels(label_file_path):
    label_file = open(label_file_path)

    for line in label_file:
        user_id, item_id, behavior_type, user_geohash, item_category, time, date = line.split(delimiter)

        if behavior_type == buy_behaviour_type:
            labels[user_id+delimiter+item_id] = "1"

    print "load label completed"
    label_file.close()


# 获取ui对标签
def get_label_by_uipair(user_id, item_id):
    if (user_id+delimiter+item_id) in labels:
        return "1"
    else:
        return "0"



path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'\\source'
os.chdir(path)  # change dir to '~/files'

users_features_file_path = "users_featurers.csv"
items_features_file_path = "items_featurers.csv"
label_file_path = "labels.csv"
uipairs_features_file_path = "userBrand_features.csv"

load_users_features(users_features_file_path)
load_items_features(items_features_file_path)
load_labels(label_file_path)
generate_matrix(uipairs_features_file_path)