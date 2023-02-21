#!/bin/bash

set -e

showHelp() {
  message=$(cat <<- 'EOF'
	Preprocess the eccdna .bed file to input .tsv file into DNABERT

  Usage: Preprocess-DNABERT [OPTIONS] [-d <db_dir>] [-t <datatype>]
    -d, --db_dir      db directory name
    -t, --datatype    species name / cell line name
  
  Options:
    -s, --seq_len     sequence length, Default=1024
    -l, --limit       sequence length limit, Default=1000
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
    -s|--seq_len)     seq_len="$2";shift;shift;;
    -d|--db_dir)      db_dir="$2";shift;shift;;
    -l|--limit)       limit="$2";shift;shift;;
    -t|--datatype)    datatype="$2";shift;shift;;
    -h|--help)        showHelp;shift;shift;;
    *)                showHelp "Unknown parameter passed: $1";shift;shift;;
  esac; done

  # check / defaults
  if [[ -z $seq_len ]]; then seq_len=1024; fi
  if [[ -z $db_dir ]]; then db_dir=human; fi
  if [[ -z $limit ]]; then limit=1000; fi
  if [[ -z $datatype ]]; then showHelp "species name / cell line name (-t) not given."; fi
}

parseArgs "$@"

export eccdna_dir=eccdna_${datatype}_limit${limit}                      # eccdna directory name
#Change directory to where the script is
cd "${0%/*}"

python label_generate.py --length $seq_len --data $db_dir --cellline $datatype
echo "Finish generating 6-mers"
### (very important)Need to rename old label_${seq_len}_dev.tsv & label_${seq_len}.tsv & train.tsv & dev.tsv
cd output/$db_dir/
shuf -o dev.tsv < label_${seq_len}_dev.tsv
shuf -o train.tsv < label_${seq_len}.tsv

### Create directory for this dataset
cd ../../../examples/sample_data/ft/
if  [ ! -d "$eccdna_dir" ]; then mkdir $eccdna_dir; fi
cd $eccdna_dir/
if [ ! -d "./6/" ]; then mkdir "./6"; fi
cd 6/
cp ../../../../../eccdna/output/$db_dir/train.tsv ./
cp ../../../../../eccdna/output/$db_dir/dev.tsv ./

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
echo "Finish generating train.tsv and dev.tsv"