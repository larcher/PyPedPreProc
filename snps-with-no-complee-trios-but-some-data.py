#!/usr/bin/env python

DATA_FILENAME = "Data_ALL_0s.ped"
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(msg)s", level=logging.INFO)

import pedparse
everybody = pedparse.load_file(DATA_FILENAME)

#snps_with_complete_trios = []
snps_with_no_complete_trios = []

# here, snp's are just line numbers  - they have names, which we can find later in the .map file ... 
for snp in xrange(pedparse.TOTAL_SNPS):
    if snp % 500 == 0:
        logging.debug("Processing SNP # %d" % snp)
    for fam in everybody.values():
        if fam.count_alleles(snp) == 6:
            #snps_with_complete_trios += [snp]
            break
    else:
        # exhausted the family for loop, didn't find any complete trios for
        # the current SNP .. add this one to the "no complete trios" list
        snps_with_no_complete_trios += [snp]

logging.info("Found %d SNPs with NO complete trios" % len(snps_with_no_complete_trios))
logging.info("List of SNPs with NO complete trios: %s" % snps_with_no_complete_trios)

snps_with_no_complete_trios_but_some_data =  snps_with_no_complete_trios[:]

for snp in snps_with_no_complete_trios:
    logging.debug("Processing SNP # %d" % snp)
    for fam in everybody.values():
        if fam.count_alleles(snp) > 0:
            logging.debug("Found data (Family ID %s), skipping to next SNP" % fam.family_id)
            break
    else:
        # exhausted the family for loop, didn't find a single family with at
        # least some data for the current SNP .. so remove this from our list
        # of "SNP's with no complete trios but some data"
        logging.debug("Checked all families, found all 0's, removing SNP")
        snps_with_no_complete_trios_but_some_data.remove(snp)


logging.info("Found %d SNPs with NO complete trios but some data" % len(snps_with_no_complete_trios_but_some_data))
logging.info("List of SNPs with NO complete trios but some data: %s" % snps_with_no_complete_trios_but_some_data)
