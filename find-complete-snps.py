#!/usr/bin/env python

DATA_FILENAME = "Data_ALL_0s.ped"

import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(msg)s", level=logging.INFO)
logging.info("Hi there.")

import pedparse
      
everybody = pedparse.load_file(DATA_FILENAME, limit_trios=1)

logging.info( "There are %d trios" % len(everybody))

for fam in everybody.values():
    #print "Family ID: %s == %s" % ( everybody[fam].family_id, fam)
    #for snp in xrange(TOTAL_SNPS):
    #    everybody[fam].is_snp_complete(snp)
    #    #print "SNP %d complete? %s" % ( snp, everybody[fam].is_snp_complete(snp))
    #print "Complete SNP data for %d SNPs" % len(filter(lambda x: x, everybody[fam].snp_completeness.values()))
    counts = fam.do_counts()
    counts['family_id'] = fam.family_id
    counts['complete_pct'] = 100.0 * counts['complete'] / pedparse.TOTAL_SNPS
    counts['empty_pct'] = 100.0 * counts['empty'] / pedparse.TOTAL_SNPS
    counts['partial_pct'] = 100.0 * counts['partial'] / pedparse.TOTAL_SNPS
    
    logging.info( "Family ID: %(family_id)s -- Complete SNP data for %(complete)7d SNPs (%(complete_pct)6.2f%%) - Empty SNP data for %(empty)7d SNPs (%(empty_pct)6.2f%%) - Partial SNP data for %(partial)7d SNPs (%(partial_pct)6.2f%%)" % counts)
            
