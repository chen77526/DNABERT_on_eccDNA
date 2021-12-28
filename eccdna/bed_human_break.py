import argparse

def mainf():
    ### store every boundary of each chromosome into a dictionary
    bound = {}
    with open('./genome/human/hg38_noalt.fa.genome', 'r') as input_bound:
        for line in input_bound:
            bound[line.split('\t')[0]] = int(line.split('\t')[1])

    args.extend = int(args.extend)
    seq = []
    with open('./genome/human/hg38_noalt_gap.bed', 'r') as gap_f:
        with open('./db/cell_lines/{}_circleseq_eccdna_filt_uniq.bed'.format(args.cellline), 'r') as input_f:
            with open('./db/cell_lines/{}_circleseq_eccdna_filt_uniq_seq_{}_break.bed'.format(args.cellline, args.extend * 2), 'w') as output_f:
                with open('./db/cell_lines/{}_circleseq_eccdna_filt_uniq_excl_{}_break.bed'.format(args.cellline, args.extend * 2), 'w') as output_ex:
                    
                    ### write genome gap into exclude .bed file (for generating negative label .bed)
                    for line in gap_f:
                        name, start, end = line.split('\t')
                        output_ex.writelines('%s\t%s\t%s' % (name, start, end))
                    
                    ### Extend bidirectionally from both ends of eccDNA sequence
                    for line in input_f:
                        name, start, end = line.split('\t')
                        ### if sequence extends out of boundary, just put this sequence into excl .bed
                        if int(start) - args.extend < 0 or int(end) + args.extend > bound[name]:
                            output_ex.writelines('%s\t%s\t%s' % (name, start, end))
                        
                        ### save each breakpoint into positive label .bed
                        else:
                            output_f.writelines('%s\t%d\t%d\n' % (name, int(start)-args.extend, int(start)+args.extend))
                            output_f.writelines('%s\t%d\t%d\n' % (name, int(end)-args.extend, int(end)+args.extend))
                            output_ex.writelines('%s\t%d\t%d\n' % (name, int(start)-args.extend, int(end)+args.extend))
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--extend", type=int, default = '256')              # sequence length you want to extend from both ends
    parser.add_argument("--cellline", type=str)                             # cell line name
    args = parser.parse_args()
    mainf()   