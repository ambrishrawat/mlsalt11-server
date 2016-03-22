class ConfNet:
	'''
	Class for operating on on Confusion Network files
	'''
	def __init__(self):
		self.cfnw_dict = {}

	def getdict(self,dic):
		self.mdict = dic


	def gendict(lataddr):
		
		diclist = []
		with gzip.open(dicaddr,'rb') as dicfile:
		flist= dicfile.readlines()
	flist = [f.strip().split() for f in flist]
	for f in flist[1:]:
		if len(f) == 4:
			tbeg = f[1][2:]
			tend = f[2][2:]
			word = f[][]
			score = 
			tempdict = {'t}
		
		
	return

def gencncdict_old(lataddr):

	files = [f for f in listdir(lataddr) if isfile(join(lataddr, f))]
	latdict = {}
	for faddr in files:
		diclist = []
		with gzip.open(lataddr+'/'+faddr,'rb') as dicfile:
			flist= dicfile.readlines()
		flist = [f.strip().split() for f in flist]
		nnodes = int(flist[0][0][2:])
		fcount = 1
		nodedict = {}
		for i in range(nnodes):

			karcs = int(flist[fcount][0][2:])
			arccount = 1
			arcdict = {}

			fcount += 1
			nodetbeg = float(flist[fcount][1][2:])
			nodetend = float(flist[fcount][2][2:])
			while arccount <= karcs:
				if float(flist[fcount][1][2:]) < nodetbeg:
					nodetbeg = flist[fcount][1][2:] 
				if float(flist[fcount][2][2:]) > nodetend:
					nodetend = flist[fcount][2][2:] 
				arcdict[flist[fcount][0][2:]] = flist[fcount][3][2:]
				fcount+=1
				arccount+=1
			
			nodedict[(nodetbeg,nodetend)] = arcdict	
		latdict[faddr] = nodedict
	return latdict

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
					nodetbeg = flist[fcount][1][2:] 
				if float(flist[fcount][2][2:]) > nodetend:
					nodetend = flist[fcount][2][2:] 
				wordlist.append(flist[fcount][0][2:]) 
				scorelist.append(flist[fcount][3][2:])
				fcount+=1
				arccount+=1
			nodedict = {'tbeg': nodetbeg,'tend': nodetend, 'word': wordlist, 'score': scorelist}
			nodedictlist.append(nodedict)	
		latdict[faddr] = nodedictlist
	return latdict






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
	



