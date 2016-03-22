class MLF:
	'''
	Class for operating on on MLF files
	'''
	def __init__(self):
		self.mdict = {}

	def getdict(self,dic):
		self.mdict = dic

	def writemlf(self,fout):
		mlfstr = '#!MLF!#\n'
    		def genrow(key):
        		return '{0} {1} {2} {3}'.format(key['tbeg'], entry['tend'], entry['word'], entry['score'])
    		for fkey in self.mdict:
        		mlfstr += entry['name'] + '\n'
        		mlfstr += '\n'.join(map(genrow, self.mdict[fkey])
        		mlfstr += "\n.\n"
    		with open(fout,'w') as mlffile:
			mlffile.write(mlfstr)
	

	def get_word_list(string):
		return re.split(r"_<ALTSTART>_|_<ALT>_|_<ALTEND>", string)[1:-1]

	def gendict(self,addr):
		'''
		creates a dictionary for an MLF file
		Args
			address to the MLF
		Return
			the dictionary
		'''
		mlf = open(addr, 'r')
		lines = mlf.readlines()
		fn = None
		dic = {}
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

		self.mdict = dic
		return dic

	@staticmethod
	def levenshtein(dic1, dic2):
		'''
				
		'''
		def dist(e1, e2):
			'''
			Levenshtein distance
			'''
			if e1 == None or e2 == None:
				return 7
			elif e1['word'] == e2['word']:
				return 0
			else:
				return 10
		nsub, ndel, nins, ntot = 0,0,0,0
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
					#substitutions
					nsub += 1
				else:
					#matches
					ntot += 1
		print ntot, nsub, ndel, nins
	
	@staticmethod
	def merge_mlf(dic1, dic2):
		'''
		take time of mlf2
		'''
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


