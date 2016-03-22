#!/bin/bash

#$ -S /bin/bash

# some lattices may not exist - generate the list of lattices to avoid HLRescore crashing
 ./scripts/lats2scp lattices/dev03_DEV001-20010117-XX2000/decode/lattices lib/flists/dev03_DEV001-20010117-XX2000.scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/merge/flists/dev03_DEV001-20010117-XX2000.scp

# some lattices may not exist - generate the list of lattices to avoid HLRescore crashing
base/bin/HLRescore -A -D -V -T 7 -C lib/cfgs/hlrescore.cfg -w -q tvaldm -m f \
-t 100.0 200.0 \
-s 12.0 -p -10.0 -l plp/am/plp-bg/dev03_DEV001-20010117-XX2000/merge/lattices \
-L lattices/dev03_DEV001-20010117-XX2000/decode/lattices \
-S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/merge/flists/dev03_DEV001-20010117-XX2000.scp lib/dicts/train.lv.dct >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/merge/LOG

