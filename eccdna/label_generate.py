import csv, random, argparse
import pandas as pd

def seq2kmer(seq, k):
    '''
    Convert original sequence to kmers
    
    Arguments:
    seq -- str, original sequence.
    k -- int, kmer of length k specified.
    
    Returns:
    kmers -- str, kmers separated by space

    '''
    kmer = [seq[x:x+k] for x in range(len(seq)+1-k)]
    kmers = " ".join(kmer)
    return kmers.upper()

def mainf():
    with open ('./output/{}/label_{}.tsv'.format(args.data, args.length), 'w') as output_f1:
        with open ('./output/{}/label_{}_dev.tsv'.format(args.data, args.length), 'w') as output_f2:
            with open('./output/{}/{}_{}_positive_{}_limit.fa.out'.format(args.data, args.data, args.cellline, args.length), 'r') as input_f1:
                with open('./output/{}/{}_{}_negative_{}_limit.fa.out'.format(args.data, args.data, args.cellline, args.length), 'r') as input_f2:
                    ### split sequence into 6-mers
                    num1, num2 = 0, 0
                    positive, negative = [], []
                    for line in input_f1:
                        if num1 % 2 == 1:
                            positive.append(seq2kmer(line.split('\n')[0], 6))
                        num1 += 1
                    for line in input_f2:
                        if num2 % 2 == 1:
                            negative.append(seq2kmer(line.split('\n')[0], 6))
                        num2 += 1
                    
                    ### randomly select sequence into validation set (20%) and add label on each sequence
                    positive_dev, positive = positive[:len(positive) // 5], positive[len(positive) // 5:]
                    negative_dev, negative = negative[:len(negative) // 5], negative[len(negative) // 5:]
                    
                    for seq in positive_dev:
                        output_f2.writelines("%s\t%d\n" % (seq, 1))
                    for seq in negative_dev:
                        output_f2.writelines("%s\t%d\n" % (seq, 0))

                    for seq in positive:
                        output_f1.writelines("%s\t%d\n" % (seq, 1))
                    for seq in negative:
                        output_f1.writelines("%s\t%d\n" % (seq, 0))
             
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=str, default = '512')                  # sequence length
    parser.add_argument("--data", type=str)                                     # species name
    parser.add_argument("--cellline", type=str)                                 # type name
    args = parser.parse_args()
    mainf()