#!/bin/bash

#$ -S /bin/bash

# some lattices may not exist - generate the list of lattices to avoid HDecode crashing
 ./scripts/lats2scp lattices/dev03_DEV001-20010117-XX2000/decode/lattices lib/flists/dev03_DEV001-20010117-XX2000.scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0/flists/dev03_DEV001-20010117-XX2000.scp

# run the lattice rescoring
base/bin/HLRescore -A -D -V -T 7 -C lib/cfgs/hlrescore.cfg -f \
-s 12.0 -p -10.0 -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0/rescore.mlf -L lattices/dev03_DEV001-20010117-XX2000/decode/lattices \
-S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0/flists/dev03_DEV001-20010117-XX2000.scp lib/dicts/train.lv.dct >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0/LOG

