# coding=utf-8
__author__ = 'jinyu'
import types

# 生成字典的key值
def get_features_key(features):
    features_key_str = ''
    for k, v in features.iteritems():
        if (type(v) is not types.ListType) and (type(v) is not types.DictType):
            features_key_str += str(k) + ','

    return features_key_str


# 解析日期
def parse_date(raw_date):
    entry_date = raw_date
    year, month, day = entry_date.split(" ")[0].split("-")
    return int(year), int(month), int(day)


# 文件排序
def generate_sortedfile(origin_file_path, new_file_path, sort_column=0):
    origin_file = open(origin_file_path)

    entrys = origin_file.readlines()
    entrys.sort(key=lambda x: x.split(",")[sort_column])
    sorted_file = open(new_file_path, "w")
    for i in entrys:
        sorted_file.write(i)
    sorted_file.close()
    origin_file.close()