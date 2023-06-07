import torch.nn as nn
from transformers import BertPreTrainedModel, BertModel, RobertaModel
from torchcrf import CRF


class SeqClassifier(nn.Module):
    """序列标注分类器"""
    def __init__(self, input_dim, num_seq_labels, dropout_rate=0.):
        super(SeqClassifier, self).__init__()
        self.dropout = nn.Dropout(dropout_rate)
        self.linear = nn.Linear(input_dim, num_seq_labels)

    def forward(self, x):
        x = self.dropout(x)
        return self.linear(x)

class NERRoBERTa(BertPreTrainedModel):
    """NERBERT模型"""
    # config_class = BertConfig
    # pretrained_model_archive_map = BERT_PRETRAINED_MODEL_ARCHIVE_MAP
    # base_model_prefix = "bert"

    def __init__(self, config, args, seq_label_lst):
        super(NERRoBERTa, self).__init__(config)
        self.args = args
        self.num_seq_labels = len(seq_label_lst)
        self.roberta = RobertaModel(config=config)

        ############

        # self.dropout = nn.Dropout(p=0.2)
        # self.high_dropout = nn.Dropout(p=0.5)
        # num_hidden_layers = 24
        # # 24
        # n_weights = num_hidden_layers + 1
        # weights_init = torch.zeros(n_weights).float()
        # weights_init.data[:-1] = -3
        # self.layer_weights = torch.nn.Parameter(weights_init)

        ##############



        self.seq_classifier = SeqClassifier(config.hidden_size, self.num_seq_labels, args.dropout_rate)

        if args.use_crf:
            self.crf = CRF(num_tags=self.num_seq_labels, batch_first=True)

    def forward(self, input_ids, attention_mask, token_type_ids, seq_labels_ids):
        """前向传播"""
        # sequence_output, pooled_output, (hidden_states), (attentions)
        outputs = self.roberta(input_ids, attention_mask=attention_mask,
                            token_type_ids=token_type_ids, output_hidden_states=True)
        # print(outputs)
        ######################################
        # hidden_layers = outputs['hidden_states']
        # # Layer, B, L, D
        
        # sequence_output = torch.stack(
        #     [self.dropout(layer) for layer in hidden_layers], dim=3
        # )
        # # print(sequence_output.size())
        # cls_output = (torch.softmax(self.layer_weights, dim=0) * sequence_output).sum(-1)

        # logits = torch.stack(
        #     [self.seq_classifier(self.high_dropout(cls_output)) for _ in range(5)],
        #     dim=0,
        # )
        # # print(logits.size())

        # seq_logits = torch.mean(logits, dim=0)
        # # print(seq_logits.size())
        # # exit()

        ######################################
        sequence_output = outputs[0]

        seq_logits = self.seq_classifier(sequence_output)

        total_loss = 0

        if seq_labels_ids is not None:
            if self.args.use_crf:
                seq_loss = self.crf(seq_logits, seq_labels_ids, mask=attention_mask.byte(), reduction='mean')
                seq_loss = -1 * seq_loss  # negative log-likelihood
            else:
                seq_loss_fct = nn.CrossEntropyLoss(ignore_index=self.args.ignore_index, size_average=False)
                # pad部分不计算loss
                if attention_mask is not None:
                    active_loss = attention_mask.view(-1) == 1
                    active_logits = seq_logits.view(-1, self.num_seq_labels)[active_loss]
                    active_labels = seq_labels_ids.view(-1)[active_loss]
                    seq_loss = seq_loss_fct(active_logits, active_labels)
                    loss_weight = (active_labels <= 2).float()+0.5
                    seq_loss = (loss_weight*seq_loss).mean()
                else:
                    seq_loss = seq_loss_fct(seq_logits.view(-1, self.num_seq_labels), seq_labels_ids.view(-1))
                    loss_weight = (seq_labels_ids.view(-1) <= 2).float()+0.5
                    seq_loss = (loss_weight*seq_loss).mean()
            total_loss += self.args.seq_loss_coef * seq_loss

        outputs = ((seq_logits),) + outputs[2:]  # add hidden states and attention if they are here

        outputs = (total_loss,) + outputs

        return outputs  # (loss), logits, (hidden_states), (attentions)

class NERBERT(BertPreTrainedModel):
    """NERBERT模型"""
    # config_class = BertConfig
    # pretrained_model_archive_map = BERT_PRETRAINED_MODEL_ARCHIVE_MAP
    # base_model_prefix = "bert"

    def __init__(self, config, args, seq_label_lst):
        super(NERBERT, self).__init__(config)
        self.args = args
        self.num_seq_labels = len(seq_label_lst)
        self.bert = BertModel(config=config)

        self.seq_classifier = SeqClassifier(config.hidden_size, self.num_seq_labels, args.dropout_rate)

        if args.use_crf:
            self.crf = CRF(num_tags=self.num_seq_labels, batch_first=True)

    def forward(self, input_ids, attention_mask, token_type_ids, seq_labels_ids):
        """前向传播"""
        # sequence_output, pooled_output, (hidden_states), (attentions)
        outputs = self.bert(input_ids, attention_mask=attention_mask,
                            token_type_ids=token_type_ids)
        sequence_output = outputs[0]

        seq_logits = self.seq_classifier(sequence_output)

        total_loss = 0

        if seq_labels_ids is not None:
            if self.args.use_crf:
                seq_loss = self.crf(seq_logits, seq_labels_ids, mask=attention_mask.byte(), reduction='mean')
                seq_loss = -1 * seq_loss  # negative log-likelihood
            else:
                seq_loss_fct = nn.CrossEntropyLoss(ignore_index=self.args.ignore_index, size_average=False)
                # pad部分不计算loss
                if attention_mask is not None:
                    active_loss = attention_mask.view(-1) == 1
                    active_logits = seq_logits.view(-1, self.num_seq_labels)[active_loss]
                    active_labels = seq_labels_ids.view(-1)[active_loss]
                    seq_loss = seq_loss_fct(active_logits, active_labels)
                    loss_weight = (active_labels <= 2).float()+0.5
                    seq_loss = (loss_weight*seq_loss).mean()
                else:
                    seq_loss = seq_loss_fct(seq_logits.view(-1, self.num_seq_labels), seq_labels_ids.view(-1))
                    loss_weight = (seq_labels_ids.view(-1) <= 2).float()+0.5
                    seq_loss = (loss_weight*seq_loss).mean()
            total_loss += self.args.seq_loss_coef * seq_loss

        outputs = ((seq_logits),) + outputs[2:]  # add hidden states and attention if they are here

        outputs = (total_loss,) + outputs

        return outputs  # (loss), logits, (hidden_states), (attentions)
