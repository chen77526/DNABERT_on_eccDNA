#!/bin/bash
#SBATCH --job-name=[name you want to show on squeue]                                      ## Job name
#SBATCH --mem=50gb                                                                        ## Job memory request
#SBATCH --ntasks=1                                                                        ## Run on a single CPU
#SBATCH --output=./logfile/[data type directory]/fine_tune_ecc_[tune number].log          ## Standard output and error log

#### tune number => If fine tune learning rate = 4e-5, file name will be fine_tune_ecc_4e-5.log  

pwd; hostname; date

export KMER=6
export MODEL_PATH=../6-new-12w-0/
export DATA_PATH=./sample_data/ft/[dataset name]/$KMER
export OUTPUT_PATH=./ft/[dataset name]/$KMER

python run_finetune.py --model_type [dnalongcat/dna] --tokenizer_name=dna$KMER --model_name_or_path $MODEL_PATH --task_name dnaprom --do_train --do_eval --data_dir $DATA_PATH --max_seq_length 1024 --per_gpu_eval_batch_size=8 --per_gpu_train_batch_size=4 --learning_rate [a number between 1e-4 ~ 1e-6] --num_train_epochs [<= 6] --output_dir $OUTPUT_PATH --evaluate_during_training --logging_steps [30000/5000/...] --save_steps [60000/7000/...] --warmup_percent 0.1 --hidden_dropout_prob 0.1 --weight_decay 0.001 --n_process 8 --overwrite_output_dir ### --overwrite_cache

date

#### number template : 
#### (1)
#### poolLCT training dataset size = 263125 => total steps = 65781
#### logging_steps 30000 => evaluate the model performance twice on validation dataset
#### (2)
#### poolLCT training dataset size = 30877 => total steps = 7719 * 2 (epochs)
#### logging_steps 5000 => evaluate the model performance 3 times on validation dataset
#### It depends on dataset size

#### learning_rate => often set to 1e-5 to 5e-5, you can try on other learning rate
#### num_train_epochs => the larger dataset, the less training epochs (poolLCT train only "one" epoch & PC-3 train 2 epochs)

#### model_type : (choose one in [])
#### dnalongcat => sequence length longer than 512 (but need to be multiply of 512)
#### dna => sequence length shorter than 512 (any number smaller than 512)

#### task_name :
#### Can change to other tasks. Reference of definition => "DNABERT/src/transformers/data/processors/glue.py"

#### max_seq_length, per_gpu_eval_batch_size, per_gpu_train_batch_size :
#### Set smaller when memory is not enough

#### learning_rate, num_train_epochs, warmup_percent, hidden_dropout_prob, weight_decay :
#### Mainly fine-tune these parameters, especially learning_rate.

#### Add --overwrite_cache to rewrite training and validation cache when your dataset is modified