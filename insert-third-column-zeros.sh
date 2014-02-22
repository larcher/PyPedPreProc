#!/bin/bash
# this will create a new column of 0's, after the existing 2nd column
# run like this: insert-third-column-zeros Data_ALL.map > Data_ALL_new.map
cat $1 |  awk  '{ print $1" "$2" 0 "$3 }' 
