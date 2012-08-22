import sys, os
from scipy.stats import stats as st
from optparse import OptionParser , IndentedHelpFormatter

filedict = {}

def process_file(fname,out_noS,out_onlyS):
    input = open(fname,'rt')
    fnoS = open(out_noS,'wb')
    fonlyS = open(out_onlyS,'wb')
    tags = []  # tags in non singletons
    Stags = [] # Tags in singletons
    std = []   
    singletonCount = 0
    for line in input:
        if line.startswith("#"):
            fnoS.write(line)
            continue
        if(len(line.split("\t")) == 9):
            chrom,junk,junk,start,end,tag,strand,junk,attr = line.split("\t")
            
            if float(get_std(attr.rstrip())) == 0:
                singletonCount+=1
                Stags.append(int(tag))
                fonlyS.write(line)
            else:
                tags.append(int(tag))
                std.append(float(get_std(attr.rstrip())))
                fnoS.write(line)
    ratio = signal2noise(tags,Stags)
    filedict[os.path.basename(fname)] = ".\t.\t"+str(len(tags))+"\t"+str(singletonCount)+"\t"+str(st.nanmedian(tags))+"\t"+str(st.nanmean(tags))+"\t"+str(st.nanmedian(std))+"\t"+str(st.nanmean(std))+"\t"+str(ratio)

def print_stats(stats):
    fstats = open(stats,'wb')
    header = "Filename\tMapped_reads\tUniquely_mapped_reads\tPeaks\tSingletons\tPeak_median_excluding_singletons\tPeak_mean_exclusing_singletons\tMedian_std_excluding_singeltons\tMean_std_excluding_singletons\tSignal2Nose"
    fstats.write(header)
    fstats.write("\n")
    for k,v in filedict.items():
        fstats.write(k+"\t"+v)
        fstats.write("\n")
        
def get_std(attr):
    if not ";" in attr:
        return(attr.split("=")[1])
    else:
        list1 = attr.split(";")
        for at in list1:
            if at.split("=")[0] == "stddev":
                return(at.split("=")[1])

def signal2noise(tags,Stags):
    if sum(Stags) == 0:
        return(1) # instead of returning Nan I want to see those values with no singletons, hence the value 1
    else:
        return(float(sum(tags)/sum(Stags)))
    
usage = '''
input_paths may be:
- a directory to run on all files in them
- a single file.

example usages:
python generate_noS_onlyS_statistics_from_peaks.py /usr/local/peaks/genetrack_peaks.gff
python generate_noS_onlyS_statistics_from_peaks.py /usr/local/peaks/genetrack_s5e10/
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
    # Check if all the required arguments are provided, else exit     
    if not args:
        parser.print_help()
        sys.exit(1)
        
    try:
        from scipy.stats import stats
    except ImportError:
        print "You need to install Scipy(http://www.scipy.org/Download) before you can run this script."
        sys.exit(1)
    
    if not os.path.isdir(args[0]):
        # Create dir names for noS and onlyS folders
        outdir_noS = os.path.join(os.path.dirname(args[0]),"_noS")
        outdir_onlyS = os.path.join(os.path.dirname(args[0]),"_onlyS")
        
        # Check if noS and onlyS dir exists else create them
        if not os.path.exists(outdir_noS) and not os.path.exists(outdir_onlyS) :
            os.mkdir(outdir_noS)
            os.mkdir(outdir_onlyS)
        
        outfile_noS = os.path.join(outdir_noS,os.path.splitext(os.path.basename(args[0]))[0]+"noS.gff")
        outfile_onlyS = os.path.join(outdir_onlyS,os.path.splitext(os.path.basename(args[0]))[0]+"onlyS.gff")
        stats = os.path.join(outdir_noS,"peak_stats.txt")
        process_file(args[0],outfile_noS,outfile_onlyS)
        print_stats(stats)
    else:
                
        if not os.path.exists(args[0]):
            parser.error('Path %s does not exist.' % args[0])
            
        # Create dir names for noS and onlyS folders
        outdir_noS = os.path.join(args[0],"_noS")
        outdir_onlyS = os.path.join(args[0],"_onlyS")
        
        if not os.path.exists(outdir_noS) and not os.path.exists(outdir_onlyS) :
            os.mkdir(outdir_noS)
            os.mkdir(outdir_onlyS)
        stats = os.path.join(outdir_noS,"peak_stats.txt")
        for name in os.listdir(args[0]):
            if name.endswith('.gff'):
                fname = os.path.join(args[0], name)
                outfile_noS = os.path.join(outdir_noS,os.path.splitext(name)[0]+"noS.gff")
                outfile_onlyS = os.path.join(outdir_onlyS,os.path.splitext(name)[0]+"onlyS.gff")
                process_file(fname,outfile_noS,outfile_onlyS)
        print_stats(stats)
    
if __name__ == "__main__":
    run() 