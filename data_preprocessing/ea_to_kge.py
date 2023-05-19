# coding=gbk
import csv
import codecs
import re
import os
import copy
import pandas as pd
import numpy as np
import pickle
# coding=gbk

def data_write_ents(file_name, datas):
    with open(file_name, 'w+', encoding='utf-8-sig') as f:
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\n')
    print("保存文件成功，处理结束")


def data_write_triple_ke(file_name, datas):
    with open(file_name, 'w+', encoding='utf-8-sig') as f: # gb18030
        f.write(str(len(datas)) + '\n')
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[2]) + '\t' + str(value[1]) + '\n')
    print("保存文件成功，处理结束")


def get_name(string):
    if r"resource/" in string:
        sub_string = string.split(r"resource/")[-1]
    elif r"property/" in string:
        sub_string = string.split(r"property/")[-1]
    else:
        sub_string = string.split(r"/")[-1]
    sub_string = sub_string.replace('_', ' ')
    return sub_string

if __name__ == '__main__':

    fr_rel_path = "../data/dbp15k/zh_en/rel_ids_1"
    en_rel_path = "../data/dbp15k/zh_en/rel_ids_2"

    zh_ent_path = "../data/dbp15k/zh_en/ent_ids_1"
    en_ent_path = "../data/dbp15k/zh_en/ent_ids_2"

    # 用于嵌入的id
    rel_newid_dict = {}  # 用于从旧文本定位新id
    ent_newid_dict = {}  # 用于从旧文本定位新id
    newid_ent_dict = {}  # 用于从新id定位旧文本
    newid_rel_dict = {}  # 用于从新id定位旧文本
    newent_newid_dict = {}  # 用于从新文本定位新id
    newrel_newid_dict = {}  # 用于从新文本定位新id
    newid_newent_dict = {}  # 用于从新id定位新文本
    newid_newrel_dict = {}  # 用于从新id定位新文本
    id_ent_dict = {}  # 用于从旧id定位旧文本
    id_rel_dict = {}  # 用于从旧id定位旧文本
    id_newid_dict = {}  # 用于从旧id定位新id
    id_newid_entdict = {}
    id_newid_reldict = {}
    h_id = 0
    r_id = 0
    with open(fr_rel_path, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            t_id, h = params[0].strip(), params[1].strip()
            # 记录旧id - 文本
            if t_id not in id_rel_dict:
                id_rel_dict[t_id] = h
            # 记录新文本 - 新id
            if get_name(h) not in newrel_newid_dict:
                newrel_newid_dict[get_name(h)] = r_id
                newid_newrel_dict[r_id] = get_name(h)
                rel_newid_dict[h] = r_id
                newid_rel_dict[r_id] = h
                r_id += 1
            else:
                rel_newid_dict[h] = newrel_newid_dict[get_name(h)]
            id_newid_reldict[t_id] = newrel_newid_dict[get_name(h)]
        f1.close()

    with open(en_rel_path, "r", encoding="utf-8-sig") as f2:
        for line in f2.readlines():
            params = str.strip(line).split(sep='\t')
            t_id, h = params[0].strip(), params[1].strip()
            # 记录旧id - 文本
            if t_id not in id_rel_dict:
                id_rel_dict[t_id] = h
            # 记录新文本 - 新id
            if get_name(h) not in newrel_newid_dict:
                newrel_newid_dict[get_name(h)] = r_id
                newid_newrel_dict[r_id] = get_name(h)
                rel_newid_dict[h] = r_id
                newid_rel_dict[r_id] = h
                r_id += 1
            else:
                rel_newid_dict[h] = newrel_newid_dict[get_name(h)]
            id_newid_reldict[t_id] = newrel_newid_dict[get_name(h)]
        f2.close()

    with open(zh_ent_path, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            t_id, h = params[0].strip(), params[1].strip()
            # 记录旧id - 文本
            if t_id not in id_ent_dict:
                id_ent_dict[t_id] = h
            # 记录新文本 - 新id
            if get_name(h) not in newent_newid_dict:
                newent_newid_dict[get_name(h)] = h_id
                newid_newent_dict[h_id] = get_name(h)
                ent_newid_dict[h] = h_id
                newid_ent_dict[h_id] = h
                h_id += 1
            else:
                ent_newid_dict[h] = newent_newid_dict[get_name(h)]
            id_newid_entdict[int(t_id)] = int(newent_newid_dict[get_name(h)])
        f1.close()

    with open(en_ent_path, "r", encoding="utf-8-sig") as f2:
        for line in f2.readlines():
            params = str.strip(line).split(sep='\t')
            t_id, h = params[0].strip(), params[1].strip()
            # 记录旧id - 文本
            if t_id not in id_ent_dict:
                id_ent_dict[t_id] = h
            # 记录新文本 - 新id
            if get_name(h) not in newent_newid_dict:
                newent_newid_dict[get_name(h)] = h_id
                newid_newent_dict[h_id] = get_name(h)
                ent_newid_dict[h] = h_id
                newid_ent_dict[h_id] = h
                h_id += 1
            else:
                ent_newid_dict[h] = newent_newid_dict[get_name(h)]
            id_newid_entdict[int(t_id)] = int(newent_newid_dict[get_name(h)])
        f2.close()

    # 保存字典文件
    with open('./zh_en/rel_newid_dict.pkl', 'wb') as f:
        pickle.dump(rel_newid_dict, f)
    with open('./zh_en/ent_newid_dict.pkl', 'wb') as f:
        pickle.dump(ent_newid_dict, f)
    with open('./zh_en/newid_ent_dict.pkl', 'wb') as f:
        pickle.dump(newid_ent_dict, f)
    with open('./zh_en/newid_rel_dict.pkl', 'wb') as f:
        pickle.dump(newid_rel_dict, f)
    with open('./zh_en/newent_newid_dict.pkl', 'wb') as f:
        pickle.dump(newent_newid_dict, f)
    with open('./zh_en/newrel_newid_dict.pkl', 'wb') as f:
        pickle.dump(newrel_newid_dict, f)
    with open('./zh_en/newid_newent_dict.pkl', 'wb') as f:
        pickle.dump(newid_newent_dict, f)
    with open('./zh_en/newid_newrel_dict.pkl', 'wb') as f:
        pickle.dump(newid_newrel_dict, f)
    with open('./zh_en/id_ent_dict.pkl', 'wb') as f:
        pickle.dump(id_ent_dict, f)
    with open('./zh_en/id_rel_dict.pkl', 'wb') as f:
        pickle.dump(id_rel_dict, f)
    with open('./zh_en/id_newid_reldict.pkl', 'wb') as f:
        pickle.dump(id_newid_reldict, f)
    with open('./zh_en/id_newid_entdict.pkl', 'wb') as f:
        pickle.dump(id_newid_entdict, f)
    # entity2id.txt
    entity_id = []
    for ent, v in newent_newid_dict.items():
        entity_id.append([ent, v])
    data_write_ents("./zh_en/entity2id.txt", entity_id)
    # relation2id.txt
    relation_id = []
    for ent, v in newrel_newid_dict.items():
        relation_id.append([ent, v])
    data_write_ents("./zh_en/relation2id.txt", relation_id)


