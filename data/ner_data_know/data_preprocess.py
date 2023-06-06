# -*- coding:utf-8 -*-
import pandas as pd
import json
import os
from tqdm import tqdm

# with open("train_source1.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# knws = []
# for item in data:
#     knws.append(item["text"])
# print(knws)
# fw1 = open("dev/input.seq.char.1", "w", encoding="utf-8")
# fw2 = open("dev/output.seq.bio.1", "w", encoding="utf-8")

# with open("dev/input.seq.char", "r", encoding="utf-8") as f1, open("dev/output.seq.bio", "r", encoding="utf-8") as f2:
#     for line1, line2 in zip(f1,f2):
#         ind = knws.index("".join(line1.strip().split()))
#         kn = data[ind]["source"]
#         fw1.write(line1.strip()+" # "+" ".join(list(kn))+"\n")
#         fw2.write(line2.strip()+" # "+" ".join(list(kn))+"\n")

# fw1.close()
# fw2.close()



with open("test_source1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

knws = []
for item in data:
    knws.append(item["text"].strip())
print(knws)
fw1 = open("GuNER2023_test_public_know.txt", "w", encoding="utf-8")

with open("GuNER2023_test_public.txt", "r", encoding="utf-8") as f1:
    for line1 in f1:
        ind = knws.index(line1.strip())
        kn = data[ind]["source"]
        fw1.write(line1.strip()+"#"+kn+"\n")

fw1.close()


# input_file = "GuNER2023_train.txt"

# # 帝曰：「{玄齡|PER}、{如晦|PER}不以勳舊進，特其才可與治天下者，{師合|PER}欲以此離間吾君臣邪？」斥嶺表。
# def get_labels(seq):
#     seq_lst = list(seq)
#     word_lst = []
#     label_lst = []
#     flag = False
#     flag_l = False
#     ent = []
#     l_str = ""
#     for w in seq_lst:
#         if w == "{":
#             ent = []
#             flag = True
#         elif w == "|":
#             l_str = ""
#             flag_l = True
#             flag = False
#         elif w == "}":
#             word_lst = word_lst + ent
#             label_lst = label_lst + ["B-"+l_str] + ["I-"+l_str]*(len(ent)-1)
#             ent = []
#             l_str = ""
#             flag = False
#             flag_l = False
#         else:
#             if flag:
#                 ent.append(w)
#             elif flag_l:
#                 l_str += w
#             else:
#                 word_lst.append(w)
#                 label_lst.append("O")

#     assert len(word_lst) == len(label_lst)

#     return word_lst, label_lst

# if __name__ == "__main__":
#     K_fold = 5
#     for i in range(K_fold):
#         if not os.path.exists("ner_data_"+str(i+1)):
#             os.mkdir("ner_data_"+str(i+1))
#             os.mkdir("ner_data_"+str(i+1)+"/train")
#             # os.mkdir("ner_data_"+str(i+1))
#             os.mkdir("ner_data_"+str(i+1)+"/dev")

#     # f_text_train = open("ner_data/train/input.seq.char", "w", encoding="utf-8")
#     # f_label_train = open("ner_data/train/output.seq.bio", "w", encoding="utf-8")

#     # f_text_dev = open("ner_data/dev/input.seq.char", "w", encoding="utf-8")
#     # f_label_dev = open("ner_data/dev/output.seq.bio", "w", encoding="utf-8")

#     all_sample = []
#     all_label = set(["PAD", "UNK"])

#     with open(input_file, "r", encoding="utf-8") as f:
#         for line in tqdm(f):
#             word_lst, label_lst = get_labels(line.strip())
#             all_sample.append([word_lst, label_lst])
#             all_label = all_label|set(label_lst)
#     import random
#     random.seed(0)

#     random.shuffle(all_sample)

#     list_id = list(range(0, 5, 1))

#     for ii in range(len(list_id)):
#         if ii+1 < len(list_id):
#             train_samples = all_sample[0:int(len(all_sample)*ii/5)] + all_sample[int(len(all_sample)*(ii+1)/5):]
#             dev_samples = all_sample[int(len(all_sample)*ii/5):int(len(all_sample)*(ii+1)/5)]
#         else:
#             train_samples = all_sample[0:int(len(all_sample)*ii/5)]
#             dev_samples = all_sample[int(len(all_sample)*ii/5):]

#         f_text_train = open("ner_data_"+str(list_id[ii]+1)+"/train/input.seq.char", "w", encoding="utf-8")
#         f_label_train = open("ner_data_"+str(list_id[ii]+1)+"/train/output.seq.bio", "w", encoding="utf-8")

#         f_text_dev = open("ner_data_"+str(list_id[ii]+1)+"/dev/input.seq.char", "w", encoding="utf-8")
#         f_label_dev = open("ner_data_"+str(list_id[ii]+1)+"/dev/output.seq.bio", "w", encoding="utf-8")

#         for sample in train_samples:
#             f_text_train.write(" ".join(sample[0])+"\n")
#             f_label_train.write(" ".join(sample[1])+"\n")

#         for sample in dev_samples:
#             f_text_dev.write(" ".join(sample[0])+"\n")
#             f_label_dev.write(" ".join(sample[1])+"\n")

#         f_text_train.close()
#         f_label_train.close()
#         f_text_dev.close()
#         f_label_dev.close()






    # train_samples = all_sample[:int(len(all_sample)*0.8)]
    # dev_samples = all_sample[int(len(all_sample)*0.8):]

    # for sample in train_samples:
    #     f_text_train.write(" ".join(sample[0])+"\n")
    #     f_label_train.write(" ".join(sample[1])+"\n")

    # for sample in dev_samples:
    #     f_text_dev.write(" ".join(sample[0])+"\n")
    #     f_label_dev.write(" ".join(sample[1])+"\n")

    # f_text_train.close()
    # f_label_train.close()
    # f_text_dev.close()
    # f_label_dev.close()

    # f_label = open("ner_data/vocab_bio.txt", "w", encoding="utf-8")
    # for l in all_label:
    #     f_label.write(l+"\n")
    # f_label.close()




# def read_train_data(fn):
#     """读取用于训练的json数据"""
#     with open(fn, 'r', encoding='utf-8') as fr:
#         data = json.load(fr)
#     return data

# def read_test_data(fn):
#     """读取用于测试的json数据"""
#     with open(fn, 'r', encoding='utf-8') as fr:
#         data = json.load(fr)
#     return data

# def read_example_ids(fn):
#     """读取划分数据集的文件"""
#     example_ids = pd.read_csv(fn)
#     return example_ids

# def save_train_data(data, example_ids, mode, fn1, fn2):
#     """
#     训练集和验证集的数据转换
#     :param data: 用于训练的json数据
#     :param example_ids: 样本id划分数据
#     :param mode: train/dev
#     :param fn1: 文本序列 input.seq.char
#     :param fn2: BIO序列标签 output.seq.bio
#     :return:
#     """
#     eids = example_ids[example_ids['split'] == mode]['example_id'].to_list()
#     # # sample
#     # n = len(eids)
#     # eids = eids[:int(n*0.01)]
#     seq_in, seq_bio = [], []
#     for eid in eids:
#         tmp_data = data[str(eid)]
#         tmp_dialogue = tmp_data['dialogue']
#         for i in range(len(tmp_dialogue)):
#             tmp_sent = list(tmp_dialogue[i]['speaker'] + '：' + tmp_dialogue[i]['sentence'])
#             tmp_bio = ['O'] * 3 + tmp_dialogue[i]['BIO_label'].split(' ')
#             assert len(tmp_sent) == len(tmp_bio)
#             seq_in.append(tmp_sent)
#             seq_bio.append(tmp_bio)
#     assert len(seq_in) == len(seq_bio)
#     print(mode, '句子数量为：', len(seq_in))
#     # 数据保存
#     with open(fn1, 'w', encoding='utf-8') as f1:
#         for i in seq_in:
#             tmp = ' '.join(i)
#             f1.write(tmp+'\n')
#     with open(fn2, 'w', encoding='utf-8') as f2:
#         for i in seq_bio:
#             tmp = ' '.join(i)
#             f2.write(tmp+'\n')

# def get_vocab_char(fr1, fr2, fw):
#     """获得字符种类字典"""
#     chars = []
#     with open(fr1, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             line = line.strip().split(' ')
#             for i in line:
#                 if i not in chars:
#                     chars.append(i)
#     with open(fr2, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             line = line.strip().split(' ')
#             for i in line:
#                 if i not in chars:
#                     chars.append(i)
#     add_tokens = ['[PAD]', '[UNK]', '[SEP]', '[SPA]']
#     chars = add_tokens + chars
#     print('字符种类：', len(chars))

#     with open(fw, 'w', encoding='utf-8') as f:
#         for w in chars:
#             f.write(w + '\n')

# def get_vocab_bio(fr1, fr2, fw):
#     """获得bio种类字典"""
#     bio = []
#     with open(fr1, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             line = line.strip().split(' ')
#             for i in line:
#                 if i not in bio:
#                     bio.append(i)
#     with open(fr2, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             line = line.strip().split(' ')
#             for i in line:
#                 if i not in bio:
#                     bio.append(i)

#     bio = sorted(list(bio), key=lambda x: (x[2:], x[:2]))
#     add_tokens = ["PAD", "UNK"]
#     bio = add_tokens + bio
#     print('bio种类：', len(bio))

#     with open(fw, 'w', encoding='utf-8') as f:
#         for w in bio:
#             f.write(w + '\n')


# if __name__ == "__main__":

#     train_data = read_train_data('../../../dataset/train.json')
#     example_ids = read_example_ids('../../../dataset/split.csv')

#     data_dir = 'ner_data'
#     if not os.path.exists(data_dir):
#         os.makedirs(data_dir)
#         os.makedirs(data_dir+'/train')
#         os.makedirs(data_dir+'/dev')

#     # 获得训练数据
#     save_train_data(
#         train_data,
#         example_ids,
#         'train',
#         os.path.join(data_dir, 'train', 'input.seq.char'),
#         os.path.join(data_dir, 'train', 'output.seq.bio')
#     )

#     # 获得验证数据
#     save_train_data(
#         train_data,
#         example_ids,
#         'dev',
#         os.path.join(data_dir, 'dev', 'input.seq.char'),
#         os.path.join(data_dir, 'dev', 'output.seq.bio')
#     )

#     # 获取一些vocab信息
#     get_vocab_bio(
#         os.path.join(data_dir, 'train', 'output.seq.bio'),
#         os.path.join(data_dir, 'dev', 'output.seq.bio'),
#         os.path.join(data_dir, 'vocab_bio.txt')
#     )
