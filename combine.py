# -*- coding:utf-8 -*-

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

# def write_results(seq_preds_list, lines):
#     outputs = []
#     for i in range(len(seq_preds_list)):
#         pred_seq = seq_preds_list[i]
#         org_words = lines[i]
#         assert len(pred_seq) == len(org_words)
#         print(" ".join(pred_seq))
#         sent = ""
#         flag = False
#         tmp = "O"
#         for tag, w in zip(pred_seq, org_words):
#             if tag == "O":
#                 if flag:
#                     sent += "|"+tmp+"}"+w
#                     flag = False
#                 else:
#                     sent += w
#             elif tag.startswith("B-"):
#                 if flag:
#                     sent += "|"+tmp+"}"
#                     flag = False
#                 sent += "{"+w
#                 flag = True
#             elif tag.startswith("I-"):
#                 if not flag:
#                     sent += "{"
#                 sent += w
#                 flag = True
#             tmp = tag.split("-")[-1]

#         if flag:
#             sent += "|"+tmp+"}"
#             flag = False
#         print(sent)

#         outputs.append(sent)


#         # eid = eids[i]
#         # sid = sids[i]
#         # if eid not in outputs:
#         #     outputs[eid] = {}
#         #     outputs[eid][sid] = ' '.join(pred_seq[3:])  # 只保留句子的BIO标签，删去了speaker的BIO标签
#         # else:
#         #     outputs[eid][sid] = ' '.join(pred_seq[3:])

#     # pred_path = os.path.join(pred_config.test_output_file)
#     with open("submission_test_Kfold_token.txt", 'w', encoding='utf-8') as f:
#         for item in outputs:
#             f.write(item+"\n")


# K_fold = [open("submission_test_"+str(i+1)+".txt", "r", encoding="utf-8") for i in range(5)]

# preds = {}


# for f in K_fold:
# 	ind = 0
# 	for line in f:
# 		if ind not in preds:
# 			preds[ind] = {}

# 		word_lst, label_lst = get_labels(line.strip())
# 		for i in range(len(label_lst)):
# 			if i not in preds[ind]:
# 				preds[ind][i] = []
# 			preds[ind][i].append(label_lst[i])
		
# 		# preds[ind].append((word_lst, label_lst))

# 		ind += 1
# 	f.close()

# labels_p = []
# for ind in preds:
# 	p = preds[ind]
# 	preds_ = []
# 	for i in range(len(p)):
# 		test = p[i]
# 		pl = max(set(test), key=test.count)
# 		preds_.append(pl)
# 	labels_p.append(preds_)

# f = open("submission_test_"+str(1)+".txt", "r", encoding="utf-8")
# words = []
# for line in f:
# 	word_lst, label_lst = get_labels(line.strip())
# 	words.append(word_lst)
# f.close()

# write_results(labels_p, words)
# # f = open("submission_test_Kfold_.txt", "w", encoding="utf-8")
# # f.close()

###############
K_fold = [open("submission_test_"+str(i+1)+".txt", "r", encoding="utf-8") for i in range(5)]

preds = {}


for f in K_fold:
	ind = 0
	for line in f:
		if ind not in preds:
			preds[ind] = []
		preds[ind].append(line.strip())

		ind += 1
	f.close()

f = open("submission_test_Kfold.txt", "w", encoding="utf-8")
for ind in preds:
	p = preds[ind]
	max_n = 0
	max_item = ""
	setp = list(set(p))
	setp.sort(key=p.index)
	for item in setp:
		# print(p.count(item))
		# if p.count(item) == 2 and len(setp)==3:
		# 	print(item)
		if p.count(item) >= max_n:
			max_n = p.count(item)
			max_item = item
	# print("+==========="+str(ind+1))
	f.write(max_item+"\n")

f.close()