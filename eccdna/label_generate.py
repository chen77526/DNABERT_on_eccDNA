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
            with open('./output/{}/{}_{}_positive_{}.fa.out'.format(args.data, args.data, args.gene, args.length), 'r') as input_f1:
                with open('./output/{}/{}_{}_negative_{}.fa.out'.format(args.data, args.data, args.gene, args.length), 'r') as input_f2:
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
                    
                    ### randomly select sequence into validation set (10%) and add label on each sequence
                    positive_dev = random.sample(positive, len(positive)//10)
                    negative_dev = random.sample(negative, len(negative)//10)
                    for seq in positive_dev:
                        output_f2.writelines("%s\t%d\n" % (seq, 1))
                        positive.remove(seq)
                    for seq in negative_dev:
                        output_f2.writelines("%s\t%d\n" % (seq, 0))
                        negative.remove(seq)

                    for seq in positive:
                        output_f1.writelines("%s\t%d\n" % (seq, 1))
                    for seq in negative:
                        output_f1.writelines("%s\t%d\n" % (seq, 0))
             
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=str, default = '512')                  # sequence length
    parser.add_argument("--data", type=str)                                     # species name
    parser.add_argument("--gene", type=str)                                     # cell line name
    args = parser.parse_args()
    mainf()