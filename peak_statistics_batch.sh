USAGE="Usage: `basename $0` -i path_to_input_files"

if [ $# -eq 0 ];then
   echo $USAGE >&2
   exit 1
fi

while getopts i: OPT; do
     case "$OPT" in
           i)FIPATH=$OPTARG
                ;;
           *)
              echo $USAGE >&2
              exit 1
                ;;
     esac
done

abspath=$FIPATH"output"

# Create the output folder 'output'
if [ -d $abspath ]
then
echo "Output folder exists. Copying the output files here"
else
mkdir $abspath
fi

# Writing the statistics to peak statistics files
stats=$abspath"/peak_statistics.txt"
echo "Filename  Mapped_reads    Uniquely_mapped_reads   Peaks   Singletons  Peak_median_excluding_singletons    Peak_mean_exclusing_singletons  Median_std_excluding_singeltons Mean_std_excluding_singletons" >$stats

# list all the files present in the folder
files="filelist.tmp"
ls $FIPATH >$files


while read f
do

#Check if the file extension is gff and run the perl script only on gff files
extension=${f##*.}
if [ "$extension" = "gff" ]
then
echo "processing "$f
perl peak_statistics.pl $FIPATH$f >>$stats
fi

done < $files

#removing the temp files.
#mv $stats output/
rm $files