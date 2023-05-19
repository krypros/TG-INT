from transformers import BertModel
import torch
import torch.nn as nn
import pickle

class Basic_Bert_Unit_model(nn.Module):
    def __init__(self,input_size, result_size):
        super(Basic_Bert_Unit_model,self).__init__()
        emb_model = torch.load("../data/old_quate_zh200.ckpt", map_location=torch.device('cuda')) #
        # self.emb_dict = pickle.load("../data/id_emb_dict.pkl")

        self.emb_s_a = nn.Embedding(emb_model['emb_s_a.weight'].shape[0], emb_model['emb_s_a.weight'].shape[1])
        self.emb_x_a = nn.Embedding(emb_model['emb_s_a.weight'].shape[0], emb_model['emb_s_a.weight'].shape[1])
        self.emb_y_a = nn.Embedding(emb_model['emb_s_a.weight'].shape[0], emb_model['emb_s_a.weight'].shape[1])
        self.emb_z_a = nn.Embedding(emb_model['emb_s_a.weight'].shape[0], emb_model['emb_s_a.weight'].shape[1])
        self.emb_s_a.weight.data = emb_model['emb_s_a.weight']
        self.emb_x_a.weight.data = emb_model['emb_x_a.weight']
        self.emb_y_a.weight.data = emb_model['emb_y_a.weight']
        self.emb_z_a.weight.data = emb_model['emb_z_a.weight']
        with open('../data/dbp15k/zh_en/id_newid_entdict.pkl' , 'rb') as f:
            self.entid_dict = pickle.loads(f.read())

        self.result_size = result_size
        self.input_size = input_size
        self.bert_model = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.mlp_head = nn.Sequential(
            nn.Dropout(p=0.1),
            nn.Linear(input_size+800, input_size),
        )
        self.entity_fc = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(800, 800),
            nn.Tanh()
        )

        self.out_linear_layer = nn.Linear(self.input_size,self.result_size)
        self.dropout = nn.Dropout(p = 0.1)



    def forward(self,batch_word_list, attention_mask, eids=None):
        x = self.bert_model(input_ids=batch_word_list, attention_mask=attention_mask)#token_type_ids =token_type_ids
        #print(eids)
        #print(len(eids))
        sequence_output, pooled_output = x
        cls_vec = sequence_output[:,0]
        if eids != None:
            tmp_index = torch.tensor([self.entid_dict[i] for i in eids]).cuda()
            #tmp_index = torch.tensor([100]).cuda()
            emb_s = self.emb_s_a(tmp_index)
            emb_x = self.emb_x_a(tmp_index)
            emb_y = self.emb_y_a(tmp_index)
            emb_z = self.emb_z_a(tmp_index)
            # s_emb = torch.tensor(self.emb_dict[batch_word_list[0]], device='cuda')
        # print(output.shape)
            s_emb = torch.cat((emb_s, emb_x, emb_y, emb_z), dim=1)
            s_emb = self.entity_fc(s_emb)
        #print(s_emb.shape)
        #a = torch.stack([s_emb for i in range(batch_word_list.shape[0])], dim=0) # [128, 200]
            s_emb = torch.cat((cls_vec, s_emb), dim=1)  # [128, 968]
        #print(s_emb.shape)
        # s_output, weights = self.MultiAttention(s, h_n)
            output = self.mlp_head(s_emb) # torch.cat((output, s_emb), dim=0)
        else:
            output = self.dropout(cls_vec)
            output = self.out_linear_layer(output)
        return output

    def quate_sim(self,ent_1, ent_2):
        s_a, x_a, y_a, z_a = ent_1
        s_c, x_c, y_c, z_c = ent_2
        score_r = (s_a * s_c + x_a * x_c + y_a * y_c + z_a * z_c)
        score = nn.Softplus()(-score_r)
        return score

