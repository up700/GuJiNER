#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/zhangxinghua/anaconda3/lib
CUDA_VISIBLE_DEVICES=0 python predict.py --test_output_file submission_test_1.txt --model_dir ./save_model_1
CUDA_VISIBLE_DEVICES=0 python predict.py --test_output_file submission_test_2.txt --model_dir ./save_model_2
CUDA_VISIBLE_DEVICES=0 python predict.py --test_output_file submission_test_3.txt --model_dir ./save_model_3
CUDA_VISIBLE_DEVICES=0 python predict.py --test_output_file submission_test_4.txt --model_dir ./save_model_4
CUDA_VISIBLE_DEVICES=0 python predict.py --test_output_file submission_test_5.txt --model_dir ./save_model_5
CUDA_VISIBLE_DEVICES=0 python predict_know.py --test_output_file submission_test_know.txt --model_dir ./save_model_know
CUDA_VISIBLE_DEVICES=0 python predict_slide.py --test_output_file submission_test_slide.txt --model_dir ./save_model_know_slide
python combine.py

CUDA_VISIBLE_DEVICES=0 python -u main.py --epoch 30 --do_predict --gama 0.001 --beta 0.01 --gpu_id 2 --lr 0.00001 --switch_ratio 0.5 --data_dir ./data/Guwen-large/ --output_dir ./out-large/best_checkpoint_IB4 --model_name_or_path ./roberta-classical-chinese-large-char --batch_size 32 --max_span_len 4
CUDA_VISIBLE_DEVICES=0 python -u main.py --epoch 30 --do_predict --gama 0.001 --beta 0.01 --gpu_id 2 --lr 0.00001 --switch_ratio 0.5 --data_dir ./data/Guwen-large/ --output_dir ./out-large/best_checkpoint_IB10 --model_name_or_path ./roberta-classical-chinese-large-char --batch_size 16 --max_span_len 10
python combine_len.py
# GPUID=$1
# echo "Run on GPU $GPUID"

# # data
# DATASET=$2
# PROJECT_ROOT=$(dirname "$(readlink -f "$0")")
# DATA_ROOT=$PROJECT_ROOT/dataset/

# # model
# TOKENIZER_TYPE=roberta
# STUDENT1_TYPE=roberta
# STUDENT2_TYPE=distilroberta
# TOKENIZER_NAME=/data/zhangxinghua/roberta-base
# STUDENT1_MODEL_NAME=/data/zhangxinghua/roberta-base
# STUDENT2_MODEL_NAME=/data/zhangxinghua/distilroberta-base

# # self-collaborative learning parameters
# LR=1e-5 
# WARMUP=200 # Sche. Warmup
# BEGIN_EPOCH=1 # Pre. Epoch
# PERIOD=6000 # Update Cycle (iterations)
# MEAN_ALPHA=0.995 # EMA α
# THRESHOLD=0.9 # Confidence Threshold δ
# TRAIN_BATCH=16 # 
# EPOCH=50
# LABEL_MODE=soft # Twitter hard


# WEIGHT_DECAY=1e-4
# SEED=0
# ADAM_EPS=1e-8
# ADAM_BETA1=0.9
# ADAM_BETA2=0.98

# EVAL_BATCH=32


# # output
# OUTPUT=$PROJECT_ROOT/ptms/$DATASET/

# CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES=$GPUID python3 -u run_script.py --data_dir $DATA_ROOT \
#   --student1_model_name_or_path $STUDENT1_MODEL_NAME \
#   --student2_model_name_or_path $STUDENT2_MODEL_NAME \
#   --output_dir $OUTPUT \
#   --tokenizer_name $TOKENIZER_NAME \
#   --cache_dir $PROJECT_ROOT/cached_models \
#   --max_seq_length 128 \
#   --learning_rate $LR \
#   --weight_decay $WEIGHT_DECAY \
#   --adam_epsilon $ADAM_EPS \
#   --adam_beta1 $ADAM_BETA1 \
#   --adam_beta2 $ADAM_BETA2 \
#   --max_grad_norm 1.0 \
#   --num_train_epochs $EPOCH \
#   --warmup_steps $WARMUP \
#   --per_gpu_train_batch_size $TRAIN_BATCH \
#   --per_gpu_eval_batch_size $EVAL_BATCH \
#   --gradient_accumulation_steps 1 \
#   --logging_steps 100 \
#   --save_steps 100000 \
#   --evaluate_during_training \
#   --seed $SEED \
#   --overwrite_output_dir \
#   --mean_alpha $MEAN_ALPHA \
#   --self_learning_label_mode $LABEL_MODE \
#   --self_learning_period $PERIOD \
#   --model_type $TOKENIZER_TYPE \
#   --begin_epoch $BEGIN_EPOCH \
#   --do_train \
#   --dataset $DATASET \
#   --threshold $THRESHOLD \

