import os
import random
import logging
import torch
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score, classification_report

from transformers import BertConfig, RobertaConfig
# from transformers import BertTokenizer, RobertaTokenizer, AutoTokenizer
from transformers import AutoTokenizer
from utils.modeling_nerbert import NERBERT, NERRoBERTa

# 模型类别
MODEL_CLASSES = {
    'roberta': (RobertaConfig, NERRoBERTa, AutoTokenizer),
    'bert': (BertConfig, NERBERT, AutoTokenizer),
}

# 模型路径
# MODEL_PATH_MAP = {
#     'bert': 'bert-base-chinese',
# }
# 模型路径
MODEL_PATH_MAP = {
    # 'bert': 'hfl/chinese-bert-wwm-ext',
    # 'roberta': '/home/zhangxinghua/roberta-classical-chinese-base-char',
    'roberta': './roberta-classical-chinese-large-char',
    # 'roberta': '/home/zhangxinghua/GuJi_NER/BERT-NER/save_model_pseudo'
    'bert': '/home/zhangxinghua/sikuroberta'
}

def get_seq_labels(args):
    """获取序列标签"""
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.seq_label_file), 'r', encoding='utf-8')]

def load_tokenizer(args):
    """加载rokenizer"""
    # 在线下载
    return MODEL_CLASSES[args.model_type][2].from_pretrained(args.model_name_or_path)
    # # 从已下载文件中读取
    # return MODEL_CLASSES[args.model_type][2].from_pretrained('./bert-base-chinese/bert-base-chinese-vocab.txt')

def init_logger():
    """logger初始化"""
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed(args):
    """随机种子设置"""
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if not args.no_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)


def compute_metrics(seq_preds, seq_labels):
    """获得评价结果"""
    assert len(seq_preds) == len(seq_labels)
    results = {}
    seq_result = get_seq_metrics(seq_preds, seq_labels)

    results.update(seq_result)

    return results


def get_seq_metrics(preds, labels):
    """计算评价结果"""
    assert len(preds) == len(labels)
    print(classification_report(labels, preds))
    return {
        "seq_precision": precision_score(labels, preds),
        "seq_recall": recall_score(labels, preds),
        "seq_f1": f1_score(labels, preds)
    }



def read_prediction_text(args):
    """读取预测文本"""
    return [text.strip() for text in open(os.path.join(args.pred_dir, args.pred_input_file), 'r', encoding='utf-8')]


class FGM():
    def __init__(self, model):
        self.model = model
        self.backup = {}

    def attack(self, epsilon=0.5, emb_name='word_embeddings'):
        # emb_name这个参数要换成你模型中embedding的参数名
        for name, param in self.model.named_parameters():
            # print(name)
            if param.requires_grad and emb_name in name:
                self.backup[name] = param.data.clone()
                norm = torch.norm(param.grad)
                if norm != 0:
                    r_at = epsilon * param.grad / norm
                    param.data.add_(r_at)

    def restore(self, emb_name='word_embeddings'):
        # emb_name这个参数要换成你模型中embedding的参数名
        for name, param in self.model.named_parameters():
            if param.requires_grad and emb_name in name:
                assert name in self.backup
                param.data = self.backup[name]
        self.backup = {}
