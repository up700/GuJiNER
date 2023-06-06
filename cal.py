# -*- coding:utf-8 -*-
import re

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

fw = open("OFI.txt", "w", encoding="utf-8")

with open("submission_test_Kfold.txt", "r", encoding="utf-8") as f1, open("submission_test_Kfold_.txt", "r", encoding="utf-8") as f2:
	for line1, line2 in zip(f1, f2):
		ofi1 = re.findall("\{([^|]+)\|OFI\}", line1.strip())
		ofi2 = re.findall("\{([^|]+)\|OFI\}", line2.strip())
		if ofi1 == ofi2:
			label = "True"
		else:
			label = "False"
		fw.write(label+" "+" ".join(ofi1)+" # "+" ".join(ofi2)+"\n")
fw.close()


