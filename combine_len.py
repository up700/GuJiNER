# -*- coding:utf-8 -*-
import re
import json

def write_output(seq_preds_list, lines):
    outputs = []
    for i in range(len(seq_preds_list)):
        pred_seq = seq_preds_list[i]
        org_words = lines[i]
        # print(" ".join(pred_seq))
        sent = ""
        flag = False
        tmp = "O"
        for tag, w in zip(pred_seq, org_words):
            if tag == "O":
                if flag:
                    sent += "|"+tmp+"}"+w
                    flag = False
                else:
                    sent += w
            elif tag.startswith("B-"):
                if flag:
                    sent += "|"+tmp+"}"
                    flag = False
                sent += "{"+w
                flag = True
            elif tag.startswith("I-"):
                # if not flag:
                #     sent += "{"
                sent += w
                # flag = True
            tmp = tag.split("-")[-1]

        if flag:
            sent += "|"+tmp+"}"
            flag = False
        # print(sent)

        outputs.append(sent)

    return outputs

def get_labels(seq):
    seq_lst = list(seq)
    word_lst = []
    label_lst = []
    flag = False
    flag_l = False
    ent = []
    l_str = ""
    for w in seq_lst:
        if w == "{":
            ent = []
            flag = True
        elif w == "|":
            l_str = ""
            flag_l = True
            flag = False
        elif w == "}":
            word_lst = word_lst + ent
            label_lst = label_lst + ["B-"+l_str] + ["I-"+l_str]*(len(ent)-1)
            ent = []
            l_str = ""
            flag = False
            flag_l = False
        else:
            if flag:
                ent.append(w)
            elif flag_l:
                l_str += w
            else:
                word_lst.append(w)
                label_lst.append("O")

    assert len(word_lst) == len(label_lst)

    return word_lst, label_lst

def mask_labels(label_lst, length):
    start = None
    label_lst_new = []
    for idx in range(len(label_lst)):
        if label_lst[idx] == "O":
            if start is not None:
                if length:
                    if idx-start > 2:
                        label_lst_new += label_lst[start:idx]
                    else:
                        label_lst_new += ["O"]*(idx-start)
                else:
                    if idx-start <= 2:
                        label_lst_new += label_lst[start:idx]
                    else:
                        label_lst_new += ["O"]*(idx-start)
                start = None
            label_lst_new.append("O")
        elif label_lst[idx].startswith("B-"):
            if start is not None:
                if length:
                    if idx-start > 2:
                        label_lst_new += label_lst[start:idx]
                    else:
                        label_lst_new += ["O"]*(idx-start)
                else:
                    if idx-start <= 2:
                        label_lst_new += label_lst[start:idx]
                    else:
                        label_lst_new += ["O"]*(idx-start)
            start = idx

    idx = len(label_lst)

    if start is not None:
        if length:
            if idx-start > 2:
                label_lst_new += label_lst[start:idx]
            else:
                label_lst_new += ["O"]*(idx-start)
        else:
            if idx-start <= 2:
                label_lst_new += label_lst[start:idx]
            else:
                label_lst_new += ["O"]*(idx-start)

    return label_lst_new

def combine_conflict(word_lst1, label_lst1, label_lst2, label_lst1_new, label_lst2_new, label_lst3):
    label_lst = []
    start = None
    org_sen = "".join(word_lst1)
    cnt = 0
    for idx, (word, lb0, lb00, lb1, lb2, lb3) in enumerate(zip(word_lst1, label_lst1, label_lst2, label_lst1_new, label_lst2_new, label_lst3)):
        if lb1 == "O" and lb2 == "O":
            if lb0.startswith("I-"):   # bonie
                label_lst.append(lb0)
            else:
                if lb00.endswith("-BOOK"): # liang book
                    label_lst.append(lb00)
                elif lb00.endswith("-OFI") and org_sen.count(word) >= 2: # OFI junshou
                    label_lst.append(lb00)
                else:
                    label_lst.append("O")
            start = None
        elif lb1 == "O" and lb2 != "O":
            # if lb2.endswith("-PER") and ((lb3=="O" and label_lst3[idx+1].endswith("-PER")) or (lb3.endswith("-PER") and (label_lst2_new[idx-1]=="O" or label_lst3[idx-2]=="O") and (label_lst3[idx-1].endswith("-PER") or label_lst3[idx-2].endswith("-PER")))):
            if idx==0 and lb2.endswith("-PER") and lb3=="O" and label_lst2_new[idx+1].endswith("-PER") and label_lst2_new[idx+2].endswith("-PER") and label_lst3[idx+1].endswith("-PER") and label_lst3[idx+2].endswith("-PER"):
                # label_lst.append(lb3)
                # cnt += 1
                # continue
                lb2 = "O"
                label_lst2_new[idx+1] = label_lst2_new[idx+1].replace("I-", "B-")
                cnt += 1

            if lb0.startswith("B-") and lb2.startswith("I-"):
                lb2 = lb2.replace("I-", "B-")
            if word in set(["。", "，", "？", "！", "、"]):
                lb2 = "O"
                label_lst2_new[idx+1: idx+3] = ["O"]*2
            if start and lb2.startswith("I-"):
                label_lst.append(lb2.replace("I-", "B-"))
                start = None
            else:
                label_lst.append(lb2)
                start = None
        elif lb1 != "O" and lb2 == "O":
            if lb1.endswith("-PER") and lb00.endswith("-OFI"):
                label_lst.append(lb00)
            else:
                if idx+2 < len(word_lst1) and lb1.endswith("-OFI") and lb3 == "O" and (word_lst1[idx+1] in set(["。", "，", "？", "！", "、"]) or word_lst1[idx+2] in set(["。", "，", "？", "！", "、"])):
                    label_lst.append(lb3)
                    # cnt += 1
                else:
                    label_lst.append(lb1)
            start = None
        else:
            label_lst.append(lb1)
            start = True
    # print(cnt)

    return label_lst

def span_match(sen):
    # ents = re.findall("\{([^|]+)\|PER|OFI\}", sen)

    all_ents = []

    for ent in re.finditer(r'\{.*?\}', sen):
        st = ent.start()
        end = ent.end()
        if end - st < 8:
            continue
        all_ents.append(sen[st-2:end+2])
    for ent in all_ents:
        if sen.count(ent) >= 2:
            ent_ = ent.replace("{", "").replace("|PER}", "").replace("|OFI}", "")
            sen = sen.replace(ent, ent_)

    return sen

def combine_book(target_sen, sen_1, sen_2, sen_3):
    book1 = re.findall("\{([^|]+)\|BOOK\}", sen_1)
    book2 = re.findall("\{([^|]+)\|BOOK\}", sen_2)
    book3 = re.findall("\{([^|]+)\|BOOK\}", sen_3)
    book = book1+book2+book3
    for bk in set(book):
        if len(bk)>2 and book.count(bk)<2:
            target_sen = target_sen.replace("{"+bk+"|BOOK}", bk)
            # print(bk)

    return target_sen

def cal_disconsis(consist_cal):
    it_ = []
    for item in consist_cal:
        c = consist_cal[item]
        if "PER" in c and "OFI" in c:
            if len(c["PER"])>1 and len(c["OFI"])>1 and (len(c["PER"])/len(c["OFI"])*1.0 >= 0.5):
                it_.append(item)
                # print(item, len(c["PER"])/len(c["OFI"]), len(c["OFI"])/len(c["PER"]))
    return set(it_)

def deal_disconsis(consist_cal, sen):
    ofi = re.findall("\{([^|]+)\|OFI\}", sen)
    def ends(consist_cal, ofi_item):
        for ii in consist_cal:
            if ofi_item.endswith(ii):
                return True
        return False
    for item in ofi:
        if item in consist_cal or ends(consist_cal, item):
            if sen.count(item) < 2 and item+"|OFI}{" not in sen:
                sen = sen.replace("{"+item+"|OFI}", item)
                # print(sen)

    for i1 in ofi:
        for i2 in ofi:
            if len(i1) > len(i2) and i2.endswith(i1[-2:]) and ofi.index(i1) < ofi.index(i2) and len(i2) <= 3:
                sen = sen.replace("{"+i2+"|OFI}", i2)


    # per = re.findall("\{([^|]+)\|PER\}", sen)
    # for item in per:
    #     if item in consist_cal:
    #         if sen.count(item) < 2 and item+"|PER}{" not in sen:
    #             sen = sen.replace("{"+item+"|PER}", item)
    #             print(sen)
    pattern = r"、\{([^}]+)\|OFI\}\{([^}]+)\|OFI\}，"
    matches = re.findall(pattern, sen)
    if len(matches) > 0:
        # print(sen)
        sen = sen.replace(matches[0][0]+"|OFI}{", matches[0][0])


    return sen

def consistency_train(train_data, sen, sen_know, sen_slide, sen_ib4):
    s = sen.split("，")
    ofi1 = re.findall("\{([^|]+)\|PER\}", s[-1])
    for item in train_data:
        ofi2 = re.findall("\{([^|]+)\|OFI\}", item.split("，")[-1])
        if len(s) > 3 and len(ofi1) > 0 and len(ofi2) > 0:
            if len(ofi1[0])==len(ofi2[0]) and len(set(list(ofi1[0]))&set(list(ofi2[0]))) >= 1.0/2*len(ofi1[0]) and "{"+ofi1[0]+"|PER}。" in sen:
                sen = sen.replace("{"+ofi1[0]+"|PER}", "{"+ofi1[0]+"|OFI}")

    corpus = "".join(train_data)
    ofi = re.findall("\{([^|]+)\|OFI\}", sen)
    for item in ofi:
        if corpus.count(item) > 0 and corpus.count("{"+item+"|OFI}") == 0 and corpus.count("{"+item+"|PER}") == 0 and corpus.count(item+"{") > 0:
            sen = sen.replace("{"+item+"|OFI}", item)

    per1 = re.findall("\{([^|]+)\|PER\}", sen_know)
    per2 = re.findall("\{([^|]+)\|PER\}", sen)
    per = set(per2)-set(per1)
    for p in per:
        if len(p) > 1 and corpus.count(p) > corpus.count("{"+p+"|PER}") and corpus.count("{"+p+"|PER}") > 0:
            sen = sen.replace("{"+p+"|PER}", p)

    ofi1 = re.findall("\{([^|]+)\|OFI\}", sen_slide)
    ofi2 = re.findall("\{([^|]+)\|OFI\}", sen)
    per1 = re.findall("\{([^|]+)\|PER\}", sen_slide)
    per2 = re.findall("\{([^|]+)\|PER\}", sen)
    if len(ofi2) < len(ofi1) and len(per1) == 0 and len(per2) > 0:
        sen = sen_slide

    pattern = r'\{([^{}|]*)\|PER\}\{([^{}|]*)\|OFI\}、\{([^{}|]*)\|OFI\}'
    matches = re.findall(pattern, sen_know)
    if len(matches) > 0:
        matches = matches[0]
        if len(matches) > 2:
            if "{"+matches[0]+"|PER}" in sen_ib4 and "{"+matches[-1]+"|OFI}" in sen_ib4 and "{"+matches[-2]+"|OFI}" not in sen_ib4:
                sen = sen.replace(matches[-2]+ "、"+matches[-1], "{"+matches[-2]+ "、"+matches[-1]+"|OFI}")

    pattern = r"「\{([^}]+)\|OFI\}"
    matches = re.findall(pattern, sen)
    if len(matches) > 0:
        if "{"+matches[0]+"|OFI}{" not in sen:
            sen = sen.replace("{"+matches[0]+"|OFI}", matches[0])

    return sen
    

fw = open("test_submission_submit.txt", "w", encoding="utf-8")

seq_preds_list = []
lines = []
outputs_org = []
IB_4 = []
IB_10 = []
seq_lb = []
with open("submission_test_Kfold.txt", "r", encoding="utf-8") as f1, open("submission_test_IB_10.txt", "r", encoding="utf-8") as f2, open("submission_test_IB_4.txt", "r", encoding="utf-8") as f3:
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
        # print(str(idx+1)+"#")
        # print(label_lst1_new)
        # print(label_lst2_new)
        # print(label_lst)
        # print("######")
        seq_preds_list.append(label_lst)
        lines.append(word_lst1)

outputs = write_output(seq_preds_list, lines)

PER_vocab = []
with open("PER_vocab.txt", "r", encoding="utf-8") as f:
    for line in f:
        PER_vocab.append(line.strip())
OFI_vocab = []
with open("OFI_vocab.txt", "r", encoding="utf-8") as f:
    for line in f:
        OFI_vocab.append(line.strip())

with open("conflicts_filter.json", "r", encoding="utf-8") as f:
    consist_cal = json.load(f)

data_train = []
with open("GuNER2023_train.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_train.append(line.strip())

result_know = []
with open("submission_test_know.txt", "r", encoding="utf-8") as f:
    for line in f:
        result_know.append(line.strip())

result_slide = []
with open("submission_test_slide.txt", "r", encoding="utf-8") as f:
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
                # text = text.replace("{"+p+"|OFI}", "{"+p+"|PER}")
                if len(p) > 2:
                    text = text.replace("{"+p+"|OFI}", "{"+p+"|PER}")
                else:
                    text = text.replace("{"+p+"|OFI}", p)
            else:
                text = text.replace(p, "{"+p+"|PER}")

    for p in OFI_vocab:
        if p in text and p not in re.findall("\{([^|]+)\|OFI\}", text) and p+"|OFI}" not in text:
            if p in re.findall("\{([^|]+)\|PER\}", text):
                # text = text.replace("{"+p+"|PER}", "{"+p+"|OFI}")
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


		# for w, l in zip(word_lst, label_lst):
		# 	fw.write(w+" "+l+"\n")
		# fw.write("\n")
fw.close()


