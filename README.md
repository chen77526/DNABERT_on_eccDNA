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

Please place dev.tsv & train.tsv into "DNABERT/example/sample_data/ft/eccdna_PC-3_limit1000/6/"

### *Implement only prediction step from PC-3 fine-tuned model*
[PC-3 sample model](https://drive.google.com/drive/folders/1hi_nr4_9CbKblrrrrSyL-o5RcpmtF8YI?usp=sharing)

If you want to predict directly, please place pytorch_model.bin into "DNABERT/example/ft/eccdna_PC-3_limit1000/6/".

---
## Quick start

### Implement from pre-processing step (you can skip previous steps if you download file directly from our google drive)

### *pre-processing*
```
chmod u+x ./eccdna/limit_gen.sh

./eccdna/limit_gen.sh -d human -c PC-3_circleseq_eccdna_filt_uniq -t PC-3 -b hg38_noalt.fa.genome -r hg38_noalt.fa -g hg38_noalt_gap.bed
```

### *fine-tune*
```
export KMER=6
export MODEL_PATH=../6-new-12w-0/
export DATA_PATH=./sample_data/ft/eccdna_PC-3_limit1000/$KMER
export OUTPUT_PATH=./ft/eccdna_PC-3_limit1000/$KMER

python3 run_finetune.py \
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
```

### *prediction*
```
export KMER=6
export MODEL_PATH=./ft/eccdna_PC-3_limit1000/$KMER
export DATA_PATH=./sample_data/ft/eccdna_PC-3_limit1000/$KMER
export PREDICTION_PATH=./result/eccdna_PC-3_limit1000/$KMER

python3 run_finetune.py \
    --model_type dnalongcat \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
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
## Advance usage

### *pre-processing*
```
Usage: Preprocess-DNABERT [OPTIONS] [-d <db_dir>] [-c <eccdna_bed>] [-t <datatype>] [-b <geno_bound>] [-r <geno_ref>] [-g <geno_gap>]
    -d, --db_dir      db directory name
    -c, --eccdna_bed  reference eccdna bed file
    -t, --datatype    species name / cell line name
    -b, --geno_bound  reference genome boundary name
    -r, --geno_ref    reference genome name
    -g, --geno_gap    reference genome gap name

  Options:
    -e, --ext         number of bp extended from eccdna center, Default=512
    -s, --seq_len     sequence length, Default=1024
    -l, --limit       limit sequence length, Default=1000
    -h, --help        show this help messages

  Output: tsv file with binary label ( seq_len-5+1 columns ):
  0 - seq_len-5 : DNA sequences in 6-mer format
  -1            : 0 or 1, 1 represent that this sequence contains eccdna
```

### *fine-tune and prediction*

### refer to [DNABERT github](https://github.com/jerryji1993/DNABERT)
---
## *./eccDNA/*
#### EccDNA data pre-processing about DNABERT ([README](https://github.com/chen77526/DNABERT_on_eccDNA/blob/dev/eccdna/README.md))

## *./examples/result_transform.py*
For visualizing output of DNABERT. Transfer output token ID back to DNA sequence and show its type in confusion matrix

output file path : ./examples/tsv_result/

argument:
--data  : dataset name
--len   : sequence length
```
python3 ./examples/result_transform.py --data PC-3 --len 1024
```

## *./examples/seq_match.py*
Combine the prediction results of both models, sequence index, and comparison result of two models into a tsv file

output file path : ./examples/location/

argument:
--modelType     : training model type
--testSetType   : testing data set type
--ref           : reference sequence file name (positive data set)
--len           : sequence length
--sel           : self-testing or not

```
python3 ./examples/seq_match.py --modelType PC-3 --testSetType PC-3 --ref human_PC-3_positive_1024_limit.fa.out --len 1024 -sel True
```

# DNABERT
This repository includes the implementation of 'DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome'. Please cite our paper if you use the models or codes. The repo is still actively under development, so please kindly report if there is any issue encountered.

 In this package, we provides resources including: source codes of the DNABERT model, usage examples, pre-trained models, fine-tuned models and visulization tool. This package is still under development, as more features will be included gradually. Training of DNABERT consists of general-purposed pre-training and task-specific fine-tuning. As a contribution of our project, we released the pre-trained models in this repository. We extended codes from [huggingface](https://github.com/huggingface/transformers) and adapted them to the DNA scenario.

## Citation
If you have used DNABERT in your research, please kindly cite the following publication:

Yanrong Ji, Zhihan Zhou, Han Liu, Ramana V Davuluri, DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome, Bioinformatics, 2021;, btab083, https://doi.org/10.1093/bioinformatics/btab083


## 1. Environment setup

We recommend you to build a python virtual environment with [Anaconda](https://docs.anaconda.com/anaconda/install/linux/). Also, please make sure you have at least one NVIDIA GPU with Linux x86_64 Driver Version >= 410.48 (compatible with CUDA 10.0). We applied distributed training on 8 NVIDIA GeForce RTX 2080 Ti with 11 GB graphic memory, and the batch size corresponds to it. If you use GPU with other specifications and memory sizes, consider adjusting your batch size accordingly.

#### 1.1 Create and activate a new virtual environment

```
conda create -n dnabert python=3.6
conda activate dnabert
```



#### 1.2 Install the package and other requirements

(Required)

```
conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

git clone https://github.com/jerryji1993/DNABERT
cd DNABERT
python3 -m pip install --editable .
cd examples
python3 -m pip install -r requirements.txt
```



(Optional, install apex for fp16 training)

change to a desired directory by `cd PATH_NAME`

```
git clone https://github.com/NVIDIA/apex
cd apex
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```





## 2. Pre-train (Skip this section if you fine-tune on pre-trained models)

#### 2.1 Data processing

Please see the template data at `/example/sample_data/pre`. If you are trying to pre-train DNABERT with your own data, please process you data into the same format as it. Note that the sequences are in kmer format, so you will need to convert your sequences into that. We also provide a custom function `seq2kmer`in `motif/motif_utils.py` for this conversion.



In the following example, we use DNABERT with kmer=6 as example.



#### 2.2 Model Training

```
cd examples

export KMER=6
export TRAIN_FILE=sample_data/pre/6_3k.txt
export TEST_FILE=sample_data/pre/6_3k.txt
export SOURCE=PATH_TO_DNABERT_REPO
export OUTPUT_PATH=output$KMER

python run_pretrain.py \
    --output_dir $OUTPUT_PATH \
    --model_type=dna \
    --tokenizer_name=dna$KMER \
    --config_name=$SOURCE/src/transformers/dnabert-config/bert-config-$KMER/config.json \
    --do_train \
    --train_data_file=$TRAIN_FILE \
    --do_eval \
    --eval_data_file=$TEST_FILE \
    --mlm \
    --gradient_accumulation_steps 25 \
    --per_gpu_train_batch_size 10 \
    --per_gpu_eval_batch_size 6 \
    --save_steps 500 \
    --save_total_limit 20 \
    --max_steps 200000 \
    --evaluate_during_training \
    --logging_steps 500 \
    --line_by_line \
    --learning_rate 4e-4 \
    --block_size 512 \
    --adam_epsilon 1e-6 \
    --weight_decay 0.01 \
    --beta1 0.9 \
    --beta2 0.98 \
    --mlm_probability 0.025 \
    --warmup_steps 10000 \
    --overwrite_output_dir \
    --n_process 24
```

Add --fp16 tag if you want to perfrom mixed precision. (You have to install the 'apex' from source first).





## 3. Fine-tune (Skip this section if you use fine-tuned model)

#### 3.1 Data processing

Please see the template data at `/example/sample_data/ft/`. If you are trying to fine-tune DNABERT with your own data, please process you data into the same format as it. Note that the sequences are in kmer format, so you will need to convert your sequences into that. We also provide a custom function `seq2kmer`in `motif/motif_utils.py` for this conversion.



#### 3.2 Download pre-trained DNABERT

[DNABERT3](https://drive.google.com/file/d/1nVBaIoiJpnwQxiz4dSq6Sv9kBKfXhZuM/view?usp=sharing)

[DNABERT4](https://drive.google.com/file/d/1V7CChcC6KgdJ7Gwdyn73OS6dZR_J-Lrs/view?usp=sharing)

[DNABERT5](https://drive.google.com/file/d/1KMqgXYCzrrYD1qxdyNWnmUYPtrhQqRBM/view?usp=sharing)

[DNABERT6](https://drive.google.com/file/d/1BJjqb5Dl2lNMg2warsFQ0-Xvn1xxfFXC/view?usp=sharing)

Download the pre-trained model in to a directory. (If you would like to replicate the following examples, please download DNABERT 6). Then unzip the package by running:

```
unzip 6-new-12w-0.zip
```

We also provide a model with `KMER=6` that is fine-tuned on the sample dataset for prediction/visulization/motif_analysis. If you use the fine-tuned model instead of fine-tuning a model by your self, please download the fine-tuned and put it under `examples/ft/6`. 

[Fine-tuned Model](https://drive.google.com/drive/folders/15wFcukTv3ecPw9_25dcOv-bZmj-8d_-6?usp=sharing)


#### 3.3 Fine-tune with pre-trained model

In the following example,  we use DNABERT with kmer=6 as example. We use `prom-core`, a 2-class classification task as example.

```
cd examples

export KMER=6
export MODEL_PATH=PATH_TO_THE_PRETRAINED_MODEL
export DATA_PATH=sample_data/ft/$KMER
export OUTPUT_PATH=./ft/$KMER

python run_finetune.py \
    --model_type dna \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_train \
    --do_eval \
    --data_dir $DATA_PATH \
    --max_seq_length 100 \
    --per_gpu_eval_batch_size=32   \
    --per_gpu_train_batch_size=32   \
    --learning_rate 2e-4 \
    --num_train_epochs 5.0 \
    --output_dir $OUTPUT_PATH \
    --evaluate_during_training \
    --logging_steps 100 \
    --save_steps 4000 \
    --warmup_percent 0.1 \
    --hidden_dropout_prob 0.1 \
    --overwrite_output \
    --weight_decay 0.01 \
    --n_process 8
```

Add --fp16 tag if you want to perfrom mixed precision. (You have to install the 'apex' from source first).

We also provide a model with `KMER=6` that is fine-tuned on the sample dataset for prediction/visulization/motif_analysis. If you use the fine-tuned model instead of fine-tuning a model by your self, please download the fine-tuned and put it under `examples/ft/6`. 

[Fine-tuned Model](https://drive.google.com/drive/folders/15wFcukTv3ecPw9_25dcOv-bZmj-8d_-6?usp=sharing)



## 4. Prediction

After the model is fine-tuned, we can get predictions by running

```$
export KMER=6
export MODEL_PATH=./ft/$KMER
export DATA_PATH=sample_data/ft/$KMER
export PREDICTION_PATH=./result/$KMER

python run_finetune.py \
    --model_type dna \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_predict \
    --data_dir $DATA_PATH  \
    --max_seq_length 75 \
    --per_gpu_pred_batch_size=128   \
    --output_dir $MODEL_PATH \
    --predict_dir $PREDICTION_PATH \
    --n_process 48
```

With the above command, the fine-tuned DNABERT model will be loaded from `MODEL_PATH` , and makes prediction on the `dev.tsv` file that saved in `DATA_PATH` and save the prediction result at `PREDICTION_PATH`.


Add --fp16 tag if you want to perfrom mixed precision. (You have to install the 'apex' from source first).


## 5. Visualization

Visualiazation of DNABERT consists of 2 steps. Calcualate attention scores and Plot.

#### 5.1 Calculate attention scores

calculate with only one model (For example, DNABERT6)

```
export KMER=6
export MODEL_PATH=./ft/$KMER
export DATA_PATH=sample_data/ft/$KMER
export PREDICTION_PATH=./result/$KMER

python run_finetune.py \
    --model_type dna \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_visualize \
    --visualize_data_dir $DATA_PATH \
    --visualize_models $KMER \
    --data_dir $DATA_PATH \
    --max_seq_length 81 \
    --per_gpu_pred_batch_size=16   \
    --output_dir $MODEL_PATH \
    --predict_dir $PREDICTION_PATH \
    --n_process 96
```

With the above command, the fine-tuned DNABERT model will be loaded from `MODEL_PATH` , and calculates attention scores on the `dev.tsv` file that saved in `DATA_PATH` and save the result at `PREDICTION_PATH`.

Add --fp16 tag if you want to perfrom mixed precision. (You have to install the 'apex' from source first).

####5.2 Plotting tool

## 6. Motif analysis

Once the attention scores are generated, we can proceed further to perform motif analysis using `motif/find_motifs.py`:

```
cd ../motif

export KMER=6
export DATA_PATH=../examples/sample_data/ft/$KMER
export PREDICTION_PATH=../examples/result/$KMER
export MOTIF_PATH=./result/$KMER

python find_motifs.py \
    --data_dir $DATA_PATH \
    --predict_dir $PREDICTION_PATH \
    --window_size 24 \
    --min_len 5 \
    --pval_cutoff 0.005 \
    --min_n_motif 3 \
    --align_all_ties \
    --save_file_dir $MOTIF_PATH \
    --verbose
```

The script will generate a .txt file and a weblogo .png file for each motif under `MOTIF_PATH`.

## 7. Genomic variants analysis

To perform genomic variants analysis (e.g. SNPs), we need to first ensure the predictions for the sequences were generated. Then, create a file (template in `SNP/example_mut_file.txt`) specifying for which sequences in `dev.tsv` and start and end indices where we need to perform the mutation. The first column indicates the index of sequence in `dev.tsv` to be mutated. Second and third columns are the start and end indices while the fourth column is the target of mutation (can be substitution, insertion, deletion, etc.)

Once such a file is created, we can perform mutation on the sequences:

```
cd ../SNP
python mutate_seqs.py ./../examples/sample_data/ft/6/dev.tsv ./examples/ --mut_file ./example_mut_file.txt --k 6
```
Alternatively, we can choose to leave the `--mut_file` argument blank, where the program would try to perform substitution of all bases to the four possible nucleotides ('A', 'T', 'C', or 'G') for all sequences. This would be useful for plotting a mutation heatmap as included in the paper. **Note that this would be slow if the `dev.tsv` contains a lot of sequences or the input sequences are very long, as the command would try to perform mutation on all possible locations of them**.

```
cd ../SNP
python mutate_seqs.py ./../examples/sample_data/ft/6/dev.tsv ./examples/ --k 6
```

After that, we can again predict on the generated sequences. **Note: if you have insertion/deletions in your `mut_file.txt`, consider changing the `max_seq_length` we use when making predictions.**

```
export KMER=6
export MODEL_PATH=../examples/ft/$KMER
export DATA_PATH=examples
export PREDICTION_PATH=examples

python ../examples/run_finetune.py \
    --model_type dna \
    --tokenizer_name=dna$KMER \
    --model_name_or_path $MODEL_PATH \
    --task_name dnaprom \
    --do_predict \
    --data_dir $DATA_PATH  \
    --max_seq_length 75 \
    --per_gpu_pred_batch_size=128   \
    --output_dir $MODEL_PATH \
    --predict_dir $PREDICTION_PATH \
    --n_process 48
```

This will again create `pred_results.npy` file under the `$PREDICTION_PATH`. Once we have all the above, we can compute the effect of these mutations by:

```
python SNP.py \
    --orig_seq_file ../examples/sample_data/ft/6/dev.tsv \
    --orig_pred_file ../examples/result/6/pred_results.npy \
    --mut_seq_file examples/dev.tsv \
    --mut_pred_file examples/pred_results.npy \
    --save_file_dir examples
```

This would save a `mutations.tsv` file under `save_file_dir`, that contains index of original sequence (in original `dev.tsv`), original sequence and predictions, mutated sequence and predictions, as well as the difference score and log odds ratio of the change in every case.


## Q&A

#### 1. I cannot start training the model/I have installation issues for the dependencies.

Please kindly make sure that you satisfied all system requirements for DNABERT, and that you have a conda environment properly set up. We have recently successfully tested our pipeline on Amazon EC2 Deep Learning AMI (Ubuntu 18.04). As an option, you could compare your system/environment setup with this AMI.

#### 2. Can DNABERT run on sequences longer than 512?

#### 3. Can DNABERT be extended to multi-class classification?
