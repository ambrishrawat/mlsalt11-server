import HTK_scripts as htk
import numpy as np
import utils as utl
import time
import subprocess


'''
EPISODE LIST: lib/testlists/

WER after rescoring is inside scoring is in ctm tild: scoring/sclite/dev03sub_plp-bg_1best_LM12.0_IN-10.0.ctm.filt.sys -- Err
'''

def exp1():
	'''
	 obtain the 1-best output from the lattices with the bigram language model
	'''
	#episode
	#htk.one_best_list(episode, lattice_parent_dir, pass_for_lattice, save_dir)
	pass

def exp2():
	#rescore 
	#htk.lm_rescore(episode, language_dir, save_dir):
	lms = ['lms/lm1', 'lms/lm2', 'lms/lm3', 'lms/lm4','lms/lm5']
	episode_list = 'dev03'
	episodes = open('lib/testlists/'+ episode_list+'.lst', 'r')
	episodes = episodes.readlines()
	episodes = [e.strip() for e in episodes]

	for i,lm in enumerate(lms):
		save_dir = 'plp-tglm' + str(i+1)
		for e in episodes:
			htk.lm_rescore(e, lm, save_dir)
		htk.score(save_dir, episode_list, 'rescore') #Score of 1 best hypothesis

def exp3():
	pass

def exp4():
	'''
	EM like approach to find interpolated weights

	Streams are list of word probabilities for each language
	for now streams for the 5 models are in major directory: stream1, stream2 ..., stream5

	perplecity list is in lists/perplexity.lst

	see interpolatedLM.py

	final interpolated LM is in lm_int.qz
	'''
	pass

def exp5():
	pass

def exp6():
	'''
	stream.sh generates streams for set of episoed
	For each ep in eval03
	1. rescore wrt interpolated LM
	2. convert 1bh (.mlf) to .dat file -- DIY
	3. Get perplexities for all 5 LM{1..5} -- to use for interpolated_LM (EM) to get new interpolation weights
	4. RESCORE LATTICE -- to get 1 best hypothesis
	'''
	#dev03
	#get_plex('lm_int_dev03','stream_lm_intdev03', 'lib/texts/dev03.dat')
	episode_list = 'eval03'
	episodes = open('lib/testlists/'+ episode_list+'.lst', 'r')
	episodes = episodes.readlines()
	episodes = [e.strip() for e in episodes]

	save_dir = 'plp/plp-ilm'

	for e in episodes:
		#step 1
		htk.lm_rescore(e, 'lm_int_dev03', save_dir)	
		#step 2
		dat_file = 'dat_files/sentences.dat'
		mlf_file = save_dir + '/'+ e + '/rescore/rescore.mlf' #plp-ilm/eval03_DEV011-20010206-XX1830/rescore
		utl.convert(mlf_file, dat_file)
		#step 3
		lm_dir = 'interpolated_lms/lm_' + episode_list
		utl.LM_interpolation(dat_file, lm_dir)
		#step 4
		output = 'lm_rescore/rescore_' + episode_list
		htk.lm_rescore(e, lm_dir, output)
	
	#get WER
	htk.score(output, episode_list, 'rescore')


#--------SPEAKER ADAPTATION-----

def exp_sa_1():
	#fix episode
	#os.system('rm -r ')
	episode_list = 'dev03sub'
	episode = 'dev03_DEV001-20010117-XX2000'
	save_dir = 'plp/am/plp-bg'
	#determinise
	htk.determinize_lats(episode, 'lattices', 'decode', save_dir)
	#rescore -- in save_dir/episode/decode -- will have rescored hmm lattice
	htk.am_rescore(episode, save_dir, 'merge', save_dir, 'plp', 'plp-decode')
	#Comment on performance compared to the original lattices
	#score 1-best hypothesis of this -- mlf file
	#scoring of 1-best hypothesis
	htk.score(save_dir, episode_list, 'plp-decode')
	#generate score of original lattice
	htk.one_best_list(episode, 'lattices', 'decode', save_dir)
	htk.score(save_dir, episode_list, '1best/LM12.0_IN-10.0')




def exp_sa_2():
	'''
	Adaptation

	'''
	episode_list = 'dev03sub'
	episode = 'dev03_DEV001-20010117-XX2000'
	save_dir = 'plp/am/plp-bg'
	#get transforms--in save_dir/episode/adapt
	htk.am_adapt(episode, save_dir, '1best/LM12.0_IN-10.0/', save_dir, 'plp', outpass ="adapt")
	#rescore using transforms
	
	htk.am_rescore_adapt(episode,
                     save_dir,
                     'merge', #this is the determinised
                     save_dir,
                     'adapt',
                     save_dir,
                     'plp',
                     'plp_adapted_original_1best')
	#score
	htk.score(save_dir, episode_list, 'plp_adapted_original_1best')


def exp_sa_3():
	episode_list = 'dev03sub'
	episode = 'dev03_DEV001-20010117-XX2000'
	save_dir = 'plp/am/plp-bg'
	#determinise-- done in exp 1
	#htk.determinize_lats(episode, 'lattices', 'decode', save_dir)
	#rescore -- in save_dir/episode/decode -- will have rescored hmm lattice -- for new supervision
	htk.am_rescore(episode, save_dir, 'merge', save_dir, 'grph-plp', 'grph-plp-decode')
	time.sleep(120)
	#adapt emission distribution parameters for plp hmm using grph-plp supervision
	htk.am_adapt(episode, save_dir, 'grph-plp-decode', save_dir, 'plp', outpass ="grph-plp-adapt")
	#we got params, use these and rescore
	htk.am_rescore_adapt(episode,
                 save_dir,
                 'merge', #this is the determinised
                 save_dir,
                 'grph-plp-adapt',
                 save_dir,
                 'plp',
                 'plp_adapted_grph_plp')


	#score
	htk.score(save_dir, episode_list, 'plp_adapted_grph_plp')



##------------SYSTEM COMBINATION--------##
#substitution: 10, insertion: 7, deletion: 7


def exp_comb_1_comparison_results():
	'''
	Levenshtein distance
	we do not consider time information-align words

	'''
	mfl_1_parent_dir = 'plp/am/plp-bg'
	mfl_2_parent_dir = 'plp/am/plp-bg'
	mlf_1_pass = 'grph-plp-decode'
	mlf_2_pass = 'plp-decode'
	episode = 'dev03_DEV001-20010117-XX2000' 

	htk.sc_hled_compare(episode, mfl_1_parent_dir, mlf_1_pass, mfl_2_parent_dir, mlf_2_pass)

def exp_comb_1():
	'''
	Levenshtein distance
	we do not consider time information-align words

	'''
	mfl_1_parent_dir = 'plp/am/plp-bg'
	mfl_2_parent_dir = 'plp/am/plp-bg'
	mlf_1_pass = 'grph-plp-decode'
	mlf_2_pass = 'plp-decode'
	episode = 'dev03_DEV001-20010117-XX2000'

	mlf1 = mfl_1_parent_dir + '/' +episode+ '/' + mlf_1_pass + '/rescore.mlf'
	mlf2 = mfl_2_parent_dir + '/' +episode+ '/' + mlf_2_pass + '/rescore.mlf'
	utl.edit_distance(mlf1, mlf2)

def exp_comb_2():
	mfl_1_parent_dir = 'plp/am/plp-bg'
	mfl_2_parent_dir = 'plp/am/plp-bg'
	mlf_1_pass = 'grph-plp-decode'
	mlf_2_pass = 'plp-decode'
	episode = 'dev03_DEV001-20010117-XX2000'
	episode_list = 'dev03sub'
	mlf1 = mfl_1_parent_dir + '/' +episode+ '/' + mlf_1_pass + '/rescore.mlf'
	mlf2 = mfl_2_parent_dir + '/' +episode+ '/' + mlf_2_pass + '/rescore.mlf'

	mlf_dic = utl.merge_mlf(mlf1, mlf2)
	fout = 'dev03_DEV001-20010117-XX2000/rescore/rescore.mlf'
	utl.write_mlf(mlf_dic, episode, '.', '.' , fout)

	htk.score('.', 'dev03sub', 'rescore')
	#htk.score(mfl_1_parent_dir, episode_list, mlf_1_pass)
	htk.score(mfl_2_parent_dir, episode_list, mlf_2_pass)

	

def exp_cn():
	episode_list = 'dev03sub'
	episode = 'dev03_DEV001-20010117-XX2000'
	save_dir = 'plp/am/plp-bg'
	
	lattice_pass = 'grph-plp-decode'
	htk.cnrescore(episode,save_dir,lattice_pass)
	htk.score(save_dir, episode_list, 'plp-decode')
	htk.score(save_dir, episode_list, lattice_pass+'_cn')
	htk.score_map(save_dir, episode_list, lattice_pass+'_cn','plp-bg_decode_cn')
	

def exp_cn_combine():
	episode_list = 'dev03sub'
	episode = 'dev03_DEV001-20010117-XX2000'
	save_dir = 'plp/am/plp-bg'
	
	cnc1_pass = 'grph-plp-decode_cn'
	cnc2_pass = 'plp-decode_cn'

	cnc1 = save_dir + '/' + episode + '/' + cnc1_pass + '/lattices/'
	cnc2 = save_dir + '/' + episode + '/' + cnc2_pass + '/lattices/'

	fout = 'dev03_DEV001-20010117-XX2000/rescore/rescore.mlf'

	mlf_dic = utl.cnc_combine(cnc1,cnc2)
	utl.write_mlf(mlf_dic,episode,'.','.',fout)
	
	htk.score('.',  episode_list, 'rescore')
	htk.score_map('.', episode_list, 'rescore','plp-bg_decode_cn')
	htk.score_map('.', episode_list, 'rescore','grph-plp-bg_decode_cn')
	

if __name__ == '__main__':
	#exp6()
	#exp_sa_1()
	#exp_sa_3()
	#exp_comb_2()
	#exp_cn()
	exp_cn_combine()



'''


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




'''









