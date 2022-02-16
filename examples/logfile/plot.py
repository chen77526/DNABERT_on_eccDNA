import argparse, re, string, glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

def search(path):
    with open(path, 'r') as f:
        txt = ' '.join(f.readlines())
        if args.data == 'acc':
            matches = re.findall('acc = (0.\d+)', txt)
        elif args.data == 'auc':
            matches = re.findall('auc = (0.\d+)', txt)
        elif args.data == 'loss':
            matches = re.findall('loss = (0.\d+)', txt)
    return matches

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='lr')
    parser.add_argument("--data", type=str, default='acc')
    args = parser.parse_args()
    paths = sorted(glob.glob("{}ecc_{}_*.log".format(args.input, args.data)), key = lambda num : float(num.split('/')[3].split('_')[2].strip('.log')))
    leg = ['{} = {}'.format(args.input.split('/')[2], path.split('/')[3].split('_')[2].strip('.log')) for path in paths]
    l = []
    for p in paths:
        tmp1 = search(p)
        tmp1 = [float(num) for num in tmp1]
        l.append(tmp1)

    match = 0
    with open('{}fine_tune_ecc_{}.log'.format(args.input, leg[0].strip('{} = '.format(args.input.split('/')[2]))), 'r') as f:
        txt = ' '.join(f.readlines())
        match = re.search('logging_steps=(\d+)', txt)
    
    ## original line
    x = np.arange(1, len(l[0])+1) * int(match.group(1))
    ll = np.array(l).T

    ## smooth line
    xnew = np.linspace(x.min(), x.max(), 300)
    spl = make_interp_spline(x, ll, k=3)  # type: BSpline
    ll_smooth = spl(xnew)
    
    plt.figure(1)
    plt.plot(xnew, ll_smooth)
    plt.title('{} eccDNA'.format(args.input.split('/')[1].split('_')[0]), fontdict = {'fontsize' : 30})
    plt.xlabel('steps', fontsize = 20)
    if args.data == 'acc':
        plt.ylabel('Accuracy', fontsize = 20)
    elif args.data == 'auc':
        plt.ylabel('Area under the ROC Curve', fontsize = 20)
    elif args.data == 'loss':
        plt.ylabel('Loss', fontsize = 20)
    
    plt.legend(labels = leg, loc = 0)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8)

    plt.savefig('{}/{}_smooth.png'.format(args.input, args.data), dpi = 100)
    
    plt.figure(2)
    plt.plot(x, ll)
    plt.xlabel('steps', fontsize = 20)
    if args.data == 'acc':
        plt.ylabel('Accuracy', fontsize = 20)
    elif args.data == 'auc':
        plt.ylabel('Area under the ROC Curve', fontsize = 20)
    elif args.data == 'loss':
        plt.ylabel('Loss', fontsize = 20)
    
    plt.legend(labels = leg, loc = 0)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8)
    
    plt.savefig('{}/{}.png'.format(args.input, args.data), dpi = 100)