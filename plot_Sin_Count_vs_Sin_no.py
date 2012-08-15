import sys, os, pybedtools, math
from optparse import OptionParser , IndentedHelpFormatter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MaxNLocator
from matplotlib import patches


def process_file(fname,outfile):
    input = open(fname,'rt')
    #tags = {}
    no = []
    for line in input:
        if line.startswith("#"):
            continue
        if(len(line.split("\t")) == 9):
            chrom,junk,junk,start,end,tag,strand,junk,attr = line.split("\t")
            if float(get_std(attr.rstrip())) == 0:
                #if int(tag) in tags:
                    #tags[int(tag)] += 1
                no.append(int(tag))
                #else:
                #    tags[int(tag)] = 1
    plot_histogram(outfile,no)
    
    
def plot_histogram(outfile,no):
    #x = []
    #y = []
    #for i in tags.items():
    #    x.append(i)
    #    y.append(tags[i])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(no)
    plt.savefig(outfile)
    
        
def get_std(attr):
    if not ";" in attr:
        return(attr.split("=")[1])
    else:
        list1 = attr.split(";")
        for at in list1:
            if at.split("=")[0] == "stddev":
                return(at.split("=")[1])

usage = '''
input_paths may be:
- a directory to run on all files in them

example usages:
python plot_Sin_Count_vs_Sin_no.py /usr/local/peak-pairs/
'''.lstrip()


 
# We must override the help formatter to force it to obey our newlines in our custom description
class CustomHelpFormatter(IndentedHelpFormatter):
    def format_description(self, description):
        return description


def run():
    parser = OptionParser(usage='%prog [options] input_paths', description=usage, formatter=CustomHelpFormatter())
    #parser.add_option('-u', action='store', type='int', dest='up_distance',default=49,
    #                  help='Upstream distance to go from the peak-pair mid_point+1, Default=49.')
    #parser.add_option('-d', action='store', type='int', dest='down_distance',default=50,
    #                  help='Downstream distance to go from the peak-pair mid_point, Default=50')
    #parser.add_option('-i', action='store', type='int', dest='iter',default=100,
    #                  help='Number of iterations to do for shuffling')
    
    (options, args) = parser.parse_args()
    
    if not args:
        parser.print_help()
        sys.exit(1)
        
    if not os.path.exists(args[0]):
        parser.error('Path %s does not exist.' % args[0])
    for name in os.listdir(args[0]):
        if name.endswith('.gff'):
            fname = os.path.join(args[0], name)
            outfile = os.path.join(args[0],"SingeltonPlot_"+os.path.splitext(name)[0]+".png") 
            process_file(fname,outfile)
    
    
if __name__ == "__main__":
    run() 