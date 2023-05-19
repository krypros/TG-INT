import pickle


def data_write_triple(file_name, datas):
    with open(file_name, 'w+', encoding='gb18030') as f:
        f.write(str(len(datas)) + '\n')
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\n')
    print("保存文件成功，处理结束")


def data_write_rel(file_name, datas):
    with open(file_name, 'w+', encoding='gb18030') as f:
        f.write(str(len(datas)) + '\n')
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\n')
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
    store_path = "./zh_en/"
    sup_path = "../data/dbp15k/zh_en/sup_pairs"
    train_path = "./zh_en/train2id.txt"
    rel_path = "./zh_en/relation2id.txt"
    # 用于从旧id定位旧文本
    with open('./zh_en/id_ent_dict.pkl', 'rb') as f1:
        id_ent_dict = pickle.load(f1)
    with open('./zh_en/ent_newid_dict.pkl', 'rb') as f1:
        ent_newid_dict = pickle.load(f1)
    result_triple = []
    rels = []
    with open(train_path, "r", encoding="gb18030") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            if len(params) < 3:
                continue
            h, t, r = params[0].strip(), params[1].strip(), params[2].strip()
            result_triple.append([h, t, r])

    with open(rel_path, "r", encoding="gb18030") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            if len(params) < 2:
                continue
            r_id, r = params[0].strip(), params[1].strip()
            rels.append([r_id, r])
    rels.append([len(rels), 'alike'])
    # 读取EA的对齐对，加入anchor关系
    with open(sup_path, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            if len(params) < 2:
                continue
            h_1, h_2 = params[0].strip(), params[1].strip()
            result_triple.append([ent_newid_dict[id_ent_dict[h_1]], ent_newid_dict[id_ent_dict[h_2]], len(rels)-1])
            result_triple.append([ent_newid_dict[id_ent_dict[h_2]], ent_newid_dict[id_ent_dict[h_1]], len(rels)-1])
    data_write_triple(store_path + "train2idAdd.txt", result_triple)
    data_write_rel(store_path + "relation2idAdd.txt", rels)