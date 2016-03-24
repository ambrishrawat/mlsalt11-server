import classes.wrapper as htk
from classes.utils import *
from classes.MLF import MLF
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

def exp_mlf():
	mlf1_addr = './models/dev03_DEV001-20010117-XX2000/plp-decode/rescore.mlf'
	mlf1 = MLF()
	mlf1.gendict(mlf1_addr)

	mlf2_addr = './models/dev03_DEV001-20010117-XX2000/grph-plp-decode/rescore.mlf'
	mlf2 = MLF()
	mlf2.gendict(mlf2_addr)

	MLF.levenshtein(mlf1.return_dict(),mlf2.return_dict())

	mlf3 = MLF()
	mlf3.assign_dict(MLF.merge_mlf(mlf1,mlf2))
	pass


def step1():
	'''
	Generate the interpolated language model on YouTube devlopment set (Training YTBEdev)
	'''
	parent_dir = 'model/'
	epi_list = 'YTBEdev'

	'''
	rescore the available plp-bg lattice (bigram l.m. scores) with the 5 trigram l.m. scores
	'''
	with open('/home/ar773/MLSALT11/lib/testlists/'+epi_list+'.lst','r') as testlist:
		lattice_list = testlist.readlines()
		lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
		
		for episode in lattice_list:
			save_dir = parent_dir  + 'plp-tglm'+str(i+1)
			for i,language_dir in enumerate(lm_list):
				episode = episode.strip()
				htk.lmrescore(episode, language_dir, )
			htk.score(save_dir,epi_list,'rescore')
	


	'''
	generate the probability stream for the vocabulary
	'''
	plex = []
	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
	for i,language_dir in enumerate(lm_list):
		plex.append([float(htk.get_plex(language_dir,'Stream/stream_'+epi_list+'_lm'+str(i+1),'/home/ar773/MLSALT11/lib/texts/YTBEdev.dat'))])

	'''
	get interpolatiom weights for the 5 language models (expectation maximization)
	'''
	p = plex
	p = [[float(1/t[0])] for t in p ]	
	s =  sum([t[0] for t in p])
	p = [[float(t[0]/s)] for t in p]
	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
	inter_weights = em(p,epi_list)
	#inter_weights = [t[0] for t in inter_weights]


	'''
	generate the interpolated language model (lmmerge)
	'''
	htk.lm_merge(lm_list, inter_weights, 'InterpolatedLMs/lm'+epi_list)
	pass


def step2():
	'''
	Generate episode specific interpolated language models and get the updated lattices
	'''
	parent_dir = 'model/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:

		htk.lm_rescore(episode,'InterpolatedLMs/lm'+epi_list_tag,'./models','lm_inter_rescore')
		convert('models/plp-lmYTBEdev/'+episode+'/rescore/rescore.mlf','DATFiles/'+episode+'_lm_'++'.dat')	
		p = []
        lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
        for i,language_dir in enumerate(lm_list):
                p.append([float(htk.get_plex(language_dir,'Stream/stream_'+episode+'_lm'+str(i+1),'/home/ar773/MLSALT11/DATFiles/'+episode+'_lm_YTBEdev.dat'))])
        
		
        p = [[float(1/t[0])] for t in p ]
        s =  sum([t[0] for t in p])
        p = [[float(t[0]/s)] for t in p]
        inter_weights = em(p,episode)
		htk.lm_merge(lm_list, inter_weights, 'InterpolatedLMs/lm_'+episode)
		htk.lm_rescore(episode,'InterpolatedLMs/lm_'+episode,'./models','lm_inter_supervised')

	



def step4():
	'''
	Perform acoustic model rescoring
	Adopt the l.m. rescored models from previous step and update the a.m.
	'''
	parent_dir = 'model/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:

		htk.determinize_lats(episode, 'lattices', 'lm_inter_supervised', parent_dir)
		htk.am_rescore(episode, parent_dir, 'merge', parent_dir, 'grph', 'grph_rescored')
	
	pass



def step5():
	'''
	Perform acoustic model adaptation (needs to be done for YTBEeval seperately)
	'''
	parent_dir = 'model/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:

		
	htk.am_adapt(episode, parent_dir, 'grph_rescored', parent_dir, 'plp', outpass ="grph-plp-adapt")
	htk.am_rescore_adapt(episode,
                 parent_dir,
                 'merge', #this is the determinised
                 parent_dir,
                 'grph-plp-adapt',
                 parent_dir,
                 'plp',
                 'plp_adapted_grph_plp')
	
	pass

if __name__ == "__main__":
	exp_mlf()
	pass
