#!/usr/bin/env python

DATA_FILENAME = "Data_ALL_0s.ped"
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(msg)s", level=logging.INFO)
logging.info("Hi there.")

import pedparse
#pedparse.IGNORE_FAMILIES = ['SL20051', 'SL21022', 'SL90001', 'SL90004', 'SL90052', 'SL90012', 'SL90014', 'SL90038', 'SL90039', 'SL90119', 'SL90125', 'SL90135', 'SL90136', 'SL90137', 'SL90147', 'SL90150', 'SL90151', 'SL90156', 'SL90157', 'SL90158', 'SL90160', 'SL90161', 'SL90168', 'SL90172', 'SL90174', 'SL90175', 'SL90180', 'SL90181', 'SL90182', 'SL90183', 'SL90185', 'SL90191', 'SL90200', 'SL90201', 'SL90203', 'SL90205', 'SL90209', 'SL90224', 'SL90229', 'SL90231', 'SL90235', 'SL90238', 'SL90239', 'SL90267', 'SL90268', 'SL90269', 'SL90271', 'SL90297', 'SL90303']
everybody = pedparse.load_file(DATA_FILENAME)

snps_with_complete_trios = []
snps_with_no_complete_trios = []

for snp in xrange(pedparse.TOTAL_SNPS):
    if snp % 500 == 0:
        logging.debug("Processing SNP # %d" % snp)
    for fam in everybody.values():
        if fam.count_alleles(snp) == 6:
            snps_with_complete_trios += [snp]
            break
    else:
        # exhausted the family for loop, didn't find any case data .. add this one to the no data list
        snps_with_no_complete_trios += [snp]

logging.info( "found %7d SNPs with data for at least one complete trio case" % len(snps_with_complete_trios))
logging.info( "found %7d SNPs with data for NO complete trios" % len(snps_with_no_complete_trios))
logging.info("SNPs with NO complete trios: %s" % snps_with_no_complete_trios)

