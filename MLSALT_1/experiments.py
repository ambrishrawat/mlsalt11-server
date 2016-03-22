import wrapper as htk
from utils import *

def exp1():
	##
	pass

def exp2():
	##
	epi_list = 'dev03'
	with open('/home/ar773/MLSALT11/lib/testlists/'+epi_list+'.lst','r') as testlist:
		lattice_list = testlist.readlines()
		lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
		
		for episode in lattice_list:
			save_dir = 'plp-tglm'+str(i+1)
			for i,language_dir in enumerate(lm_list):
				episode = episode.strip()
				htk.lmrescore(episode, language_dir, )
			htk.score(save_dir,epi_list,'rescore')
	pass


def exp3():
	##
	plex = []
	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
	for i,language_dir in enumerate(lm_list):
		plex.append([float(htk.get_plex(language_dir,'Stream/stream_dev03_lm'+str(i+1),'/home/ar773/MLSALT11/lib/texts/dev03.dat'))])
	return plex

def exp4():
	##
	#Lpex
	p = exp3()
	print p
	p = [[float(1/t[0])] for t in p ]	
	s =  sum([t[0] for t in p])
	p = [[float(t[0]/s)] for t in p]
	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
	inter_weights = em(p,'dev03')
	#inter_weights = [t[0] for t in inter_weights]
	htk.lm_merge(lm_list, inter_weights, 'InterpolatedLMs/lmdev03')
	pass	

def exp6_wrapper(episode):
	htk.lm_rescore(episode,'InterpolatedLMs/lmdev03','plps/plp-lmdev03')
	convert('plps/plp-lmdev03/'+episode+'/rescore/rescore.mlf','DATFiles/'+episode+'_lm_dev03.dat')	
	p = []
        lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
        for i,language_dir in enumerate(lm_list):
                p.append([float(htk.get_plex(language_dir,'Stream/stream_'+episode+'_lm'+str(i+1),'/home/ar773/MLSALT11/DATFiles/'+episode+'_lm_dev03.dat'))])
        p = exp3()
        print p
        p = [[float(1/t[0])] for t in p ]
        s =  sum([t[0] for t in p])
        p = [[float(t[0]/s)] for t in p]
        inter_weights = em(p,episode)
	htk.lm_merge(lm_list, inter_weights, 'InterpolatedLMs/lm_'+episode)
	htk.lm_rescore(episode,'InterpolatedLMs/lm_'+episode,'plps/plp-exp6')
def exp6():
	epi_list = 'eval03'
        with open('/home/ar773/MLSALT11/lib/testlists/'+epi_list+'.lst','r') as testlist:
                episodes = testlist.readlines()	
		for episode in episodes:
			episode = episode.strip()
			exp6_wrapper(episode)
		htk.score('plps/plp-exp6',epi_list,'rescore')
if __name__ == "__main__":
	exp6()
	pass
