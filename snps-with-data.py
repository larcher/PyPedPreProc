#!/usr/bin/env python

DATA_FILENAME = "Data_ALL_0s.ped"
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(msg)s", level=logging.INFO)
logging.info("Hi there.")

import pedparse
everybody = pedparse.load_file(DATA_FILENAME)

snps_with_case_data = []
snps_with_no_case_data = []

for snp in xrange(pedparse.TOTAL_SNPS):
    if snp % 500 == 0:
        logging.debug("Processing SNP # %d" % snp)
    for fam in everybody.values():
        if fam.case.get_snp(snp) != (pedparse.ALLELE_UNKNOWN, pedparse.ALLELE_UNKNOWN):
            snps_with_case_data += [snp]
            break
    else:
        # exhausted the family for loop, didn't find any case data .. add this one to the no data list
        snps_with_no_case_data += [snp]

logging.info( "found %7d SNPs with data for at least one case" % len(snps_with_case_data))
logging.info( "found %7d SNPs with data for NO cases" % len(snps_with_no_case_data))

logging.info("SNPs with NO case data: %s"%  snps_with_no_case_data)
