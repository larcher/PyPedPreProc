#!/usr/bin/env python

#Zero out everything that's not a complete trio 

DATA_FILENAME = "Data_ALL_0s.ped"
import logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(msg)s", level=logging.INFO)

import pedparse

# Good start: remove the 49 families which have no SNPs with complete trios
pedparse.IGNORE_FAMILIES = pedparse.FAMILIES_WITH_NO_COMPLETE_TRIOS 

everybody = pedparse.load_file(DATA_FILENAME)


#with the remaining 45 families
with open("newped","w") as new_file:
    for fam in everybody.values():
        for snp in xrange(pedparse.TOTAL_SNPS):
            if fam.count_alleles(snp) < 6: 
                #zero out that whole trio for that SNP
                fam.clear_snp(snp)
        # write the family out to the new file ... maybe one line at a time
        new_file.write( fam.case.to_string() ) 
        new_file.write( fam.father.to_string() ) 
        new_file.write( fam.mother.to_string() ) 



