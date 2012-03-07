use strict;
use warnings;
use File::Basename;


# Decalre all the global variables
my %options;
my (@tagcounts,@stds);
my ($stddev); my $peakcount = 0; my $singletoncount= 0;

# Using fileparser to get the basename and path
my ($fname,$path,$suffix) = fileparse($ARGV[0],".gff");
my $basename = basename($ARGV[0], ".gff");

open IN,$ARGV[0] || "Input file not found\n";
open OUT,">".$path.$basename."_NoS.gff" || "Output file not found"; # change here if you want to change the output file directory


while(<IN>){
    
    chomp($_);
# Extracting stddev from file based on the 9th column, if it has ';' seperation or not
    my @cols = split(/\t/,$_);
    if($cols[8] =~ m/.*;.*/){
        foreach my $val (split(/;/,$cols[8])){
            if((split(/=/,$val))[0] eq "stddev"){
                $stddev = (split(/=/,$val))[1];
                last;
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

print $ARGV[0]."\t.\t.\t".$peakcount."\t".$singletoncount."\t".median(@tagcounts)."\t".mean(@tagcounts)."\t".median(@stds)."\t".mean(@stds)."\n";

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

