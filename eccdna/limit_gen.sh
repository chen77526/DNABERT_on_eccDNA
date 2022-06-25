#!/bin/bash

set -e

showHelp() {
  message=$(cat <<- 'EOF'
	Preprocess the eccdna .bed file to input .tsv file into DNABERT

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
	EOF
	)
  if [[ -n $1 ]]; then
    echo -e "*** ERROR: $1 ***\n\n$message" >&2
    exit 1
  else
    echo "$message"
    exit 0
  fi
}

parseArgs() {
  while [[ "$#" > 0 ]]; do
  case $1 in
    -e|--ext)         ext="$2";shift;shift;;
    -s|--seq_len)     seq_len="$2";shift;shift;;
    -l|--limit)       limit="$2";shift;shift;;
    -d|--db_dir)      db_dir="$2";shift;shift;;
    -c|--eccdna_bed)  eccdna_bed="$2";shift;shift;;
    -t|--datatype)    datatype="$2";shift;shift;;
    -b|--geno_bound)  geno_bound="$2";shift;shift;;
    -r|--geno_ref)    geno_ref="$2";shift;shift;;
    -g|--geno_gap)    geno_gap="$2";shift;shift;;
    -h|--help)        showHelp;shift;shift;;
    *)                showHelp "Unknown parameter passed: $1";shift;shift;;
  esac; done

  # check / defaults
  if [[ -z $ext ]]; then ext=512; fi
  if [[ -z $seq_len ]]; then seq_len=1024; fi
  if [[ -z $limit ]]; then limit=1000; fi
  if [[ -z $db_dir ]]; then showHelp "db directory name (-d) not given."; fi
  if [[ -z $eccdna_bed ]]; then showHelp "reference eccdna bed file (-c) not given."; fi
  if [[ -z $datatype ]]; then showHelp "species name / cell line name (-t) not given."; fi
  if [[ -z $geno_bound ]]; then showHelp "reference genome boundary name (-b) not given."; fi
  if [[ -z $geno_ref ]]; then showHelp "reference genome name (-r) not given."; fi
  if [[ -z $geno_gap ]]; then showHelp "reference genome gap name (-g) not given."; fi
}

parseArgs "$@"

export eccdna_dir=eccdna_${datatype}_limit${limit}                      # eccdna directory name

### Acoording to sequence length contraint, check original .bed files and produce corresponding positive label .bed file
### and sequence need to removed in order to generate a negative label .bed file
python bed_limit.py --extend $ext --datatype $datatype --limit $limit --boundary ./genome/$db_dir/$geno_bound --gap ./genome/$db_dir/$geno_gap --eccdna ./db/$db_dir/$eccdna_bed --output ./db/$db_dir/

### Generate negative label .bed file
bedtools shuffle -i ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_seq_${seq_len}_${limit}.bed -g ./genome/$db_dir/$geno_bound -excl ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_excl_${seq_len}_${limit}.bed > ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_comp_${seq_len}_${limit}.bed

### Check if negative label .bed is intersect with positive label .bed
bedtools intersect -a ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_comp_${seq_len}_${limit}.bed -b ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_excl_${seq_len}_${limit}.bed

### Acquire its corresponding FASTA file
bedtools getfasta -fi ./genome/$db_dir/$geno_ref -bed ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_seq_${seq_len}_${limit}.bed -fo ./output/$db_dir/${datatype}_positive_${seq_len}_limit.fa.out
bedtools getfasta -fi ./genome/$db_dir/$geno_ref -bed ./db/$db_dir/${datatype}_circleseq_eccdna_filt_uniq_comp_${seq_len}_${limit}.bed -fo ./output/$db_dir/${datatype}_negative_${seq_len}_limit.fa.out

### Cut FASTA format into 6-mers and append its label to every sequence
python label_generate.py --length $seq_len --data $db_dir --cellline $datatype

### (very important)Need to rename old label_${seq_len}_dev.tsv & label_${seq_len}.tsv & train.tsv & dev.tsv
cd output/$db_dir/
shuf -o dev.tsv < label_${seq_len}_dev.tsv
shuf -o train.tsv < label_${seq_len}.tsv

### Create directory for this dataset
cd ../../../examples/sample_data/ft/
mkdir $eccdna_dir
cd $eccdna_dir/
mkdir 6
cd 6/
cp ../../../eccdna/output/$db_dir/train.tsv ./
cp ../../../eccdna/output/$db_dir/dev.tsv ./

### Add header line to these .tsv files
cat ../../template.txt ./dev.tsv > ./dev2.tsv
cat ../../template.txt ./train.tsv > ./train2.tsv
rm dev.tsv
rm train.tsv
mv dev2.tsv dev.tsv
mv train2.tsv train.tsv

### Remove sequence which contains "N"(unknown nucleotide)
sed -i '/N/d' train.tsv
sed -i '/N/d' dev.tsv