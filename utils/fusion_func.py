import re


def write_output(seq_preds_list, lines):
    outputs = []
    for i in range(len(seq_preds_list)):
        pred_seq = seq_preds_list[i]
        org_words = lines[i]
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
                sent += w
            tmp = tag.split("-")[-1]

        if flag:
            sent += "|"+tmp+"}"
            flag = False

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
            if idx==0 and lb2.endswith("-PER") and lb3=="O" and label_lst2_new[idx+1].endswith("-PER") and label_lst2_new[idx+2].endswith("-PER") and label_lst3[idx+1].endswith("-PER") and label_lst3[idx+2].endswith("-PER"):
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

    return target_sen

def cal_disconsis(consist_cal):
    it_ = []
    for item in consist_cal:
        c = consist_cal[item]
        if "PER" in c and "OFI" in c:
            if len(c["PER"])>1 and len(c["OFI"])>1 and (len(c["PER"])/len(c["OFI"])*1.0 >= 0.5):
                it_.append(item)
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
    