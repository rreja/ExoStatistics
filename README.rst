Peak Statistics
================

Introduction
-------------

The script in this repository can be used to perform some basic statistics
on the peak call file.


Requirements
------------

- The software requires only Perl_ (5 or higher) to run.
- The input file should be in standard Gff_ format

Installation
------------

Unpack the source code archive. The folder contains the followng

- `peak_statistics.pl`: Script for basic statistics when running on a single file
- `peak_statistics_batch.sh` : Script for batch processing
- 'README.rst` : Readme file
- `sample.gff`: The sample input file to test the scripts.

When running the script on a single input gff file:

- open the file `peak_statistics.pl` in  any text editor of your choice.
- Comment out the line 18 by putting a "#" in front of it.
- Uncomment the lines 21 and 22 by removing the "#" in front of them.
- You are ready to use the file. How to run the script from your terminal?

- Type the following:

    $ perl peak_statistics.pl <path_to_your_input_file>
    $ # for example peak_statistics.pl /Users/input/sample.gff


.. _Perl: http://www.perl.org/
.. _Gff: http://genome.ucsc.edu/FAQ/FAQformat#format3
