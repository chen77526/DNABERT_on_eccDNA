import os
import argparse
import numpy as np
import pandas as pd

def findTPTN(ID):
    # modified
    focus = pd.read_csv('./result_{}_{}.tsv'.format(ID, args.data), header=None, delimiter='\t')
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
    # modified
    result.to_csv('./tsv_result/{}/{}_{}_result_{}.tsv'.format(args.data, ID, args.data, args.len), sep='\t')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default='C4-2')
    parser.add_argument("--len", type=int, default=1024)
    args = parser.parse_args()

    # modified
    inputTsv = pd.read_csv('./sample_data/ft/6/dev.tsv', skiprows=1, header=None, delimiter='\t')
    inputTsv.columns = ['sequence', 'label']
    inputTsv.drop(['label'], inplace=True, axis=1)
    inputTsv['sequence'] = inputTsv['sequence'].str.split(' ')
    inputTsv_seq = pd.DataFrame(inputTsv['sequence'].tolist())
    for col in inputTsv_seq.columns:
        if col == 0: continue
        inputTsv_seq[col] = inputTsv_seq[col].str.slice(start=-1)
    
    inputTsv_seq = pd.Series(inputTsv_seq[inputTsv_seq.columns].values.tolist()).str.join('')
    print(inputTsv_seq)

    inputTsv_split = inputTsv_seq.apply(lambda x: pd.Series(list(x)))
    
    outdir = './tsv_result/{}'.format(args.data)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    
    # modified
    inputTsv_seq.to_csv('{}/{}_seq_{}.tsv'.format(outdir, args.data, args.len), sep='\t')
    # modified
    findTPTN(args.data)