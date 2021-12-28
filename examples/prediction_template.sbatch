#!/bin/bash
#SBATCH --job-name=[name you want to show on squeue]                             ## Job name
#SBATCH --mem=25gb                                                               ## Job memory request
#SBATCH --ntasks=1                                                               ## Run on a single CPU
#SBATCH --output=prediction_[train dataset name]_[test dataset name].log         ## Standard output and error log

pwd; hostname; date

export KMER=6
export MODEL_PATH=./ft/[dataset name]/$KMER
export DATA_PATH=./sample_data/ft/[dataset name]/$KMER
export PREDICTION_PATH=./result/[dataset name]_[testing dataset name]/$KMER

python run_finetune.py --model_type [dnalongcat/dna] --tokenizer_name=dna$KMER --model_name_or_path $MODEL_PATH --task_name dnaprom --do_predict --data_dir $DATA_PATH  --max_seq_length 1024 --per_gpu_pred_batch_size=128 --output_dir $MODEL_PATH --predict_dir $PREDICTION_PATH --n_process 48 --overwrite_cache

date

#### model_type : (choose one in [], must be the same as your model setting)
#### dnalongcat => sequence length longer than 512 (but need to be multiply of 512)
#### dna => sequence length shorter than 512 (any number smaller than 512)

#### task_name : (must be the same as your model setting)
#### Can change to other tasks. Reference of definition => "DNABERT/src/transformers/data/processors/glue.py"