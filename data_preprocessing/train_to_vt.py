import csv
import codecs
from random import shuffle
import os
import copy
import pandas as pd
import numpy as np
import pickle


def data_write_txt(file_name, datas):
    with open(file_name, 'w+', encoding='gb18030') as f:
        f.write(str(len(datas)) + '\n')
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\n')
    print("保存文件成功，处理结束")


def data_write_csv(file_name, datas):
    file_csv = codecs.open(file_name, 'w+', 'utf-8-sig')  # 追加
    writer = csv.writer(file_csv)
    for value in datas:
        writer.writerow(value)
    print("保存文件成功，处理结束")


def list_del_dup(dup_list):
    data_repu = pd.DataFrame(dup_list)
    data_repu.drop_duplicates(inplace=True)
    re_list = np.array(data_repu).tolist()
    # re_list = filter(lambda x: "未知" not in str(x), re_list)
    # re_list = [_ for _ in re_list]
    return re_list

if __name__ == '__main__':

    cnnvd_path = "./zh_en/train2id_all.txt"

    store_path = "./zh_en/"

    entity_dict = {}
    relation_dict = {}
    test_list = []
    valid_list = []


    result_triple = []
    # 读取三元组
    with open(cnnvd_path, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            if len(params) < 3:
                continue
            h, t, r = params[0].strip(), params[1].strip(), params[2].strip()
            result_triple.append([h, t, r])

    shuffle(result_triple)
    length = len(result_triple)
    print("读入三元组长度：", length)
    test_num = 10000
    # test_num = random.randint(length//11, length//10)
    print("test数量：", test_num)
    valid_num = 10000
    # valid_num = random.randint(length//11, length//10)
    print("valid数量：", valid_num)
    test_list = result_triple[:test_num]
    valid_list = result_triple[test_num:valid_num+test_num]
    train_triple = result_triple
    print("输出train三元组长度：", len(train_triple))
    print("输出test三元组长度：", len(test_list))
    print("输出valid三元组长度：", len(valid_list))


    data_write_txt(store_path + "train2id.txt", train_triple)
    data_write_txt(store_path + "test2id.txt", test_list)
    data_write_txt(store_path + "valid2id.txt", valid_list)
