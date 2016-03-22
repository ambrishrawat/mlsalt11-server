#!/bin/bash

#$ -S /bin/bash

base/bin/HLEd -A -D -V -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/adapt.mlf -l '*' -X rec lib/edfiles/delsil.led plp/am/plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0//rescore.mlf  > plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/LOG.hled

# some MLF labels  may not exist - generate the list of files that have MLF entries
./scripts/mlf2scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/adapt.mlf lib/flists/dev03_DEV001-20010117-XX2000.scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/flists/dev03_DEV001-20010117-XX2000.scp

base/bin/HVite -A -D -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/model.mlf -H hmms/MMF.plp -T 1 -C lib/cfgs/hvite.cfg -y lab -X rec -t 250.0 250.0 1000.1 \
-b \<s\> -a -m -I plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/adapt.mlf -S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/flists/dev03_DEV001-20010117-XX2000.scp lib/dicts/train.hv.dct hmms/xwrd.clustered.plp >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/LOG.align

base/bin/HERest -A -D -H hmms/MMF.plp -T 1 -C lib/cfgs/hvite.cfg -t 250.0 250.0 1000.1 \
-J lib/classes -C lib/cfgs/cmllr.cfg -h "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%_*" -K plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/xforms cmllr \
-u a -I plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/model.mlf  -S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/flists/dev03_DEV001-20010117-XX2000.scp hmms/xwrd.clustered.plp >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/LOG.cmllr

base/bin/HERest -A -D -H hmms/MMF.plp -T 1 -C lib/cfgs/hvite.cfg -t 250.0 250.0 1000.1 \
-a -J plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/xforms cmllr -E plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/xforms cmllr \
-J lib/classes -C lib/cfgs/mllr.cfg -h "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%_*" -K plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/xforms mllr \
-u a -I plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/model.mlf  -S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/flists/dev03_DEV001-20010117-XX2000.scp hmms/xwrd.clustered.plp >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/adapt/LOG.mllr 

