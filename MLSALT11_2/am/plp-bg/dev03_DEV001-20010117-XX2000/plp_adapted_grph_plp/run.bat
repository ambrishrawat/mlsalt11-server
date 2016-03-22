#!/bin/bash

#$ -S /bin/bash

source  /opt/intel/composerxe/bin/compilervars.sh intel64

# some lattices may not exist - generate the list of lattices to avoid HDecode crashing
 ./scripts/lats2scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/merge/lattices lib/flists/dev03_DEV001-20010117-XX2000.scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/plp_adapted_grph_plp/flists/dev03_DEV001-20010117-XX2000.scp

# run the decoding making use of the adaptation transforms
base/bin/HDecode -A -D -V -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/plp_adapted_grph_plp/rescore.mlf -H hmms/MMF.plp -s 12.0 -p -10.0  \
    -X rec -T 1 -t 250.0 250.0 -v 175.0 135.0 -u 10000 -n 32 -m -J plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-adapt/xforms mllr -J lib/classes -C lib/cfgs/cmllr.cfg \
    -z lat -l plp/am/plp-bg/dev03_DEV001-20010117-XX2000/plp_adapted_grph_plp/lattices  -h "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%_*" \
    -C lib/cfgs/hdecode.cfg -X lat -w -L plp/am/plp-bg/dev03_DEV001-20010117-XX2000/merge/lattices -S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/plp_adapted_grph_plp/flists/dev03_DEV001-20010117-XX2000.scp lib/dicts/train.lv.dct hmms/xwrd.clustered.plp >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/plp_adapted_grph_plp/LOG
