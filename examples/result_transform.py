import pandas as pd
import argparse

def findTPTN(ID):
    focus = pd.read_csv('result_{}_{}.tsv'.format(ID, args.data), header=None, delimiter='\t')
    focus_re = focus.rename(columns={focus.columns[-2]: 'label', focus.columns[-1]: 'preds'})
    focus_TP = focus_re[(focus_re['label'] == 1) & (focus_re['preds'] == 1)]
    focus_TN = focus_re[(focus_re['label'] == 0) & (focus_re['preds'] == 0)]
    return {'TP' : focus_TP, 'TN' : focus_TN}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default='C4-2')
    args = parser.parse_args()

    dataType = ['C4-2', 'ES2', 'HeLaS3', 'LnCap', 'OVCAR8', 'PC-3', 'U937', 'leukocytes', 'muscle', 'pool_LCN', 'pool_LCT']
    TP, TN = [], []
    for typeID in dataType:
        result = findTPTN(typeID)
        TP.append(result['TP'])
        TN.append(result['TN'])

    for i in range(len(TP)):
        for col in TP[i].columns:
            # print(TP[i][col])
            if ((TP[i][col] < 5).any()):
                TP[i].drop(col, inplace=True, axis=1)
            if ((TN[i][col] < 5).any()):
                TN[i].drop(col, inplace=True, axis=1)
    
    TP_all = TP[0].copy()
    TN_all = TN[0].copy()

    print(TP_all, TN_all)
    for i in range(1, len(TP)):
        TP_all = pd.merge(left=TP_all, right=TP[i], how='inner')
        TN_all = pd.merge(left=TN_all, right=TN[i], how='inner')
    print(TP_all, TN_all)

    TP_all.to_csv('./TP_{}.csv'.format(args.data), sep='\t')
    TN_all.to_csv('./TN_{}.csv'.format(args.data), sep='\t')