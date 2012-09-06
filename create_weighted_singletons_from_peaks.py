import sys, os
from scipy.stats import stats as st
from optparse import OptionParser , IndentedHelpFormatter
import pybedtools

allInfo = {}

def process_file(filename,outfile,sg07,options):
    input = open(filename,'rt')
    fwtS = open(outfile,'wb')
    region = options.ex/2
    posS = ""
    negS = ""
    posnoS = ""
    negnoS = ""
    allS   = ""
    countS = 0
    countnoS = 0
    tagS = []
    tagnoS = []
    std = []
    for line in input:
        if line.startswith("#"):
            fwtS.write(line)
            continue
        if(len(line.split("\t")) == 9):
            chrom,junk,junk,start,end,tag,strand,junk,attr = line.split("\t")
            
            if float(get_std(attr.rstrip())) == 0:
                tagS.append(int(tag))
                if strand == "+":
                    posS = posS+line
                else:
                    negS = negS+line
                    
            else:
                countnoS +=1
                std.append(float(get_std(attr.rstrip())))
                tagnoS.append(int(tag))
                allS = allS+line
                if strand == "+":
                    posnoS = posnoS+line
                else:
                    negnoS = negnoS+line
                    
    #posS_int_negnoS = pybedtools.BedTool(posS,from_string=True).slop(g=sg07,l=10,r=10).intersect(pybedtools.BedTool(negnoS,from_string=True),u=True) # add half the exclusion zone to start and end coordinate
    #negS_int_posnoS = pybedtools.BedTool(negS,from_string=True).slop(g=sg07,l=10,r=10).intersect(pybedtools.BedTool(posnoS,from_string=True),u=True)
    try:
    
        posS_int_negnoS = pybedtools.BedTool(posS,from_string=True).intersect(pybedtools.BedTool(negnoS,from_string=True).slop(g=sg07,l=region,r=region),u=True) # add half the exclusion zone to start and end coordinate
        negS_int_posnoS = pybedtools.BedTool(negS,from_string=True).intersect(pybedtools.BedTool(posnoS,from_string=True).slop(g=sg07,l=region,r=region),u=True)
        fullFile = allS+str(posS_int_negnoS)+str(negS_int_posnoS) # merging singletons and non singletons together
        countS = posS_int_negnoS.count() + negS_int_posnoS.count() # Couting all the singletongs
        fwtS.write(str(pybedtools.BedTool(fullFile,from_string=True).sort()))
    except pybedtools.helpers.BEDToolsError:
        # if the peak call file had no singletons in it.
        print "The file had no singletons"
        countS = 0
        fullFile = allS
        fwtS.write(str(pybedtools.BedTool(fullFile,from_string=True).sort()))
        
    ratio = signal2noise(tagnoS,tagS) # calculating the signal to noise ratio.   
    #fullFile = allS+str(posS_int_negnoS)+str(negS_int_posnoS) # merging singletons and non singletons together
    #countS = posS_int_negnoS.count() + negS_int_posnoS.count() # Couting all the singletongs
    #fwtS.write(str(pybedtools.BedTool(fullFile,from_string=True).sort()))
    #ratio = signal2noise(tagnoS,tagS) # calculating the signal to noise ratio.
    allInfo[os.path.basename(filename)] = ".\t.\t"+str(countnoS)+"\t"+str(countS)+"\t"+str(st.nanmedian(tagnoS))+"\t"+str(st.nanmean(tagnoS))+"\t"+str(st.nanmedian(std))+"\t"+str(st.nanmean(std))+"\t"+str(ratio)
    

def get_std(attr):
    if not ";" in attr:
        return(attr.split("=")[1])
    else:
        list1 = attr.split(";")
        for at in list1:
            if at.split("=")[0] == "stddev":
                return(at.split("=")[1])


def print_stats(stats):
    fstats = open(stats,'wb')
    header = "Filename\tMapped_reads\tUniquely_mapped_reads\tPeaks\tSingletons\tPeak_median_excluding_singletons\tPeak_mean_exclusing_singletons\tMedian_std_excluding_singeltons\tMean_std_excluding_singletons\tSignal2Nose"
    fstats.write(header)
    fstats.write("\n")
    for k,v in allInfo.items():
        fstats.write(k+"\t"+v)
        fstats.write("\n")
    
def signal2noise(tags,Stags):
    if sum(Stags) == 0:
        return(1) # instead of returning Nan I want to see those values with no singletons, hence the value 1
    else:
        return(float(sum(tags)/sum(Stags)))   

usage = '''
input_paths may be:
- a directory to run on all files in them
- a single file.

REQUIREMENT:
1) a file with chromosome lengths in it, in the format: chr1 1 1000000

example usages:
python create_weighted_singletons_from_peaks.py /usr/local/peaks/genetrack_peaks.gff
python create_weighted_singletons_from_peaks.py /usr/local/peaks/genetrack_s5e10/
'''.lstrip()


 
# We must override the help formatter to force it to obey our newlines in our custom description
class CustomHelpFormatter(IndentedHelpFormatter):
    def format_description(self, description):
        return description





def run():
    parser = OptionParser(usage='%prog [options] input_paths', description=usage, formatter=CustomHelpFormatter())
    parser.add_option('-e', action='store', type='int', dest='ex',default=20,
                      help='Exclusion zone used during peak calling.Default 20')
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
        import pybedtools
    except ImportError:
        print "You need to install Scipy(http://www.scipy.org/Download) before you can run this script."
        print "If you have Scipy installed, then you should check if you have pybedtools installed"
        sys.exit(1)
        
    sg07 = os.path.join(os.path.dirname(os.path.abspath(__file__)),"sg07.txt") # location of the chromosome length file. Located with the scripts. DO NOT change
    
    if not os.path.isdir(args[0]):
        # Create dir names for wtS folders
        outdir_wtS = os.path.join(os.path.dirname(args[0]),"_wtS")
                
        # Check if wtS dir exists else create them
        if not os.path.exists(outdir_wtS) :
            os.mkdir(outdir_wtS)
        
        outfile_wtS = os.path.join(outdir_wtS,os.path.splitext(os.path.basename(args[0]))[0]+"wtS.gff")
        stats = os.path.join(outdir_wtS,"peak_stats.txt")
        process_file(args[0],outfile_wtS,sg07,options)
        print_stats(stats)
    else:
                
        if not os.path.exists(args[0]):
            parser.error('Path %s does not exist.' % args[0])
            
        # Create dir names for noS and onlyS folders
        outdir_wtS = os.path.join(args[0],"_wtS")
        
        if not os.path.exists(outdir_wtS):
            os.mkdir(outdir_wtS)
        stats = os.path.join(outdir_wtS,"peak_stats.txt")
        for name in os.listdir(args[0]):
            if name.endswith('.gff'):
                fname = os.path.join(args[0], name)
                outfile_wtS = os.path.join(outdir_wtS,os.path.splitext(name)[0]+"wtS.gff")
                process_file(fname,outfile_wtS,sg07,options)
        print_stats(stats)
    
if __name__ == "__main__":
    run() 