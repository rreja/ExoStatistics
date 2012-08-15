import sys, os
from optparse import OptionParser , IndentedHelpFormatter


def process_file(fname,outfile):
    input = open(fname,'rt')
    fo = open(outfile,'wb')
    for line in input:
        if line.startswith("#"):
            continue
        if(len(line.split("\t")) == 9):
            chrom,junk,junk,start,end,tag,strand,junk,attr = line.split("\t")
            if float(get_std(attr.rstrip())) == 0:
                fo.write(line)
                

  
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
- a single file.

example usages:
python create_singleton_from_peaks.py /usr/local/peaks/
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
        
    if not os.path.isdir(args[0]):
        outfile = os.path.join(os.path.dirname(args[0]),"Singelton_"+os.path.splitext(os.path.basename(args[0]))[0]+".txt")
        process_file(args[0],outfile)
    else:
                
        if not os.path.exists(args[0]):
            parser.error('Path %s does not exist.' % args[0])
        for name in os.listdir(args[0]):
            if name.endswith('.gff'):
                fname = os.path.join(args[0], name)
                outfile = os.path.join(args[0],"Singelton_"+os.path.splitext(name)[0]+".txt") 
                process_file(fname,outfile)
    
    
if __name__ == "__main__":
    run() 