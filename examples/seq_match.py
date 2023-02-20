import os
import argparse
import numpy as np
import pandas as pd

# if __name__ == '__main__':
parser = argparse.ArgumentParser()
parser.add_argument("--modelType", type=str, help="model type")
parser.add_argument("--testSetType", type=str, help="test set type")
parser.add_argument("--ref", type=str, help="real sequence file name")
parser.add_argument("--len", type=int, default=1024, help="sequence length")
parser.add_argument("--sel", type=bool, default=False, help="self-testing or not")
args = parser.parse_args()

merge_result = 'tsv_result/{}/{}_{}_result_{}.tsv'.format(args.testSetType, args.modelType, args.testSetType, args.len)
input_PN_tsv = pd.read_csv(merge_result, index_col=0, skiprows=1, header=None, delimiter='\t')
print(input_PN_tsv)
seq_result = 'tsv_result/{}/{}_seq_{}.tsv'.format(args.testSetType, args.testSetType, args.len)
input_seq_tsv = pd.read_csv(seq_result, index_col=0, skiprows=1, header=None, delimiter='\t')
print(input_seq_tsv)

mapping = {}
PN = {}

ref_seq = '../eccdna/output/human/{}'.format(args.ref)
if not args.sel:
  with open(ref_seq) as refer_positive_train:
    all_lines = refer_positive_train.readlines()
    for i in range(0, len(all_lines), 2):
      mapping[all_lines[i+1][:-1].upper()] = all_lines[i][1:-1]
      PN[all_lines[i+1][:-1].upper()] = 'positive'
  
  ref_n_tr = ref_seq.replace('positive', 'negative')
  with open(ref_n_tr) as refer_negative_train:
    all_lines = refer_negative_train.readlines()
    for i in range(0, len(all_lines), 2):
      mapping[all_lines[i+1][:-1].upper()] = all_lines[i][1:-1]
      PN[all_lines[i+1][:-1].upper()] = 'negative'
        
ref_p_te = ref_seq.replace('train', 'test')
with open(ref_p_te) as refer_positive_test:
  all_lines = refer_positive_test.readlines()
  for i in range(0, len(all_lines), 2):
    mapping[all_lines[i+1][:-1].upper()] = all_lines[i][1:-1]
    PN[all_lines[i+1][:-1].upper()] = 'positive'
    
ref_n_te = ref_p_te.replace('positive', 'negative')
with open(ref_n_te) as refer_negative_test:
  all_lines = refer_negative_test.readlines()
  for i in range(0, len(all_lines), 2):
    mapping[all_lines[i+1][:-1].upper()] = all_lines[i][1:-1]
    PN[all_lines[i+1][:-1].upper()] = 'negative'

input_PN_tsv.columns = ['result']
input_seq_tsv.columns = ['sequence']
input_seq_tsv['result'] = input_PN_tsv['result']
input_seq_tsv['location'] = input_seq_tsv['sequence'].map(mapping)
input_seq_tsv['PN'] = input_seq_tsv['sequence'].map(PN)

outdir = './location/{}'.format(args.testSetType)
if not os.path.exists(outdir):
  os.mkdir(outdir)
        
input_seq_tsv.to_csv('./location/{}/{}_location_{}.tsv'.format(args.testSetType, args.testSetType, args.len), sep='\t')
print(input_seq_tsv)