import numpy as np
import pandas as pd
import argparse
import os

def findTPTN(ID):
    focus = pd.read_csv('result_{}_{}.tsv'.format(ID, args.data), header=None, delimiter='\t')
    focus_re = focus.rename(columns={focus.columns[-2]: 'label', focus.columns[-1]: 'preds'})
    conditions = [
        (focus_re['label'] == 1) & (focus_re['preds'] == 1),
        (focus_re['label'] == 0) & (focus_re['preds'] == 1),
        (focus_re['label'] == 0) & (focus_re['preds'] == 0),
        (focus_re['label'] == 1) & (focus_re['preds'] == 0)
    ]
    choices = ['TP', 'FP', 'TN', 'FN']
    focus_re['result'] = np.select(conditions, choices)
    result = pd.Series(focus_re['result'])
    print(result)
    result.to_csv('./tsv_result/{}/{}_{}_result.tsv'.format(args.data, ID, args.data), sep='\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default='C4-2')
    parser.add_argument("--model", type=str, default='C4-2')
    args = parser.parse_args()

    # eccdna_{}all is a folder which contains only dev.tsvd. dev.tsv is a concatenated file of original train.tsv and dev.tsv
    inputTsv = pd.read_csv('./sample_data/ft/eccdna_{}_limit1000/6/dev.tsv'.format(args.data), skiprows=1, header=None, delimiter='\t')
    inputTsv.columns = ['sequence', 'label']
    inputTsv.drop(['label'], inplace=True, axis=1)
    inputTsv['sequence'] = inputTsv['sequence'].str.split(' ')
    inputTsv_seq = pd.DataFrame(inputTsv['sequence'].tolist())
    for col in inputTsv_seq.columns:
        if col == 0: continue
        inputTsv_seq[col] = inputTsv_seq[col].str.slice(start=-1)
    
    inputTsv_seq = pd.Series(inputTsv_seq[inputTsv_seq.columns].values.tolist()).str.join('')
    print(inputTsv_seq)
    
    outdir = './tsv_result/{}'.format(args.data)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
        
    inputTsv_seq.to_csv('{}/{}_seq.tsv'.format(outdir, args.data), sep='\t')

    result = findTPTN(args.model)
