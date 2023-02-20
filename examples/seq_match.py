import os
import argparse
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--modelType", type=str, help="model type")
parser.add_argument("--testSetType", type=str, help="test set type")
parser.add_argument("--ref", type=str, help="real sequence file name (positive)")
parser.add_argument("--len", type=int, default=1024, help="sequence length")
parser.add_argument("--sel", type=bool, default=False, help="self-testing or not")
args = parser.parse_args()

merge_result = 'tsv_result/{}/{}_{}_result_{}.tsv'.format(args.modelType, args.testSetType, args.testSetType, args.len)
input_PN_tsv = pd.read_csv(merge_result, index_col=0, skiprows=1, header=None, delimiter='\t')
print(input_PN_tsv)
seq_result = 'tsv_result/{}/{}_seq_{}.tsv'.format(args.testSetType, args.testSetType, args.len)
input_seq_tsv = pd.read_csv(seq_result, index_col=0, skiprows=1, header=None, delimiter='\t')
print(input_seq_tsv)

mapping = {}
PN = {}
        
ref_seq = '../eccdna/output/human/{}'.format(args.ref)
with open(ref_seq) as refer_positive_test:
  all_lines = refer_positive_test.readlines()
  for i in range(0, len(all_lines), 2):
    mapping[all_lines[i+1][:-1].upper()] = all_lines[i][1:-1]
    PN[all_lines[i+1][:-1].upper()] = 'positive'
    
ref_seq_neg = ref_seq.replace('positive', 'negative')
with open(ref_seq_neg) as refer_negative_test:
  all_lines = refer_negative_test.readlines()
  for i in range(0, len(all_lines), 2):
    mapping[all_lines[i+1][:-1].upper()] = all_lines[i][1:-1]
    PN[all_lines[i+1][:-1].upper()] = 'negative'

CNN_result_positive = '../../output/CNN/{}/{}_circleseq_eccdna_file_uniq_pred_positive.fa'.format(args.testSetType, args.testSetType)
CNN_result_negative = '../../output/CNN/{}/{}_circleseq_eccdna_file_uniq_pred_negative.fa'.format(args.testSetType, args.testSetType)

CNN_result = {'sequence' : [], 'CNN_result' : []}
with open(CNN_result_positive) as CNN_pred_positive:
  all_lines = CNN_pred_positive.readlines()
  for i in range(0, len(all_lines), 2):
    CNN_result['sequence'].append(all_lines[i+1][:-1].upper())
    CNN_result['CNN_result'].append('TP' if PN[all_lines[i+1][:-1].upper()] == 'positive' else 'FP')

with open(CNN_result_negative) as CNN_pred_negative:
  all_lines = CNN_pred_negative.readlines()
  for i in range(0, len(all_lines), 2):
    CNN_result['sequence'].append(all_lines[i+1][:-1].upper())
    CNN_result['CNN_result'].append('TN' if PN[all_lines[i+1][:-1].upper()] == 'negative' else 'FN')

input_PN_tsv.columns = ['DNABERT_result']
input_seq_tsv.columns = ['sequence']
input_seq_tsv['location'] = input_seq_tsv['sequence'].map(mapping)
input_seq_tsv['PN'] = input_seq_tsv['sequence'].map(PN)
input_seq_tsv['DNABERT_result'] = input_PN_tsv['DNABERT_result']

CNN_tsv = pd.DataFrame(CNN_result)
final_result = pd.merge(input_seq_tsv, CNN_tsv)

conditions = [
    ((final_result['DNABERT_result'] == 'TP') | (final_result['DNABERT_result'] == 'TN')) & ((final_result['CNN_result'] == 'TP') | (final_result['CNN_result'] == 'TN')),
    ((final_result['DNABERT_result'] == 'TP') | (final_result['DNABERT_result'] == 'TN')) & ((final_result['CNN_result'] == 'FP') | (final_result['CNN_result'] == 'FN')),
    ((final_result['DNABERT_result'] == 'FP') | (final_result['DNABERT_result'] == 'FN')) & ((final_result['CNN_result'] == 'TP') | (final_result['CNN_result'] == 'TN')),
    ((final_result['DNABERT_result'] == 'FP') | (final_result['DNABERT_result'] == 'FN')) & ((final_result['CNN_result'] == 'FP') | (final_result['CNN_result'] == 'FN'))
]
choices = ['Both correct', 'DNABERT', 'CNN', 'Both fail']

final_result['comparison'] = np.select(conditions, choices)

outdir = './location/{}'.format(args.testSetType)
if not os.path.exists(outdir):
  os.mkdir(outdir)
        
final_result.to_csv('./location/{}/{}_location_{}.tsv'.format(args.testSetType, args.testSetType, args.len), sep='\t')
print(final_result)