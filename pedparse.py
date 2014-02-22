import logging

TOTAL_SNPS = 237436
SKIP_FIELDS = 6 
#ALLELE_UNKNOWN = "-9"
ALLELE_UNKNOWN = "0"
# skip these family id's because they have incomplete triads (only have data for case and one parent)
IGNORE_FAMILIES = []

# these are families with no complete trios .. usually CASE plus ONE PARENT only
FAMILIES_WITH_NO_COMPLETE_TRIOS = ['SL20051', 'SL21022', 'SL90001', 'SL90004', 'SL90052', 'SL90012', 'SL90014', 'SL90038', 'SL90039', 'SL90119', 'SL90125', 'SL90135', 'SL90136', 'SL90137', 'SL90147', 'SL90150', 'SL90151', 'SL90156', 'SL90157', 'SL90158', 'SL90160', 'SL90161', 'SL90168', 'SL90172', 'SL90174', 'SL90175', 'SL90180', 'SL90181', 'SL90182', 'SL90183', 'SL90185', 'SL90191', 'SL90200', 'SL90201', 'SL90203', 'SL90205', 'SL90209', 'SL90224', 'SL90229', 'SL90231', 'SL90235', 'SL90238', 'SL90239', 'SL90267', 'SL90268', 'SL90269', 'SL90271', 'SL90297', 'SL90303']

class Individual:
    def __init__(self,family_id,fields):
        self.family_id = family_id
        self.meta_data = fields[:SKIP_FIELDS]
        self.alleles =  fields[SKIP_FIELDS:]

    def to_string(self):
        return " ".join( self.meta_data + self.alleles ) + "\n"
    
    def get_snp_str(self,snp):
        return "%s%s" % self.get_snp(snp)
    
    def get_snp(self,snp):
        # SNPs are numbered from 0 .. alleles is a python list, numbered from 1 .. adjustments....
        allele_1 = snp * 2 - 1 - 1
        allele_2 = allele_1 + 1
        return (self.alleles[allele_1], self.alleles[allele_2])

    def clear_snp(self,snp):
        allele_1 = snp * 2 - 1 - 1
        allele_2 = allele_1 + 1
        self.alleles[allele_1] = ALLELE_UNKNOWN
        self.alleles[allele_2] = ALLELE_UNKNOWN
        

    def snp_has_two_alleles(self,snp):
        """ 
        check that a given SNP has two valid alleles (not 0 or -9)
        """
        (a1, a2) = self.get_snp(snp)
        has_data =  a1 != ALLELE_UNKNOWN and a2 != ALLELE_UNKNOWN
        #if not has_data:
            #print self.family_id , self.alleles[allele_1] , self.alleles[allele_2] 
        return has_data

        

class Trio:
    mother = None
    father = None
    case = None
    # TODO idea (not how it's coded now): make  "Completeness" = number of alleles (not 0, -9, unknown) in a snp
    snp_completeness = {}
    
    def __init__(self,family_id):
        self.family_id = family_id
        self.complete_snps = 0
        self.empty_snps = 0
        self.partial_snps = 0
    def add_mother(self,mother):
        self.mother = mother
    def add_father(self,father):
        self.father = father
    def add_case(self,case):
        self.case = case

    def count_alleles(self,snp):
        # Start with 6
        # then subtract the number of ALLELE_UNKNOWN characters in all 6 (2*case + 2*mother + 2*father) slots for alleles
        return 6 - (list(self.case.get_snp(snp)) + list(self.mother.get_snp(snp)) + list(self.father.get_snp(snp))).count(ALLELE_UNKNOWN)

    def clear_snp(self,snp):
        self.case.clear_snp(snp)
        self.father.clear_snp(snp)
        self.mother.clear_snp(snp)
    
    def do_counts(self):
        for snp in xrange(TOTAL_SNPS):
            allele_count = self.count_alleles(snp)
            if allele_count == 6:
                self.complete_snps += 1
            elif allele_count == 0:
                self.empty_snps += 1
            else:
                self.partial_snps += 1
                logging.debug("Family ID %s has Partial SNP %s - Case[%s] Mom[%s] Dad[%s]" % (self.family_id, snp, self.case.get_snp_str(snp), self.mother.get_snp_str(snp), self.father.get_snp_str(snp)))
        return {'complete': self.complete_snps, 'empty': self.empty_snps, 'partial': self.partial_snps}
    
    def count_complete_snps(self):
        return reduce(lambda x,y: x + (1 if self.is_snp_complete(y) else 0), xrange(TOTAL_SNPS), 0)

    def is_snp_complete(self,snp):
        return self.case.snp_has_two_alleles(snp) and self.mother.snp_has_two_alleles(snp) and self.father.snp_has_two_alleles(snp)
        #is_complete = self.case.snp_has_two_alleles(snp) and self.mother.snp_has_two_alleles(snp) and self.father.snp_has_two_alleles(snp)
        ##if is_complete:
        ##    print "SNP %s is complete"
        #self.snp_completeness[snp] = is_complete
        #return is_complete

    def count_partially_complete_snps(self):
        return reduce(lambda x,y: x + (1 if self.is_snp_one_parent_complete(y) else 0), xrange(TOTAL_SNPS), 0)

    def is_snp_one_parent_complete(self,snp):
        return self.case.snp_has_two_alleles(snp) and (self.mother.snp_has_two_alleles(snp) or self.father.snp_has_two_alleles(snp))


def load_file(filename, limit_trios=None):
    everybody = {} 
    with open(filename) as f:
        logging.info( "loading file %s" % filename)
        #for n in [1,2,3]:
        #    line = f.readline()
        for line in f:
            line = line.strip()
            fields = line.split(" ")
            family_id = fields[0]
            logging.debug("Read line for family id %s" % family_id)
            #print "Family ID: %s" % family_id 
            if family_id in IGNORE_FAMILIES:
                logging.debug("Family ID %s marked as ignored, skipping." % family_id)
                continue

            #this_person = Individual(family_id, fields[SKIP_FIELDS:])
            this_person = Individual(family_id, fields)

            if not everybody.has_key(family_id):
                everybody[family_id] = Trio(family_id)
            if 'father' in fields[1]:
                everybody[family_id].add_father(this_person)
            if 'mother' in fields[1]:
                everybody[family_id].add_mother(this_person)
            if 'proband' in fields[1]:
                everybody[family_id].add_case(this_person)
            if not ( everybody[family_id].mother is None or everybody[family_id].case is None or everybody[family_id].father is None ):
                if limit_trios and len(everybody) == limit_trios:
                    break
        
        logging.info( "File %s loaded - There are %d trios" % (filename, len(everybody)))
    return everybody
