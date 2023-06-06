#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/zhangxinghua/anaconda3/lib

CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_1 --model_dir save_model_1 --model_type roberta --do_train --do_eval --num_train_epochs 100 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 100 --weight_decay 0.001
CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_2 --model_dir save_model_2 --model_type roberta --do_train --do_eval --num_train_epochs 100 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 100 --weight_decay 0.001
CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_3 --model_dir save_model_3 --model_type roberta --do_train --do_eval --num_train_epochs 100 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 100 --weight_decay 0.001
CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_4 --model_dir save_model_4 --model_type roberta --do_train --do_eval --num_train_epochs 100 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 100 --weight_decay 0.001
CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_5 --model_dir save_model_5 --model_type roberta --do_train --do_eval --num_train_epochs 100 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 100 --weight_decay 0.001

CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_know --model_dir save_model_know --model_type roberta --do_train --do_eval --num_train_epochs 30 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 120 --weight_decay 0.001

CUDA_VISIBLE_DEVICES=0 python main_bio.py --task ner_data_know_slide --model_dir save_model_know_slide --model_type roberta --do_train --do_eval --num_train_epochs 30 --warmup_steps 200 --learning_rate 2e-5 --use_crf --train_batch_size 16 --dropout_rate 0.05 --gradient_accumulation_steps 2 --logging_steps 100 --max_seq_len 102 --weight_decay 0.001


CUDA_VISIBLE_DEVICES=0 python -u main_span.py --epoch 30 --do_train --do_eval --gama 0.001 --beta 0.01 --gpu_id 2 --lr 0.00001 --switch_ratio 0.5 --data_dir ./data/Guwen-large/ --output_dir ./out-large/ --model_name_or_path ./roberta-classical-chinese-large-char --batch_size 32 --model_type roberta --max_span_len 4
CUDA_VISIBLE_DEVICES=0 python -u main_span.py --epoch 30 --do_train --do_eval --gama 0.001 --beta 0.01 --gpu_id 2 --lr 0.00001 --switch_ratio 0.5 --data_dir ./data/Guwen-large/ --output_dir ./out-large/ --model_name_or_path ./roberta-classical-chinese-large-char --batch_size 16 --model_type roberta --max_span_len 10
