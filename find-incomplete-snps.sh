#!/bin/bash
DATA=Data_ALL_0s.ped
total_snps=237436

#ids=$( cut -d" " -f1 <  $DATA | uniq )
ids="SL90001 SL90004 SL90012 SL90014 SL90038 SL90039 SL90052 SL90119 SL90135 SL90136 SL90137 SL90147 SL90150 SL90151 SL90156 SL90157 SL90160 SL90161 SL90168 SL90172 SL90174 SL90175 SL90180 SL90181 SL90182 SL90183 SL90191 SL90200 SL90201 SL90203 SL90209 SL90224 SL90229 SL90231 SL90235 SL90238 SL90239 SL90267 SL90268 SL90269 SL90271 SL90297 SL90303 SL90108 SL20051 SL20726 SL20210 SL20239 SL90086 SL90085 SL90062 SL90084 SL90082 SL90025 SL90031 SL90045 SL90070 SL90076 SL90034 SL90077 SL20597 SL20670 SL90096 SL90154 SL90125 SL90103 SL90158 SL20258 SL90206 SL90205 SL90169 SL90163 SL90185 SL90177 SL90265 SL90226 SL90246 SL90249 SL90276 SL90241 SL21022 SL20287 SL20282 SL20053 SL20003 SL20009 SL20356 SL20091 SL20127 SL20112 SL20405 SL20383 SL90092 SL90190"

# how mnay initial columns to skip:
base=6
# which SNP to start with:
snp=2

while [ $snp -lt $total_snps ] 
do
    col1=$(( $base + ($snp * 2 ) - 1  ))
    col2=$(( $base + ($snp * 2)  ))
    echo   SNP $snp ------------  columns $col1 and $col2
    complete=0
    for id in $ids ; do
        #echo "SNP $snp for Family ID: $id"
        grep $id $DATA | cut -d" " -f1,$col1,$col2   | grep '\b0\b' > /dev/null 
        if [ $? = 1 ] ; then
            complete=$(( $complete + 1 ))
            echo -n +
        else 
            echo -n -e -
        fi
        #echo "----"
    done
    echo "SNP $snp has $complete complete trios"
    snp=$(( $snp + 1 ))
done

