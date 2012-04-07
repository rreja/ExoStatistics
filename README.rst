Peak Statistics
================

Introduction
-------------

The scripts in this repository can be used to perform some basic statistics on the "peak calls". The "peak calls" file is the output file obtained by running genetrack program on the index/raw tag file.

The basic operations include separating the singleton and non-singelton peaks and then calculating the median and average of tag counts and standard deviations.


Requirements
------------

- The script only requires Perl_ (5 or higher) to run.
- The input file should be in standard Gff_ format

THE SCRIPT WILL BREAK IF:
------------------------

- The files have excel ^M character in it. For sanity check, open your file in terminal, to see if you can see ^M character in your file. In case, you find ^M character in your file, use the following command to remove it::

    $ perl -p -e 's/^M/\n/g;' <file_with_excel_char> > <new_file>

- If the input files are not in the standard Gff_ format.


Installing and Running the scripts
------------

Unpack the source code archive. The folder contains the following::

-  peak_statistics.pl: Script for basic statistics.
-  README.rst: Readme file
-  sample.gff: The sample input file to test the script.


To get help on the parameters, type::

    $ perl  peak_statistics.pl -h
    $ Options: -i <path1>     path to the folder with peak call files [accepted file format, gff].
    $          -h             help

Do a test run of the script by typing::

    $ perl peak_statistics.pl -i . 

The folder should now contain, a "peak_stats.txt" and a "sample_NoS.gff" file.
This means that script runs fine on your system.


Output
------

Following output files will be generated:

- An output file with  '_NoS.gff' at the end will be generated, for each input. This contains all the non-singelton peaks. (non-singelton peaks are those with standard deviation greater than 0).


- "peak_stats.txt" containing the summary for each input file. The summary includes the following information::

    - Filename
    - Percentage of mapped reads
    - Percentage of uniquely mapped reads
    - Total non-singelton peaks
    - Total singelton peaks
    - Median of tag counts for non-singleton peaks
    - Mean of tag counts for non-singleton peaks
    - Median fuzziness (standard deviation) for non-singleton peaks
    - Mean fuzziness (standard deviation) for non-singleton peaks

 

.. _Perl: http://www.perl.org/
.. _Gff: http://genome.ucsc.edu/FAQ/FAQformat#format3
