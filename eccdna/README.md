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

## *_gen.sh
Shell scripts for pre-processing a new dataset and put the dataset into "../examples/sample_data"

## label_generate*.py
generate train.tsv & dev.tsv for each dataset which matches input type of DNABERT