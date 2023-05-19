import pickle
from random import shuffle
import pandas as pd
import numpy as np

def data_write_triple(file_name, datas):
    with open(file_name, 'w+', encoding='utf-8-sig') as f:
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\n')
    print("保存文件成功，处理结束")


def data_write_triple_ke(file_name, datas):
    with open(file_name, 'w+', encoding='utf-8-sig') as f:
        f.write(str(len(datas)) + '\n')
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\n')
    print("保存文件成功，处理结束")


def list_del_dup(dup_list):
    data_repu = pd.DataFrame(dup_list)
    data_repu.drop_duplicates(inplace=True)
    re_list = np.array(data_repu).tolist()
    # re_list = filter(lambda x: "未知" not in str(x), re_list)
    # re_list = [_ for _ in re_list]
    return re_list


if __name__ == '__main__':
    # 用于从旧id定位旧文本
    with open('./zh_en/id_ent_dict.pkl', 'rb') as f1:
        id_ent_dict = pickle.load(f1)
    with open('./zh_en/id_rel_dict.pkl', 'rb') as f1:
        id_rel_dict = pickle.load(f1)
    # 用于从旧文本定位新id
    with open('./zh_en/rel_newid_dict.pkl', 'rb') as f1:
        rel_newid_dict = pickle.load(f1)
    with open('./zh_en/ent_newid_dict.pkl', 'rb') as f1:
        ent_newid_dict = pickle.load(f1)


    # 过滤rel_triple
    trps_1 = []
    path_trp_1 = "../data/dbp15k/zh_en/triples_1"
    path_trp_2 = "../data/dbp15k/zh_en/triples_2"
    with open(path_trp_1, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            h, r, t = params[0].strip(), params[1].strip(), params[2].strip()
            trps_1.append((ent_newid_dict[id_ent_dict[h]],
                           ent_newid_dict[id_ent_dict[t]],
                           rel_newid_dict[id_rel_dict[r]]))
    with open(path_trp_2, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            h, r, t = params[0].strip(), params[1].strip(), params[2].strip()
            trps_1.append((ent_newid_dict[id_ent_dict[h]],
                           ent_newid_dict[id_ent_dict[t]],
                           rel_newid_dict[id_rel_dict[r]]))

    # 保存cnnvd过滤的关系三元组
    trps_1 = list_del_dup(trps_1)
    data_write_triple_ke("./zh_en/train2id_all.txt", trps_1)

