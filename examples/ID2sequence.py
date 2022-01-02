import pandas as pd
import argparse

mapping = pd.read_csv('../6-new-12w-0/vocab.txt', header=None)
mapping.columns = ['token']

def mapSeq(inputFile):
    outputFile = pd.DataFrame().reindex_like(inputFile).astype(str)
    outputFile.drop('Unnamed: 0', inplace=True, axis=1)
    print(inputFile)
    for id in inputFile.index:
        for idx in inputFile.loc[id].index:
            if idx == "Unnamed: 0": continue
            elif idx == "1":
                outputFile.at[id, idx] = mapping['token'][inputFile.loc[id, idx]]
            else:
                outputFile.at[id, idx] = mapping['token'][inputFile.loc[id, idx]][-1]
        
    outputFile['seq'] = pd.Series(outputFile[outputFile.columns].values.tolist()).str.join('')
    print(outputFile)
    output = outputFile['seq']
    return output
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default='TP')
    parser.add_argument("--data", type=str, default='leukocytes')
    args = parser.parse_args()
    inputTsv = pd.read_csv('./{}_{}.csv'.format(args.type, args.data), header=0, delimiter='\t', dtype=int)
    # for idx in mapping.index:
    #     print(idx, '\t', mapping['token'][idx])
    sequence = mapSeq(inputTsv)
    sequence.to_csv('./{}_{}_sequence.csv'.format(args.type, args.data), sep='\t')