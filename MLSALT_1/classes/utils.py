import os
import numpy as np
import scipy as sc
import xml.etree.ElementTree as et
import xml.dom.minidom as minidom

def em(l_old,episode):
	#l_old = np.matrix([[0.0],[0.0],[0.0],[0.0],[0.0]])
	s = np.matrix((np.loadtxt('./Stream/stream_'+episode+'_lm1')))
	for i in range(4):
		s = np.vstack((s,np.loadtxt('./Stream/stream_'+episode+'_lm'+str(i+2)+'')))
	
	l_new = np.matrix([[0.2],[0.2],[0.2],[0.2],[0.2]])

	thresh = 0.001

	while np.linalg.norm(l_old-l_new)>thresh:
	
		l_old = l_new
		#e-step
		l_temp = [np.sum(np.divide(np.matrix(l_old[i]*s[i]),l_old.T*s)) for i in range(5)]

		#m-step
		l_new = l_temp/np.sum(l_temp)

	return l_new
	pass

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
	

