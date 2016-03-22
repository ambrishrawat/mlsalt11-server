#!/bin/bash

#$ -S /bin/bash

base/bin/HLConf -A -D -V -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/lattices.mlf -C lib/cfgs/hlconf.cfg -T 1 \
-a 0.083333 -s 1.0 -r 1.0 -p 0.0 -z -Z -l plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/lattices \
-S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/lattices.scp lib/dicts/train.lv.dct >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/LOG

base/bin/HLEd -A -D -V -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/align.mlf -l '*' -X rec lib/edfiles/delsil.led plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/lattices.mlf  > plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/LOG.hled

# some MLF labels  may not exist - generate the list of files that have MLF entries
./scripts/mlf2scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/align.mlf lib/flists/dev03_DEV001-20010117-XX2000.scp plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/flists/dev03_DEV001-20010117-XX2000.scp

base/bin/HVite -A -D -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/time+sil.mlf -H hmms/MMF.plp -T 1 -C lib/cfgs/hvite.cfg \
-X rec -t 250.0 250.0 1000.1 \
-b \<s\> -a -I plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/align.mlf -S plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/flists/dev03_DEV001-20010117-XX2000.scp lib/dicts/train.hv.dct hmms/xwrd.clustered.plp >& plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/LOG.align

base/bin/HLEd -A -D -V -i plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/time.mlf -l '*' -X rec lib/edfiles/delsil.led plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/time+sil.mlf  > plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/LOG.hled2

paste plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/time.mlf plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/align.mlf | awk '{if (NF>2) {printf("%d %d %s %f\n",$1,$2,$3,$NF)} else {print $2}}' > plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/rescore.mlf

