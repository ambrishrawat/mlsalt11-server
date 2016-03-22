import HTK_scripts as htk
import numpy as np
import os
import re
from SequenceAlignment import SequenceAlignment
import gzip
from os import listdir
from os.path import isfile, join
import numpy
import operator
def convert(mlf, dest):
	'''
	converts mlf file to .dat file
	e.g.
	mlf = 'plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0/rescore.mlf'
	out = 'answer.dat'
	'''
	mlf = open(mlf, 'r')
	dest = open(dest, 'w')
	lines = mlf.readlines()
	transcript = []
	for i in range(2,len(lines)):
		line = lines[i].split()
		if line[0] == '.':
			dest.write('<s> ' + ' '.join(transcript) + ' </s>\n')
			transcript = []
		else:
			if len(line) > 1:
				transcript.append(line[2])


#exp 4
def LM_interpolation(dat_file, fout_path):
	'''
	e.g. dat_file: lib/texts/dev03.dat

	'''
	#generate streams and get perplexity values to initialise LM weights
	lms = ['lms/lm1', 'lms/lm2', 'lms/lm3', 'lms/lm4','lms/lm5']
	pplex = []
	for i,lm in enumerate(lms):
		perplexity = htk.get_plex(lm, 'temp_streams/stream_'+str(1+i), dat_file)
		pplex.append(float(perplexity))
	pplex = np.array(pplex)

	P = np.matrix(np.loadtxt('temp_streams/stream_1'))
	for i in range(2,6):
		P = np.vstack((P, np.loadtxt('temp_streams/stream_' + str(i))))

	lamda, lamda_ = np.ones(5),np.ones(5)
	lamda = (lamda/pplex)
	lamda = lamda/np.sum(lamda)

	j = 0
	while np.linalg.norm(lamda_ - lamda) > 0.00001:
		#print np.linalg.norm(lamda_ - lamda)
		j +=1
		lamda = lamda_
		#E step
		lamda_ = [np.sum((lamda[i]*P[i])/(lamda*P)) for i in range(5)]
		#M step
		lamda_ = lamda_/np.sum(lamda_)

	#for l in lamda_:
	#	fout.write(str(l) + '\n')

	os.system('base/bin/LMerge -C lib/cfgs/hlm.cfg -i ' +str(lamda_[1])+' lms/lm2 -i '+str(lamda_[2])+' lms/lm3 -i '+str(lamda_[3])+' lms/lm4 -i '+str(lamda_[4])+' lms/lm5 lib/wlists/train.lst lms/lm1 '+ fout_path)

	#print perplexity of model
	perplexity = htk.get_plex(fout_path, 'temp_streams/stream', dat_file)
	print "Perplexity: ", perplexity
	os.system('rm -r temp_streams/stream_*')

	#return language model weights
	return lamda_

def generate_dic(mlf):
	mlf = open(mlf, 'r')
	lines = mlf.readlines()
	dic = {}
	fn = None
	for i in range(1,len(lines)):
		line = lines[i].split()
		if len(line) == 1:
			if line[0] != '.':
				key = line[0].split('/')[-1].strip("\"")
				dic[key] = []
				fn = key
		else:
			dic[fn].append(line[2])

	return dic

def generate_dic_time(mlf):
	mlf = open(mlf, 'r')
	lines = mlf.readlines()
	dic = {}
	fn = None
	for i in range(1,len(lines)):
		line = lines[i].split()
		if len(line) == 1:
			if line[0] != '.':
				key = line[0].split('/')[-1].strip("\"")
				dic[key] = []
				fn = key
		else:
			temp = {'tbeg': float(line[0]), 'tend': float(line[1]), 'word': line[2], 'score': line[3]}
			dic[fn].append(temp)

	return dic

def dist(e1, e2):
	'''
	Levenshtein distance
	(exp 1 - system combination)
	'''
	if e1 == None or e2 == None:
		return 7
	elif e1 == e2:
		return 0
	else:
		return 10

def dist_time(e1,e2):
	'''
	combination of ROVER systems- considering time
	'''
	
	if e1 == None or e2 == None:
		return 7
	else:
		frac = min(e1['tend'], e2['tend']) - max(e1['tbeg'], e2['tbeg'])
		dur = min(e1['tend'] - e1['tbeg'], e2['tend'] - e2['tbeg'])
		frac = frac/dur
		if frac > 0.5 and e1['word'] == e2['word']:
			return 0
		else:
			return 10



def edit_distance(mlf1, mlf2):
	#D=77, S=522, I=67
	dic1 = generate_dic(mlf1)
	dic2 = generate_dic(mlf2)
	nsub, ndel, nins = 0,0,0

	for file in set(dic1.keys()+dic2.keys()):
		l1 = dic1[file]
		l2 = dic2[file]
		sa = SequenceAlignment.align(l1,l2,dist)
		for i in sa:
			if i[0] is None and i[1] is not None:
				#insertion
				nins +=1
			elif i[1] is None and i[0] is not None:
				#deletion
				ndel +=1
			elif l1[i[0]] != l2[i[1]]:
				nsub += 1
	print nsub, ndel, nins



def merge_mlf(mlf1, mlf2):
	'''
	take time of mlf2
	'''
	dic1 = generate_dic_time(mlf1)
	dic2 = generate_dic_time(mlf2)
	mlf3 = {}
	for file in set(dic1.keys()+dic2.keys()):
		temp = []
		l1 = dic1[file]
		l2 = dic2[file]
		sa = SequenceAlignment.align(l1,l2,dist_time)
		for i in sa:
			if i[0] is None and i[1] is not None:
				#insertion
				tbeg = l2[i[1]]['tbeg']
				score = l2[i[1]]['score'] +'_0.2'
				word = l2[i[1]]['word']+ '_<ALTSTART>_<DEL>_<ALTEND>'
				tend = l2[i[1]]['tend']
				tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
				temp.append(tdic)

			elif i[1] is None and i[0] is not None:
				#deletion
				tbeg = l1[i[0]]['tbeg']
				l1[i[0]]['tbeg'] = tbeg
				score = l1[i[0]]['score'] +'_0.2'
				word = l1[i[0]]['word']+ '_<ALTSTART>_<DEL>_<ALTEND>'
				tend = l1[i[0]]['tend']
				tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
				temp.append(tdic)

			elif l1[i[0]]['word'] == l2[i[1]]['word']:
				tbeg = l2[i[1]]['tbeg']
				tend = l2[i[1]]['tend']
				score = str( 0.5*float(l1[i[0]]['score']) + 0.5*float(l2[i[1]]['score']))
				tdic = {'tbeg': tbeg, 'tend': tend, 'word': l1[i[0]]['word'], 'score': score}
				temp.append(tdic)
			else:
				#substitution
				tbeg = l2[i[1]]['tbeg']
				tend = l2[i[1]]['tend']
				score = l1[i[0]]['score'] +'_'+ l2[i[1]]['score']
				word = l1[i[0]]['word'] + '_<ALTSTART>_' + l2[i[1]]['word'] +'_<ALTEND>'
				tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
				temp.append(tdic)


			mlf3[file] = temp
	return mlf3

def write_mlf(mlf_dic, episode, parent_dir, mlf_pass, fout):
	fout = open(fout,'w')
	fout.write('#!MLF!#\n')
	#temp = '"'+ parent_dir +'/' + episode + '/' + mlf_pass +'lattices/'

	for file,farr in mlf_dic.items():
		fout.write('"' + file +'"\n')
		for f in farr:
			temp = str(f['tbeg']) + ' ' + str(f['tend']) + ' ' + f['word'] + ' ' + str(f['score']) + '\n'
			fout.write(temp)
		fout.write('.\n')



def gencncdict(lataddr):

	files = [f for f in listdir(lataddr) if isfile(join(lataddr, f))]
	latdict = {}
	for faddr in files:
		
		with gzip.open(lataddr+'/'+faddr,'rb') as dicfile:
			flist= dicfile.readlines()
		flist = [f.strip().split() for f in flist]
		nnodes = int(flist[0][0][2:])
		fcount = 1
		nodedictlist = []
		for i in range(nnodes):

			karcs = int(flist[fcount][0][2:])
			arccount = 1
			
			fcount += 1
			nodetbeg = float(flist[fcount][1][2:])
			nodetend = float(flist[fcount][2][2:])
			wordlist = []
			scorelist = []
			while arccount <= karcs:
				if float(flist[fcount][1][2:]) < nodetbeg:
					nodetbeg = float(flist[fcount][1][2:]) 
				if float(flist[fcount][2][2:]) > nodetend:
					nodetend = float(flist[fcount][2][2:]) 
				wordlist.append(flist[fcount][0][2:]) 
				scorelist.append(flist[fcount][3][2:])
				fcount+=1
				arccount+=1
			nodedict = {'tbeg': nodetbeg,'tend': nodetend, 'word': wordlist, 'score': scorelist}
			nodedictlist.append(nodedict)	
		latdict[faddr] = nodedictlist
	return latdict


def dist_cnc(e1,e2):
	'''
	combination of Confusion Networks systems- considering time
	'''
	
	if e1 == None or e2 == None:
		return 7
	else:
		frac = min(e1['tend'], e2['tend']) - max(e1['tbeg'], e2['tbeg'])
		dur = min(e1['tend'] - e1['tbeg'], e2['tend'] - e2['tbeg'])
		frac = frac/dur
		
		sc1_idx = [e1['score'][sc] for sc in list(numpy.nonzero(numpy.in1d(e1['word'],e2['word']))[0])]
		sc2_idx = [e2['score'][sc] for sc in list(numpy.nonzero(numpy.in1d(e2['word'],e1['word']))[0])]
		
		if frac > 0.5:
			return 0
		else:
			return 10

def cnc_combine(cnc1,cnc2):
	dic1 = gencncdict(cnc1)
	dic2 = gencncdict(cnc2)
	mlf3 = {}
	for f in set(dic1.keys()+dic2.keys()):
		temp = []
		l1 = dic1[f]
		l2 = dic2[f]
		sa = SequenceAlignment.align(l1,l2,dist_cnc)
		for i in sa:
			if i[0] is None and i[1] is not None:
				#insertion
				tbeg = str(int(l2[i[1]]['tbeg']*1e7))
				idx,score = max(enumerate(map(float,l2[i[1]]['score'])),key=operator.itemgetter(1))
				score = str(score)
				word = l2[i[1]]['word'][idx]
				tend = str(int(l2[i[1]]['tend']*1e7))
				if word not in ['!NULL','<s>','</s>']: 
					tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
					temp.append(tdic)

			elif i[1] is None and i[0] is not None:
				#deletion
				tbeg = str(int(l1[i[0]]['tbeg']*1e7))
				idx,score = max(enumerate(map(float,l1[i[0]]['score'])),key=operator.itemgetter(1))
				score = str(score)
				word = l1[i[0]]['word'][idx]
				tend = str(int(l1[i[0]]['tend']*1e7))
				if word not in ['!NULL','<s>','</s>']: 
					tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
					temp.append(tdic)

			elif dist_cnc(l1[i[0]],l2[i[1]]) == 0:
				tbeg = str(int(l2[i[1]]['tbeg']*1e7))
				tend = str(int(l2[i[1]]['tend']*1e7))

				idx1,score1 = max(enumerate(map(float,l1[i[0]]['score'])),key=operator.itemgetter(1))
				idx2,score2 = max(enumerate(map(float,l2[i[1]]['score'])),key=operator.itemgetter(1))
				
				score = ''
				word = ''
			
				if score1 > score2:
					score = str(score1)
					word = l1[i[0]]['word'][idx1]
				else:
					score = str(score2)
					word = l2[i[1]]['word'][idx2]
				if word not in ['!NULL','<s>','</s>']: 
					tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
					temp.append(tdic)
			else:
				tbeg = str(int(l2[i[1]]['tbeg']*1e7))
				tend = str(int(l2[i[1]]['tend']*1e7))
				idx1,score1 = max(enumerate(map(float,l1[i[0]]['score'])),key=operator.itemgetter(1))
				idx2,score2 = max(enumerate(map(float,l2[i[1]]['score'])),key=operator.itemgetter(1))
				
				score = ''
				word = ''
			
				if score1 > score2:
					score = str(int(score1*1e7))
					word = l1[i[0]]['word'][idx1]
				else:
					score = str(int(score2*1e7))
					word = l2[i[1]]['word'][idx2]
				if word not in ['!NULL','<s>','</s>']: 
					tdic = {'tbeg': tbeg, 'tend': tend, 'word': word, 'score': score}
					temp.append(tdic)

			mlf3[f[:-7]+'.rec'] = sorted(temp,key=lambda x:int(x['tbeg']))
	return mlf3
	pass	

if __name__ == '__main__':
	#LM_interpolation('lib/texts/dev03.dat', 'test')
	#mlf = 'plp/am/plp-bg/dev03_DEV001-20010117-XX2000/1best/LM12.0_IN-10.0/rescore.mlf'
	#edit_distance(mlf,mlf)
	cnc1 = 'plp/am/plp-bg/dev03_DEV001-20010117-XX2000/plp-decode_cn/lattices/'
	cnc2 = 'plp/am/plp-bg/dev03_DEV001-20010117-XX2000/grph-plp-decode_cn/lattices/'
	cnc_combine(cnc1,cnc2)


















