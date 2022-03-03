# plot.py
## Quick start

1. Save ```.log``` from DNABERT output.
2. ```cd ./[your_dataset_type]/[tuning_parameter]/```
3. ```grep '[acc/auc/loss] = ' [your_logfile_name] > ecc_[acc/auc/loss]_[number_you_tune].log```, which acc, auc, and loss you can choose to generate the plot.
4. Then type below command line:

```
python plot.py --input ./PC-3_comparison/lr/ --data acc

arguments:
    --input         input logfile directory, string before '_' needs to be dataset name
    --data          type of plot -> acc / auc / loss
```