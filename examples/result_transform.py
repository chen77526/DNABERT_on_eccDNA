import numpy as np
import pandas as pd
import argparse

mapping = pd.read_csv('../6-new-12w-0/vocab.txt', header=None)
mapping.columns = ['token']

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
    result.to_csv('./{}_{}_result.tsv'.format(ID, args.data), sep='\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default='C4-2')
    args = parser.parse_args()

    inputTsv = pd.read_csv('./sample_data/ft/eccdna_{}_comparison/6/dev.tsv'.format(args.data), skiprows=1, header=None, delimiter='\t')
    inputTsv.columns = ['sequence', 'label']
    inputTsv.drop(['label'], inplace=True, axis=1)
    inputTsv['sequence'] = inputTsv['sequence'].str.split(' ')
    inputTsv_seq = pd.DataFrame(inputTsv['sequence'].tolist())
    for col in inputTsv_seq.columns:
        if col == 0: continue
        inputTsv_seq[col] = inputTsv_seq[col].str.slice(start=-1)
    
    inputTsv_seq = pd.Series(inputTsv_seq[inputTsv_seq.columns].values.tolist()).str.join('')
    print(inputTsv_seq)
    inputTsv_seq.to_csv('./{}_seq.tsv'.format(args.data), sep='\t')

    dataType = ['C4-2', 'ES2', 'HeLaS3', 'LnCap', 'OVCAR8', 'PC-3', 'U937', 'leukocytes', 'muscle', 'pool_LCN', 'pool_LCT']
    for typeID in dataType:
        result = findTPTN(typeID)
        # TP.append(result['TP'])
        # TN.append(result['TN'])
        # FP.append(result['FP'])
        # FN.append(result['FN'])

    # for i in range(len(TP)):
    #     for col in TP[i].columns:
    #         # print(TP[i][col])
    #         if ((TP[i][col] < 5).any()):
    #             TP[i].drop(col, inplace=True, axis=1)
    #         if ((TN[i][col] < 5).any()):
    #             TN[i].drop(col, inplace=True, axis=1)
    #         if ((FP[i][col] < 5).any()):
    #             FP[i].drop(col, inplace=True, axis=1)
    #         if ((FN[i][col] < 5).any()):
    #             FN[i].drop(col, inplace=True, axis=1)
    
    # TP_all = TP[0].copy()
    # TN_all = TN[0].copy()
    # FP_all = FP[0].copy()
    # FN_all = FN[0].copy()

    # print('************ TP ************\n', TP_all, '************ TN ************\n', TN_all)
    # print('************ FP ************\n', FP_all, '************ FN ************\n', FN_all)
    # for i in range(1, len(TP)):
    #     TP_all = pd.merge(left=TP_all, right=TP[i], how='inner')
    #     TN_all = pd.merge(left=TN_all, right=TN[i], how='inner')

    # TP_all.to_csv('./TP_{}.csv'.format(args.data), sep='\t')
    # TN_all.to_csv('./TN_{}.csv'.format(args.data), sep='\t')