## Citation
Yanrong Ji, Zhihan Zhou, Han Liu, Ramana V Davuluri, DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome, Bioinformatics, 2021;, btab083, https://doi.org/10.1093/bioinformatics/btab083

[reference github](https://github.com/jerryji1993/DNABERT)

## DNABERT/
DNABERT model
##### *result_transform.py* (code I added)
For visualizing output of DNABERT. Transfer output token ID back to DNA sequence and show its type in confusion matrix

output file path : ./tsv_result/

argument : --data -> dataset name

## eccDNA/
EccDNA data pre-processing about DNABERT

## Download pre-trained DNABERT
##### (Refer to https://github.com/jerryji1993/DNABERT) 
##### (I place this model at ./DNABERT/)

[DNABERT3](https://drive.google.com/file/d/1nVBaIoiJpnwQxiz4dSq6Sv9kBKfXhZuM/view?usp=sharing)

[DNABERT4](https://drive.google.com/file/d/1V7CChcC6KgdJ7Gwdyn73OS6dZR_J-Lrs/view?usp=sharing)

[DNABERT5](https://drive.google.com/file/d/1KMqgXYCzrrYD1qxdyNWnmUYPtrhQqRBM/view?usp=sharing)

[DNABERT6](https://drive.google.com/file/d/1BJjqb5Dl2lNMg2warsFQ0-Xvn1xxfFXC/view?usp=sharing)

Download the pre-trained model in to a directory. (If you would like to replicate the following examples, please download DNABERT 6). Then unzip the package by running:

```
unzip 6-new-12w-0.zip
```

They also provide a model with `KMER=6` that is fine-tuned on the sample dataset for prediction/visulization/motif_analysis. If you use the fine-tuned model instead of fine-tuning a model by your self, please download the fine-tuned and put it under `examples/ft/6`. 

[Fine-tuned Model](https://drive.google.com/drive/folders/15wFcukTv3ecPw9_25dcOv-bZmj-8d_-6?usp=sharing)

## Download DNABERT eccDNA example

[PC-3 sample dataset](https://drive.google.com/drive/folders/1hi_nr4_9CbKblrrrrSyL-o5RcpmtF8YI?usp=sharing)

Please place these 2 files into "DNABERT/example/sample_data/ft/eccdna_PC-3_comparison/6/"