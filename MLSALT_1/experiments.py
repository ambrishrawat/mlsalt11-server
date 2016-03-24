import classes.wrapper as htk
from classes.utils import *
from classes.MLF import MLF


def step0():
	'''
	(NOT REQUIRED: only for completeness) rescore the available plp-bg lattice (bigram l.m. scores) with the 5 trigram l.m. scores
	'''

	parent_dir = 'models/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:	
		lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
		for i,language_dir in enumerate(lm_list):
			episode = episode.strip()
			htk.lm_rescore(episode, language_dir, parent_dir,'plp-tglm'+str(i+1))
	

def step1():
	'''
	Generate the interpolated language model on YouTube devlopment set (Training YTBEdev)
	'''

	'''
	generate the probability stream for the vocabulary
	'''
	epi_list_tag = 'YTBEdev'
	plex = []
	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
	for i,language_dir in enumerate(lm_list):
		plex.append([float(htk.get_plex(language_dir,'Stream/stream_'+epi_list_tag+'_lm'+str(i+1),'lib/texts/YTBEdev.dat'))])

	'''
	get interpolatiom weights for the 5 language models (expectation maximization)
	'''
	p = plex
	p = [[float(1/t[0])] for t in p ]	
	s =  sum([t[0] for t in p])
	p = [[float(t[0]/s)] for t in p]
	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
	inter_weights = em(p,epi_list_tag)
	#inter_weights = [t[0] for t in inter_weights]


	'''
	generate the interpolated language model (lmmerge)
	'''
	htk.lm_merge(lm_list, inter_weights, 'InterpolatedLMs/lm'+epi_list_tag)
	
	pass


def step2():
	'''
	Generate episode specific interpolated language models and get the updated lattices
	'''
	parent_dir = 'models/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:

		htk.lm_rescore(episode,'InterpolatedLMs/lm'+epi_list_tag,parent_dir,'lm_YTBEdev_rescore')

def step3():
	'''
	Generate episode specific interpolated language models and get the updated lattices
	'''
	parent_dir = 'models/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:
		convert('models/'+episode+'/lm_YTBEdev_rescore/rescore.mlf','DATFiles/'+episode+'_lm_YTBEdev.dat')	
		p = []
        	lm_list = ['lms/lm1','lms/lm2','lms/lm3','lms/lm4','lms/lm5']
        	for i,language_dir in enumerate(lm_list):
                	p.append([float(htk.get_plex(language_dir,'Stream/stream_'+episode+'_lm'+str(i+1),'DATFiles/'+episode+'_lm_YTBEdev.dat'))])
        
		
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
	parent_dir = 'models/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:

		htk.determinize_lats(episode, 'lattices', 'lm_inter_supervised', parent_dir, 'merge_lm_inter_supervised')
		htk.am_rescore(episode, parent_dir, 'merge_lm_inter_supervised', parent_dir, 'grph', 'grph_rescored')
	
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


	'''
	Perform second speaker adaptation (tandem/hybrid feature) and save it the new model 
	'''


	'''
	After this step, we have achieved 2 Lattices 
	'''
def step6():
	'''
	Merge 1-best hypothesis from 2 Lattices

	'''
	parent_dir = 'model/'
	epi_list_tag = 'YTBEdev'
	epi_list = get_episode_list(epi_list_tag)
	for episode in epi_list:
		mlf1_addr = './models/'+episode+'//rescore.mlf'
		mlf1 = MLF()
		mlf1.gendict(mlf1_addr)

		mlf2_addr = './models/'+episode+'//rescore.mlf'
		mlf2 = MLF()
		mlf2.gendict(mlf2_addr)	

		MLF.levenshtein(mlf1.return_dict(),mlf2.return_dict())

		mlf3 = MLF()
		mlf3.assign_dict(MLF.merge_mlf(mlf1,mlf2))
	

def step7():
	'''
	CNC combination (if time permits)
	'''



if __name__ == "__main__":
	#step0()
	#step1()
	#step2()
	#step3()
	step4()
	#step5()
	#step6()
	pass
