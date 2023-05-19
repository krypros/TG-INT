def data_write_ents(file_name, datas):
    with open(file_name, 'w+', encoding='gb18030') as f:
        f.write(str(len(datas)) + '\n')
        for value in datas:
            f.write(str(value[0]) + '\t' + str(value[1]) + '\n')
    print("保存文件成功，处理结束")


if __name__ == '__main__':
    rel_path = "./zh_en/relation2id.txt"
    ent_path = "./zh_en/entity2id.txt"
    ent_list = []
    rel_list = []
    with open(ent_path, "r", encoding="utf-8-sig") as f1:
        for line in f1.readlines():
            params = str.strip(line).split(sep='\t')
            e, e_id = params[0].strip(), params[1].strip()
            ent_list.append((e_id, e))

    with open(rel_path, "r", encoding="utf-8-sig") as f2:
        for line in f2.readlines():
            params = str.strip(line).split(sep='\t')
            r, r_id = params[0].strip(), params[1].strip()
            rel_list.append((r_id, r))

    data_write_ents("./zh_en/entity2id.txt", ent_list)
    data_write_ents("./zh_en/relation2id.txt", rel_list)