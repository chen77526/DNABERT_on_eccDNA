#!/bin/bash  

export data=./PC-3_comparison/lr          ### data path

for FILE in $data/fine_tune_ecc_*.log; do
    echo $FILE | awk '{split($0, a, "/");split(a[4], b, "_");split(b[4], c, ".");print c[1]}'
done > log_gen.log

awk 'ORS=" " {print}' log_gen.log > oneline.log

export parameter=$(cat oneline.log)
for p in $parameter; do
    grep 'acc = ' $data/fine_tune_ecc_$p.log > $data/ecc_acc_$p.log
    grep 'auc = ' $data/fine_tune_ecc_$p.log > $data/ecc_auc_$p.log
    grep '   loss = ' $data/fine_tune_ecc_$p.log > $data/ecc_loss_$p.log
done

python plot.py --input $data/ --data acc
python plot.py --input $data/ --data auc
python plot.py --input $data/ --data loss