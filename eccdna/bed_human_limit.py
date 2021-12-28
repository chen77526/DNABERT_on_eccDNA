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
            with open('./db/cell_lines/{}_circleseq_eccdna_filt_uniq_seq_{}_{}.bed'.format(args.cellline, args.extend * 2, args.limit), 'w') as output_f:
                with open('./db/cell_lines/{}_circleseq_eccdna_filt_uniq_excl_{}_{}.bed'.format(args.cellline, args.extend * 2, args.limit), 'w') as output_ex:
                    ### write genome gap into exclude .bed file (for generating negative label .bed)
                    for line in gap_f:
                        name, start, end = line.split('\t')
                        output_ex.writelines('%s\t%s\t%s' % (name, start, end))
                    
                    ### select sequence shorter than constraint you set, and extend bidirectionally from their center 
                    for line in input_f:
                        name, start, end = line.split('\t')
                        mid = (int(end) + int(start)) // 2
                        if int(end) - int(start) <= args.limit:
                            ### if sequence extend out of boundary, just put this sequence into excl .bed
                            if mid - args.extend < 0 or mid + args.extend > bound[name]:
                                output_ex.writelines('%s\t%s\t%s' % (name, start, end))
                            else:
                                output_f.writelines('%s\t%d\t%d\n' % (name, mid-args.extend, mid+args.extend))
                                output_ex.writelines('%s\t%d\t%d\n' % (name, mid-args.extend, mid+args.extend))
                        else:
                            output_ex.writelines('%s\t%s\t%s' % (name, start, end))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--extend", type=int, default = '256')                  # sequence length you want to extend from center
    parser.add_argument("--cellline", type=str)                                 # cell line name
    parser.add_argument("--limit", type=int, default= '1000')                   # sequence limit
    args = parser.parse_args()
    mainf()   