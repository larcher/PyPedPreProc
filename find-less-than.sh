#!/bin/bash
# input file is the output from write.table() in R, with one value per line, each line representing a SNP.
# Here we .. 
#   use cat -n to add a line number to each line
#   use tr to strip <CR> and just leave tne \n newlines (in case this file was created on non-Unix, and we forgot to use eol="\n" in the write.table() call
#   use awk to print only the lines where second field is greater than 0 but less than X
threshold=$1

cat -n logpvalsOffspring.tsv | tr -d '\r' |  awk '( $2 > 0.0 ) && ( $2 < '$threshold' ) { print }'

# Alternate form, find values greater than a threshold
#cat -n logpvalsOffspring.tsv | awk '$2 > '$threshold' { print }'
