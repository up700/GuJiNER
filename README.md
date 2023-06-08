
## Requirements
- python==3.7.4
- pytorch==1.11.0
- [transformers==4.5.1](https://github.com/huggingface/transformers)
- numpy==1.21.6
- tqdm
- argparse==1.1
- torchcrf==0.7.2
- seqeval


## Overview

以下内容为该项目的主要结构，其中
* 根目录下的**start_train.sh**脚本为训练启动脚本（需要根据显存和GPU个数进行相应配置）。
* 根目录下的**start_predict.sh**脚本为预测脚本用于生成最终的提交文件。
* 文件**predict/test_submission_submit.txt**为最终的提交文件。

```
│  main_bio.py                            #以BIO方式进行训练的main文件
│  main_span.py                           #以SPAN方式进行训练的main文件
│  README.md                              #Readme文件
│  start_predict.sh                       #生成预测结果的sh脚本文件
│  start_train.sh                         #进行启动训练的sh脚本文件
│  trainer.py                             #BIO方式的训练器
│
├─data
│  ├─Guwen-large                          #以SPAN方式训练所需数据
│  ├─ner_data_1                           #五折交叉验证-第一折数据
│  ├─ner_data_2                           #五折交叉验证-第二折数据
│  ├─ner_data_3                           #五折交叉验证-第三折数据
│  ├─ner_data_4                           #五折交叉验证-第四折数据
│  ├─ner_data_5                           #五折交叉验证-第五折数据
│  ├─ner_data_know                        #基于古文所在篇章知识的训练数据
│  ├─ner_data_know_slide                  #基于古文所在篇章知识的滑窗训练数据
│  ├─raw                                  #测评原始数据集
│  └─wiki_knowledge                       #来自于维基百科的外部知识
│
├─models                                  #以SPAN方式进行训练相关的model
├─predict
│  ├─combine.py                           #生成五折交叉验证的结果
│  ├─combine_len.py                       #生成最终的融合结果（需先执行combine.py）
│  ├─conflicts_filter.json                #训练集中标注冲突的实体
│  ├─predict.py                           #生成以BIO方式训练的测试集结果
│  ├─predict_know.py                      #生成引入古文篇章知识训练的测试集结果
│  ├─predict_slide.py                     #生成引入古文篇章知识并使用滑窗机制进训练的测试集结果
│  ├─submission_test_1.txt                #在第一折数据训练模型的测试集预测结果
│  ├─submission_test_2.txt                #在第二折数据训练模型的测试集预测结果
│  ├─submission_test_3.txt                #在第三折数据训练模型的测试集预测结果
│  ├─submission_test_4.txt                #在第四折数据训练模型的测试集预测结果
│  ├─submission_test_5.txt                #在第五折数据训练模型的测试集预测结果
│  ├─submission_test_IB_10.txt            #SPAN模型最大长度为10的测试集预测结果
│  ├─submission_test_IB_4.txt             #SPAN模型最大长度为4的测试集预测结果
│  ├─submission_test_Kfold.txt            #五折交叉验证的最终融合结果
│  ├─submission_test_know.txt             #引入古文所在篇章知识的模型在测试集的预测结果
│  ├─submission_test_slide.txt            #引入古文所在篇章知识和滑动窗口的模型在测试集的预测结果
│  └─test_submission_submit.txt           #**最终提交结果**
│
├─utils                                   #以BIO方式训练和预测过程中常用到的工具函数
└─utils_IB                                #以SPAN方式训练和预测过程中常用到的工具函数
```



# Checkpoints

链接：https://pan.baidu.com/s/10Xj5xQbyiZ16kbvC3x6kAA 
提取码：nl1j 

下载checkpoints文件并解压到根目录，根目录需存在以下目录才可正常预测：out-large、roberta-classical-chinese-large-char、save_model_1、save_model_2、save_model_3、save_model_4、save_model_5、save_model_know、save_model_know_slide。


## How to run

在将所有的checkpoint文件夹解压放在根目录后，可以通过以下命令，对最终结果进行预测。最终结果文件为predict/test_submission_submit.txt
```console
sh start_predict.sh
```

在配置好环境后，运行以下命令也可开始重新训练。根据GPU数量和显存大小进行更改与配置。
```console
sh start_train.sh
```



