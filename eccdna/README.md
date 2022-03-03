## bed_limit.py
Filter eccDNA sequence length(< 1000 neucleotides)

```
python bed_limit.py \
    --extend 512 \
    --limit 1000 \
    --species mouse \
    --boundary ./genome/mouse/mouse.genome \
    --gap ./genome/mouse/exclude.sorted.bed \
    --eccdna ./db/mouse/mouse_circleseq_eccdna_filt_uniq.bed \
    --output ./db/mouse/

arguments:
    --extend            sequence length you want to extend from center
    --limit             sequence limit
    --species           species name of eccdna
    --boundary          genome boundary file path
    --gap               gap bedfile of whole genome path
    --eccdna            eccdna bedfile path
    --output            output bedfile path
```

## limit_gen.sh
Shell script for pre-processing a new dataset and put the dataset into "../examples/sample_data"
> Arrange your data as below to use this shell script

    .
    |-- db
    |   |-- species name (e.g., mouse, human)
    |   |   |-- eccdna .bed
    |   |   |-- eccdna seq .bed (after selecting sequence shorter than limit)
    |   |   |-- eccdna excl .bed (sequence need to exclude when generate non-eccdna sequence .bed)
    |   |   |__ eccdna comp .bed (non-eccdna sequence)
    |   |__ ...
    |-- genome
    |   |-- species name (e.g., mouse, human)
    |   |   |-- whole genome
    |   |   |-- genome boudary file
    |   |   |__ whole genome gap file
    |   |__ ...
    |-- output
    |   |-- species name (e.g., mouse, human)
    |   |   |-- positive.fa.out (positive label dna sequence)
    |   |   |-- negative.fa.out (negative label dna sequence)
    |   |   |-- label_[seq_length].tsv (training dataset)
    |   |   |-- label_[seq_length]_dev.tsv (testing dataset)
    |   |   |-- train.tsv (shuffling training dataset)
    |   |   |__ dev.tsv (shuffling testing dataset)
    |   |__ ...
    |__ ...

## label_generate.py
generate train.tsv & dev.tsv for each dataset which matches input type of DNABERT

```
python label_generate.py --length 1024 --data mouse

arguments:
    --length            sequence length
    --data              species name of eccdna
```