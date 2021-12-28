import argparse

def mainf():
    with open(args.input, 'r') as input_f:
        with open(args.output, 'w') as output_f:
            for line in input_f:
                comp = ''
                for base in line:
                    if base == 'A':
                        comp += 'T'
                    elif base == 'T':
                        comp += 'A'
                    elif base == 'C':
                        comp += 'G'
                    elif base == 'G':
                        comp += 'C'
                    else:
                        comp += base
                output_f.writelines(comp)

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='./eccdna_leukocytesall/6/dev.tsv')
    parser.add_argument('--output', type=str, default='./eccdna_leukocytesall_comp/6/dev.tsv')
    args = parser.parse_args()
    mainf()