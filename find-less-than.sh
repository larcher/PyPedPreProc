#!/bin/bash
# input file is the output from write.table() in R, with one value per line, each line representing a SNP.
# Here we .. 
#   use cat -n to add a line number to each line
#   use tr to strip <CR> and just leave tne \n newlines (in case this file was created on non-Unix, and we forgot to use eol="\n" in the write.table() call
#   use awk to print only the lines where second field is greater than 0 but less than X
#
# usage: find-less-than.sh <threshold> <file>
#    ex: find-less-than.sh 0.5 someoutputfile.out

threshold=$1
file=$2

# Note: the $2 below is part of the awk program, and distinct from the shell
# parameter variable $2 (since it's within single quotes ' ')
cat -n "$file" | tr -d '\r' |  awk '( $2 > 0.0 ) && ( $2 < '$threshold' ) { print }'

# Alternate form, find values greater than a threshold
#cat -n logpvalsOffspring.tsv | tr -d '\r' | awk '$2 > '$threshold' { print }'
