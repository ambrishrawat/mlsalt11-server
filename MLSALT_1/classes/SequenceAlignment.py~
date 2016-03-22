import operator
class SequenceAlignment:
	"""
	Class for sequence alignment
	"""
	def __init_(self):
		self.A = {}
		self.A_loc = {}
		
		pass



	@staticmethod
	def dp():
		pass
	@staticmethod
	def align(seq1,seq2,dist):
		#initialise a dictionary of A(i,j) 
		A = {}
		#gpenalty is essentially distanec between an element and None
		A[(0,0)] = 0
		for i in range(0,len(seq1)):
			A[(i+1,0)]= (i+1)*dist(seq1[i],None)
			
		for j in range(0,len(seq2)):
			A[(0,j+1)]= (j+1)*dist(None,seq2[j])

		
		A_loc = {}

		#compute the optimal alignment cost
		for i in range(0,len(seq1)):
			for j in range(0,len(seq2)):
				options  = [dist(seq1[i],seq2[j])+A[(i,j)],\
					dist(seq1[i],None) + A[(i,j+1)],\
					dist(None,seq2[j]) + A[(i+1,j)]]
				A_loc[(i+1,j+1)], A[(i+1,j+1)] = min(enumerate(options),key=operator.itemgetter(1))
		
		#required because of the boundary conditions
		for i in range(0,len(seq1)):
			A_loc[(i+1,0)]= 1
			
		for j in range(0,len(seq2)):
			A_loc[(0,j+1)]= 2
				
		
		alignpair = []
		i,j = len(seq1),len(seq2)
		
		while i > 0 or j > 0:
			if A_loc[(i,j)] == 1:
				alignpair.append((i-1,None))
				i = i - 1
				
			elif A_loc[(i,j)] == 2:
				alignpair.append((None,j-1))
				j = j - 1
			elif A_loc[(i,j)] == 0:
				alignpair.append((i-1,j-1))
				i = i - 1
				j = j - 1
				
		
		return reversed(alignpair)	

	@staticmethod
	def multialign(seqlist,dist):
		#initialise a dictionary of A(i,j) 
		A = {}
		#gpenalty is essentially distanec between an element and None
		alist = list(itertools.product(*seqlist))
				
		A[(0,0)] = 0
		for i in range(0,len(seq1)):
			A[(i+1,0)]= (i+1)*dist(seq1[i],None)
			
		for j in range(0,len(seq2)):
			A[(0,j+1)]= (j+1)*dist(None,seq2[j])

		
		A_loc = {}

		#compute the optimal alignment cost
		for i in range(0,len(seq1)):
			for j in range(0,len(seq2)):
				options  = [dist(seq1[i],seq2[j])+A[(i,j)],\
					dist(seq1[i],None) + A[(i,j+1)],\
					dist(None,seq2[j]) + A[(i+1,j)]]
				A_loc[(i+1,j+1)], A[(i+1,j+1)] = min(enumerate(options),key=operator.itemgetter(1))
		
		#required because of the boundary conditions
		for i in range(0,len(seq1)):
			A_loc[(i+1,0)]= 1
			
		for j in range(0,len(seq2)):
			A_loc[(0,j+1)]= 2
				
		
		alignpair = []
		i,j = len(seq1),len(seq2)
		
		while i > 0 or j > 0:
			if A_loc[(i,j)] == 1:
				alignpair.append((i-1,None))
				i = i - 1
				
			elif A_loc[(i,j)] == 2:
				alignpair.append((None,j-1))
				j = j - 1
			elif A_loc[(i,j)] == 0:
				alignpair.append((i-1,j-1))
				i = i - 1
				j = j - 1
				
		
		return reversed(alignpair)	


def dist(e1, e2):							
	if e1 == None or e2 == None:
		return 0
	elif e1 == e2:
		return -1
	else:
		return 1			
	
if __name__ == '__main__':
	
	seq1 = "axdf"
	seq2 = "extg"

	
	alignpair = SequenceAlignment.align(seq1,seq2,dist)
	
	seq1_print = ''
	seq2_print = ''
	for a in alignpair:
		if a[0] is None and a[1] is not None:
			seq1_print = seq1_print + ' '
			seq2_print = seq2_print + seq2[a[1]]
		if a[0] is not None and a[1] is None:
			seq1_print = seq1_print + seq1[a[0]]
			seq2_print = seq2_print + ' '
		if a[0] is not None and a[1] is not None:
			seq1_print = seq1_print + seq1[a[0]]
			seq2_print = seq2_print + seq2[a[1]]

	print seq1_print
	print seq2_print
