#!/bin/bash

export ext=128                                                          # number of bp extended from center
export seq_len=256                                                      # sequence length
export cellline=LnCap                                                   # name of cellline
export db_dir=cell_lines                                                # db directory name
export species=human                                                    # reference genome directory name
export geno_bound=hg38_noalt.fa.genome                                  # reference genome boundary name
export geno_ref=hg38_noalt.fa                                           # reference genome name
export eccdna_dir=eccdna_${cellline}_pair${seq_len}                     # eccdna directory name

### Acoording to sequence length contraint, check original .bed files and produce corresponding positive label .bed file
### and sequence need to removed in order to generate a negative label .bed file
python bed_human_pair.py --extend $ext --cellline $cellline

### Generate negative label .bed file
bedtools shuffle -bedpe -chrom -i ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_seq_pair_${seq_len}.bed -g ./genome/$species/$geno_bound -excl ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_excl_pair_${seq_len}.bed > ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_comp_pair_tmp_${seq_len}.bed

### split "chr...  start index  end index\tchr... start index  end index" into "chr...  start index  end index\nchr...  start index  end index"
sed 's/\tchr/\nchr/g' ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_comp_pair_tmp_${seq_len}.bed > ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_comp_pair_${seq_len}.bed

### Check if negative label .bed is intersect with positive label .bed
bedtools intersect -a ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_comp_pair_${seq_len}.bed -b ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_excl_pair_${seq_len}.bed

### Acquire its corresponding FASTA file
bedtools getfasta -fi ./genome/$species/$geno_ref -bed ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_seq_${seq_len}.bed -fo ./output/$species/${species}_${cellline}_positive_${seq_len}.fa.out
bedtools getfasta -fi ./genome/$species/$geno_ref -bed ./db/$db_dir/${cellline}_circleseq_eccdna_filt_uniq_comp_pair_${seq_len}.bed -fo ./output/$species/${species}_${cellline}_negative_${seq_len}.fa.out

### Cut FASTA format into 6-mers and append its label to every sequence
python label_generate_pair.py --length $seq_len --data $species --gene $cellline

### (very important)Need to rename old label_${seq_len}_dev.tsv & label_${seq_len}.tsv & train.tsv & dev.tsv
cd output/$species/
shuf -o dev.tsv < label_${seq_len}_dev.tsv
shuf -o train.tsv < label_${seq_len}.tsv

### Create directory for this dataset
cd ../../../DNABERT/examples/sample_data/ft/
mkdir $eccdna_dir
cd $eccdna_dir/
mkdir 6
cd 6/
cp ../../../../../eccdna/output/$species/train.tsv ./
cp ../../../../../eccdna/output/$species/dev.tsv ./

### Add header line to these .tsv files
cat ../../template2.txt ./dev.tsv > ./dev2.tsv
cat ../../template2.txt ./train.tsv > ./train2.tsv
rm dev.tsv
rm train.tsv
mv dev2.tsv dev.tsv
mv train2.tsv train.tsv

### Remove sequence which contains "N"(unknown nucleotide)
sed -i '/N/d' train.tsv
sed -i '/N/d' dev.tsv