#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/zhangxinghua/anaconda3/lib
CUDA_VISIBLE_DEVICES=0 python predict/predict.py --test_output_file predict/submission_test_1.txt --model_dir ./save_model_1
CUDA_VISIBLE_DEVICES=0 python predict/predict.py --test_output_file predict/submission_test_2.txt --model_dir ./save_model_2
CUDA_VISIBLE_DEVICES=0 python predict/predict.py --test_output_file predict/submission_test_3.txt --model_dir ./save_model_3
CUDA_VISIBLE_DEVICES=0 python predict/predict.py --test_output_file predict/submission_test_4.txt --model_dir ./save_model_4
CUDA_VISIBLE_DEVICES=0 python predict/predict.py --test_output_file predict/submission_test_5.txt --model_dir ./save_model_5
CUDA_VISIBLE_DEVICES=0 python predict/predict_know.py --test_output_file predict/submission_test_know.txt --model_dir ./save_model_know
CUDA_VISIBLE_DEVICES=0 python predict/predict_slide.py --test_output_file predict/submission_test_slide.txt --model_dir ./save_model_know_slide
python predict/combine.py

CUDA_VISIBLE_DEVICES=0 python -u main_span.py --epoch 30 --do_predict --gama 0.001 --beta 0.01 --gpu_id 2 --lr 0.00001 --switch_ratio 0.5 --data_dir ./data/Guwen-large/ --output_dir ./out-large/best_checkpoint_IB4 --model_name_or_path ./roberta-classical-chinese-large-char --batch_size 32 --max_span_len 4
CUDA_VISIBLE_DEVICES=0 python -u main_span.py --epoch 30 --do_predict --gama 0.001 --beta 0.01 --gpu_id 2 --lr 0.00001 --switch_ratio 0.5 --data_dir ./data/Guwen-large/ --output_dir ./out-large/best_checkpoint_IB10 --model_name_or_path ./roberta-classical-chinese-large-char --batch_size 16 --max_span_len 10
python predict/combine_len.py
