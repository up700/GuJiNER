# -*- coding:utf-8 -*-
base_path = "predict/"
K_fold = [open(base_path + "submission_test_"+str(i+1)+".txt", "r", encoding="utf-8") for i in range(5)]

preds = {}


for f in K_fold:
	ind = 0
	for line in f:
		if ind not in preds:
			preds[ind] = []
		preds[ind].append(line.strip())

		ind += 1
	f.close()

f = open(base_path + "submission_test_Kfold.txt", "w", encoding="utf-8")
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