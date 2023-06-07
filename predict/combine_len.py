# -*- coding:utf-8 -*-
import re
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from utils.fusion_func import *
base_path = "predict/"
wiki_know_path = "data/wiki_knowledge/"
raw_data_path = "data/raw/"


fw = open(base_path + "test_submission_submit.txt", "w", encoding="utf-8")

seq_preds_list = []
lines = []
outputs_org = []
IB_4 = []
IB_10 = []
seq_lb = []
with open(base_path + "submission_test_Kfold.txt", "r", encoding="utf-8") as f1, open(base_path + "submission_test_IB_10.txt", "r", encoding="utf-8") as f2, open(base_path + "submission_test_IB_4.txt", "r", encoding="utf-8") as f3:
    for idx, (line1, line2, line3) in enumerate(zip(f1, f2, f3)):
        IB_4.append(line3.strip())
        IB_10.append(line2.strip())
        seq_lb.append(line1.strip())

        word_lst1, label_lst1 = get_labels(line1.strip())
        word_lst2, label_lst2 = get_labels(line2.strip())
        word_lst3, label_lst3 = get_labels(line3.strip())

        label_lst1_new = mask_labels(label_lst1, length=False)
        label_lst2_new = mask_labels(label_lst2, length=True)
        assert len(label_lst1_new) == len(label_lst2_new) == len(word_lst1)

        label_lst = combine_conflict(word_lst1, label_lst1, label_lst2, label_lst1_new, label_lst2_new, label_lst3)

        seq_preds_list.append(label_lst)
        lines.append(word_lst1)

outputs = write_output(seq_preds_list, lines)

PER_vocab = []
with open(wiki_know_path + "PER_vocab.txt", "r", encoding="utf-8") as f:
    for line in f:
        PER_vocab.append(line.strip())
OFI_vocab = []
with open(wiki_know_path + "OFI_vocab.txt", "r", encoding="utf-8") as f:
    for line in f:
        OFI_vocab.append(line.strip())

with open(base_path + "conflicts_filter.json", "r", encoding="utf-8") as f:
    consist_cal = json.load(f)

data_train = []
with open(raw_data_path + "GuNER2023_train.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_train.append(line.strip())

result_know = []
with open(base_path + "submission_test_know.txt", "r", encoding="utf-8") as f:
    for line in f:
        result_know.append(line.strip())

result_slide = []
with open(base_path + "submission_test_slide.txt", "r", encoding="utf-8") as f:
    for line in f:
        result_slide.append(line.strip())


it_ = cal_disconsis(consist_cal)

pattern_ = re.compile(r"\{\w+\|PER\}，(?=\{\w+\|OFI\})")
for sen, ib, ib10, sql, rk, rs in zip(outputs, IB_4, IB_10, seq_lb, result_know, result_slide):
    per = set(re.findall("\{([^|]+)\|PER\}", sen))
    text = sen
    for item in per:
        if len(item) < 2 and text.count(item) < 3:
            continue
        pattern = r"(?<!\{)"+item+r"(?!\|PER\})"
        replacement = r"{"+item+r"|PER}"
        text = re.sub(pattern, replacement, text)
    text = text.replace("{]", "]{")

    text = span_match(text)
    for p in PER_vocab:
        if p in text and p not in re.findall("\{([^|]+)\|PER\}", text) and p+"|PER}" not in text:
            if p in re.findall("\{([^|]+)\|OFI\}", text):
                if len(p) > 2:
                    text = text.replace("{"+p+"|OFI}", "{"+p+"|PER}")
                else:
                    text = text.replace("{"+p+"|OFI}", p)
            else:
                text = text.replace(p, "{"+p+"|PER}")

    for p in OFI_vocab:
        if p in text and p not in re.findall("\{([^|]+)\|OFI\}", text) and p+"|OFI}" not in text:
            if p in re.findall("\{([^|]+)\|PER\}", text):
                if len(p) > 2:
                    text = text.replace("{"+p+"|PER}", "{"+p+"|OFI}")
                else:
                    text = text.replace("{"+p+"|PER}", p)
            else:
                text = text.replace(p, "{"+p+"|OFI}")

    text = text if len(pattern_.findall(text)) >= len(pattern_.findall(ib)) else ib

    pattern_q = re.compile(r"(?<=「\{\w\|PER\})\w(?=\{\w\|PER\})")
    su = pattern_q.findall(text)
    if len(su) > 0:
        text = text.replace("|PER}"+su[0]+"{", "|PER}{"+su[0])

    ofi1 = re.findall("\{([^|]+)\|OFI\}", ib)
    ofi2 = re.findall("\{([^|]+)\|OFI\}", sen)
    diff = list(set(ofi1)-set(ofi2)) if len(ofi1)>len(ofi2) else set()
    if len(diff)>0 and len(diff[0])>2:
        text = ib

    per2 = re.findall("\{([^|]+)\|PER\}", sen)
    if len(set(ofi1)&set(per2)) > 0:
        for item in set(ofi1)&set(per2):
            text = text.replace("{"+item+"|PER}", item)
    text = combine_book(text, sql, ib10, ib)

    text = deal_disconsis(it_, text)

    text = consistency_train(data_train, text, rk, rs, ib)

    fw.write(text+"\n")


fw.close()


