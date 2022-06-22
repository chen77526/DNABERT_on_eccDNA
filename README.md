## Citation
Yanrong Ji, Zhihan Zhou, Han Liu, Ramana V Davuluri, DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome, Bioinformatics, 2021;, btab083, https://doi.org/10.1093/bioinformatics/btab083

[reference github](https://github.com/jerryji1993/DNABERT)

---
## Download pre-trained DNABERT
##### (Refer to https://github.com/jerryji1993/DNABERT) 
##### (Place this model at ./DNABERT/)

[DNABERT3](https://drive.google.com/file/d/1nVBaIoiJpnwQxiz4dSq6Sv9kBKfXhZuM/view?usp=sharing)

[DNABERT4](https://drive.google.com/file/d/1V7CChcC6KgdJ7Gwdyn73OS6dZR_J-Lrs/view?usp=sharing)

[DNABERT5](https://drive.google.com/file/d/1KMqgXYCzrrYD1qxdyNWnmUYPtrhQqRBM/view?usp=sharing)

[DNABERT6](https://drive.google.com/file/d/1BJjqb5Dl2lNMg2warsFQ0-Xvn1xxfFXC/view?usp=sharing)

Download the pre-trained model in to a directory. (If you would like to replicate the following examples, please download DNABERT 6). Then unzip the package by running:

```
unzip 6-new-12w-0.zip
```
---
## Download DNABERT eccDNA example

### *Implement from pre-processing step*
Start from [PC-3 sample bedfile](https://github.com/chen77526/DNABERT_on_eccDNA/tree/dev/eccdna/db/cell_lines) and execute ```./eccdna/limit_gen.sh``` to generate pre-processing files for DNABERT

### *Implement from fine-tune step*
[PC-3 sample dataset](https://drive.google.com/drive/folders/1hi_nr4_9CbKblrrrrSyL-o5RcpmtF8YI?usp=sharing)

Please place dev.tsv & train.tsv into "DNABERT/example/sample_data/ft/eccdna_PC-3_comparison/6/"

### *Implement only prediction step from PC-3 fine-tuned model*
[PC-3 sample model](https://drive.google.com/drive/folders/1hi_nr4_9CbKblrrrrSyL-o5RcpmtF8YI?usp=sharing)

If you want to predict directly, please place pytorch_model.bin into "DNABERT/example/ft/eccdna_PC-3_comparison/6/".

---
## Quick start

### Implement from pre-processing step (you can skip previous steps if you download file directly from our google drive)
```
# pre-processing

chmod u+x ./eccdna/limit_gen.sh
./eccdna/limit_gen.sh

# fine-tune

export KMER=6
export MODEL_PATH=../6-new-12w-0/
export DATA_PATH=./sample_data/ft/eccdna_PC-3_comparison/$KMER
export OUTPUT_PATH=./ft/eccdna_PC-3_comparison/$KMER

python run_finetune.py \
    --model_type dnalongcat \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_train \
    --do_eval \
    --data_dir $DATA_PATH \
    --max_seq_length 1024 \
    --per_gpu_eval_batch_size=8 \
    --per_gpu_train_batch_size=4 \
    --learning_rate 4e-5 \ 
    --num_train_epochs 2 \
    --output_dir $OUTPUT_PATH \
    --evaluate_during_training \
    --logging_steps 3000 \
    --save_steps 7000 \
    --warmup_percent 0.1 \
    --hidden_dropout_prob 0.1 \
    --weight_decay 0.001 \
    --n_process 8 \
    --overwrite_output_dir \
    --overwrite_cache

# prediction

export KMER=6
export MODEL_PATH=./ft/eccdna_PC-3_comparison/$KMER
export DATA_PATH=./sample_data/ft/eccdna_PC-3_comparison/$KMER
export PREDICTION_PATH=./result/eccdna_PC-3_comparison/$KMER

python run_finetune.py \
    --model_type dnalongcat \
    --tokenizer_name=dna$KMER \
    -model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_predict \
    --data_dir $DATA_PATH \
    --max_seq_length 1024 \
    --per_gpu_pred_batch_size=128 \
    --output_dir $MODEL_PATH \
    --predict_dir $PREDICTION_PATH \
    --n_process 48 \
    --overwrite_cache \
    --train_type PC-3 \
    --test_type PC-3
```
---
## *./eccDNA/*
#### EccDNA data pre-processing about DNABERT ([README](https://github.com/chen77526/DNABERT_on_eccDNA/blob/dev/eccdna/README.md))

## *./examples/result_transform.py*
For visualizing output of DNABERT. Transfer output token ID back to DNA sequence and show its type in confusion matrix

output file path : ./examples/tsv_result/

argument : --data -> dataset name


