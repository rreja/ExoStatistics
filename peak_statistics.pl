use strict;
use warnings;
use File::Basename;
use Getopt::Std;

my %opt;
getopt('i',\%opt);
&help_message if (defined $opt{h});

# Decalre all the global variables
my %options;
my (@tagcounts,@stds);
my ($stddev); my $peakcount = 0; my $singletoncount= 0;

my $dir = $opt{'i'}; #remember to put a "/" at the end of the directory.
opendir DIR, $dir || die "Cannot open the directory";

$dir = check_dir($dir);

#check if output direcory exists.
#unless(-d $dir."output/"){
#    system("mkdir ".$dir."output/");
#}

open OUT1, ">".$dir."peak_stats.txt" || die "File not found"; # the file containing the summary
print OUT1 "Filename\tMapped_reads\tUniquely_mapped_reads\tPeaks\tSingletons\tPeak_median_excluding_singletons\tPeak_mean_exclusing_singletons\tMedian_std_excluding_singeltons\tMean_std_excluding_singletons\n";

while( (my $filename = readdir(DIR))){

next if($filename =~ /^\./);
next if($filename =~ /NoS/);
# Using fileparser to get the basename and path
my ($fname,$path,$suffix) = fileparse($filename,".gff");
my $basename = basename($filename, ".gff");

if($suffix eq ".gff"){


open IN,$dir.$filename || die "Input file not found\n";
open OUT, ">".$dir.$basename."_NoS.gff" || die "Output file not found";

#print OUT1 "Filename\tMapped_reads\tUniquely_mapped_reads\tPeaks\tSingletons\tPeak_median_excluding_singletons\tPeak_mean_exclusing_singletons\tMedian_std_excluding_singeltons\tMean_std_excluding_singletons\n";
while(<IN>){
    
    chomp($_);
    next if($_ =~ /^#/);
# Extracting stddev from file based on the 9th column, if it has ';' seperation or not
    my @cols = split(/\t/,$_);
    if($cols[8] =~ m/;/){
        my @array = split(/;/,$cols[8]);
        foreach my $val (@array){
            if((split(/=/,$val))[0] eq "stddev"){
                $stddev = (split(/=/,$val))[1];
                
            }
        }
    }
    elsif((split(/=/,$cols[8]))[0] eq "stddev"){
        $stddev = (split(/=/,$cols[8]))[1];
        
    }
    
    if($stddev > 0.0){
       print OUT $_."\n";
        $peakcount++;
        push(@tagcounts,$cols[5]);
        push(@stds,$stddev);
    }
    else{
        $singletoncount++;
        
    }
   
}

print OUT1 $basename.".gff"."\t.\t.\t".$peakcount."\t".$singletoncount."\t".median(@tagcounts)."\t".mean(@tagcounts)."\t".median(@stds)."\t".mean(@stds)."\n";
close(OUT);
close(IN);
 }

}



sub median{
    my @a = sort {$a <=> $b} @_;
  return ($a[$#a/2] + $a[@a/2]) / 2;
}

sub mean{
  @_ or return 0;
  my $sum = 0;
  $sum += $_ foreach @_;
  return $sum/@_;
}

sub check_dir{
    my $dir = shift;
    my $tmp = substr($dir,-1,1);
    if($tmp eq "/"){
        return($dir);
    }
    else{
        return($dir."/");
    }
}

sub help_message {
  print qq{
Program: peak_statistics.pl (Calculate stats on peak calls)
Contact: Rohit Reja <rzr142\@psu.edu>
Usage:   peak_statistics.pl -i <peak_calls_file_directory>

    NOTE:    If you input files were saved using MS excel, then use:  perl -p -e 's/^M//g;' <input_file> > <input_file_no_excel_characters>
             to remove the excel characters in your file. ^M sould be typed as "ctrl-v-m". Or else the script will not work properly. Peak
             calls should be in "gff" format.
             
    Options: -i <path1>     path to the folder with peak call files [accepted file format, gff].
             -h             help 

    Example:
      perl peak_statistics.pl -i  .  [if your files are in the current directory]
      perl robust_peak_pair_stats.pl -i genetrack_s5e10F1/cwpair_output_mode_f0u0d100b3
      
    Output:
    Produces a "peak_stats.txt" file and also produces a "_NoS" file that contains all the
    non-singelton peaks in it. These files will be present in the folder that contains the peak call files.
  
  };
  exit;
}






