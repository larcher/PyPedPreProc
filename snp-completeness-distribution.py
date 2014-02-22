#!/usr/bin/env python

# Given:  new zeroed out data set (where 
#    
# We want to know:
#  how many SNPs have N complete trios
#  where 
#    - N is [0-45] 
#    - a "SNP with Complete Trio" = SNP has all 6 alleles for a given family
#  IOW: histogram with # of trios on the X-axis (0 to 45) and # of SNPs on the Y-axis
# 
# Sanity Checks:
#   - there should be 158 +  12 SNPs with 0 complete trios
#   - running this with all data sets should give same results  (including both the 45-family sets and the 94-family sets)

DATA_FILENAME = "Data_ALL_0s.ped"
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(msg)s", level=logging.INFO)

import pedparse
everybody = pedparse.load_file(DATA_FILENAME)

# initialize a list with buckets for 0 to N
# where N is the total number of trios ... 
# OR  
#complete_trio_buckets = [0] * (len(everybody) + 1)
# N is ttotal number of tros minus the number of known incomplete trios 
complete_trio_buckets = [0] * (len(everybody) - len(pedparse.FAMILIES_WITH_NO_COMPLETE_TRIOS) + 1)
# "+ 1" is for the 0-bucket

try:
    for snp in xrange(pedparse.TOTAL_SNPS):
        complete_trios = 0
        for fam in everybody.values():
            if fam.count_alleles(snp) == 6:
                complete_trios += 1
        complete_trio_buckets[complete_trios] += 1
except KeyboardInterrupt:
    print "OK - stopping at SNP # %d" % snp
    print

for num_trios, snp_count in enumerate(complete_trio_buckets):
    print "SNPs with %d complete trios: %d" % (num_trios, snp_count)
     
            
