# -*- coding:utf-8 -*-
import os

file_path = "/data/zhangxinghua/GuJi_NER/BERT-NER/data/ner_data"
train_file_text = os.path.join(file_path, "train/input.seq.char")
train_file_label = os.path.join(file_path, "train/output.seq.bio")
fw = open("train.txt", "w", encoding="utf-8")
with open(train_file_text, "r", encoding="utf-8") as f1, open(train_file_label, "r", encoding="utf-8") as f2:
	for line1, line2 in zip(f1, f2):
		for w, l in zip(line1.strip().split(), line2.strip().split()):
			fw.write(w+" "+l+"\n")
		fw.write("\n")
fw.close()

dev_file_text = os.path.join(file_path, "dev/input.seq.char")
dev_file_label = os.path.join(file_path, "dev/output.seq.bio")
fw = open("dev.txt", "w", encoding="utf-8")
with open(dev_file_text, "r", encoding="utf-8") as f1, open(dev_file_label, "r", encoding="utf-8") as f2:
	for line1, line2 in zip(f1, f2):
		for w, l in zip(line1.strip().split(), line2.strip().split()):
			fw.write(w+" "+l+"\n")
		fw.write("\n")
fw.close()
