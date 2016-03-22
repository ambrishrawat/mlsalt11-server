import os
import subprocess
import re
os.chdir('/home/vgj21/MLSALT2/major')

def score(parent_dir, show_list_tag, mlf_location):
    # inside parent_dir there are folders containing one-best-lists produced by decoding one model on all shows, it will search the directory for all of the shows
    # show list tags: dev03, dev03sub, eval03 - it will scores on all shows in the parent directory against the correct one best list
    # mlf_location - the name of the subdirectory of each show in the parent directory where the mlf file is located (it is called the "pass")
    # the results are generated to scoring/sclite with the appropriate naming convention

    score_function_call = "./scripts/score.sh " + parent_dir + " " + show_list_tag + " " + mlf_location
    os.system(score_function_call)

def score_map(parent_dir, show_list_tag, mlf_location, map_addr):
    # inside parent_dir there are folders containing one-best-lists produced by decoding one model on all shows, it will search the directory for all of the shows
    # show list tags: dev03, dev03sub, eval03 - it will scores on all shows in the parent directory against the correct one best list
    # mlf_location - the name of the subdirectory of each show in the parent directory where the mlf file is located (it is called the "pass")
    # the results are generated to scoring/sclite with the appropriate naming convention

    score_function_call = "./scripts/score.sh -CONFTREE ./lib/trees/" + map_addr+".tree " + parent_dir + " " + show_list_tag + " " + mlf_location
    os.system(score_function_call)

def lm_rescore(episode, language_dir, save_dir):
    # rescore lattice and gives you one best hypothesis in the save_dir (which is the parent directory for score)

    # episode - name of the episode (lattices) to rescore using your language model
    # language_dir - location of the new language model, path to file
    # save_dir - become parent directory for rescore

    lm_rescore_funtion_call = "./scripts/lmrescore.sh " + episode + " lattices decode " + language_dir \
                    + " " + save_dir + " FALSE"

    os.system(lm_rescore_funtion_call)

    while True:
        if subprocess.check_output('qstat') == '':
            return

def one_best_list(episode, lattice_parent_dir, pass_for_lattice, save_dir):
    # it is looking for lattice in (lattice_parent_director)/(episode)/(pass_for_lattice)
    # will put one best list (MLF file) in (save_dir)/(episode)/1best/LM12.0_IN-10.0/

    one_best_function_call = "./scripts/1bestlats.sh " + episode + " " + lattice_parent_dir + " " + pass_for_lattice + \
        " " + save_dir

    os.system(one_best_function_call)
    while True:
        if subprocess.check_output('qstat') == '':
            return 

def get_plex(path_to_language_model, save_stream_path, path_to_dat_file):
    # path_to_dat_file - dat file is sentence xml file, mlfs (one-best) converted to xml
    # save_stream_path is path to stream file (ends in csv)
    # path_to_language_model - path to language model file
    
    lplex_function_call = "base/bin/LPlex -C lib/cfgs/hlm.cfg -s " + save_stream_path + " -u -t " +\
                               path_to_language_model + " " + path_to_dat_file
    output = subprocess.check_output(lplex_function_call, shell=True)
    plex = re.search('perplexity (.*?), var',output)
    return plex.group(1)
    

def lm_merge(language_model_path_list, language_model_coefficient_list, new_language_modle_path):
    # language_model_path_list is a list of strings
    # language_model_coefficient_list is a list of floats
    # new_language_modle_path is a path to new model file

    merge_function_call = "./base/bin/LMerge -C lib/cfgs/hlm.cfg "
    for i in range(len(language_model_path_list)-1):
        merge_function_call = merge_function_call + "-i " + str(language_model_coefficient_list[i]) + " " + language_model_path_list[i] + " "

    merge_function_call = merge_function_call + "lib/wlists/train.lst " + language_model_path_list[-1] + " " + new_language_modle_path

    os.system(merge_function_call)


def determinize_lats(episode, lattice_parent_dir, pass_for_lattice, save_dir):
    # it is looking for lattice in (lattice_parent_director)/(episode)/(pass_for_lattice)
    # will put the determinized lattice in (save_dir)/(episode)/merge/lattices

    determinize_lats_function_call = "./scripts/mergelats.sh " + episode + " " + lattice_parent_dir + " " + pass_for_lattice + \
        " " + save_dir

    os.system(determinize_lats_function_call)
    while True:
        if subprocess.check_output('qstat') == '':
            return    

def am_rescore(episode, original_lattice_parent_dir, original_lattice_pass, targert_parent_dir, acoustic_model, outpass_param = 'decode'):
    # will look for original lattice (determinized) in original_lattice_parent_dir/episode/original_lattice_pass/
    # will save new lattice in targert_parent_dir/episode/decode/
    # acoustic models are used to generate the new lattice - options are plp, grph-plp, tandem, grph-tandem, hybrid

    am_rescore_function_call =  "./scripts/hmmrescore.sh -OUTPASS " + outpass_param + " " + episode + " " + original_lattice_parent_dir + \
        " " + original_lattice_pass + " " + targert_parent_dir + " " + acoustic_model

    os.system(am_rescore_function_call)
    while True:
        if subprocess.check_output('qstat') == '':
            return 

def am_adapt(episode, mlf_parent_dir, mlf_pass, adapted_param_save_parent_dir, acoustic_model, outpass ="adapt"):
    # this needs to be run on a adapted acoustic model one best (mlf) file if you are not using the default language
    # model, meaning you must first determinize, adapt to the language model using am_rescore

    # looks for mlf in mlf_parent_dir/episode/mlf_pass/
    # saves adapted parameters in adapted_param_save_parent_dir/episode/adapt

    am_adapt_function_call = "./scripts/hmmadapt.sh -OUTPASS " + outpass + " " + episode + " " + mlf_parent_dir + " " \
                             +  mlf_pass  + " " + adapted_param_save_parent_dir + " " + acoustic_model
    os.system(am_adapt_function_call)
    while True:
        if subprocess.check_output('qstat') == '':
            return



def am_rescore_adapt(episode,
                     original_lattice_parent_dir,
                     original_lattice_pass,
                     adaptation_param_parent_dir,
                     adaptation_param_pass,
                     targert_parent_dir,
                     acoustic_model,
                     outpass_param = 'decode'):

    # looks for the determinized lattice to rescore in original_lattice_parent_dir/episode/original_lattice_pass/
    # look for adaptation parameters in adaptation_param_parent_dir/episode/adaptation_param_pass
    # saves the rescored lattice at targert_parent_dir/episode/decode

    am_rescore_function_call = "./scripts/hmmrescore.sh -OUTPASS "+outpass_param+" -ADAPT " +adaptation_param_parent_dir + " " + \
                                adaptation_param_pass + " " + episode + " " + original_lattice_parent_dir + \
                                " " + original_lattice_pass + " " + targert_parent_dir + " " + acoustic_model

    os.system(am_rescore_function_call)

    while True:
        if subprocess.check_output('qstat') == '':
            return


#---System combination----#

def sc_hled_compare(episode, mfl_1_parent_dir, mlf_1_pass, mfl_2_parent_dir, mlf_2_pass):
    #compares the twp MLFs for the episode and outputs the number of substitutions, deletions and insertions
    hled_function_call = './base/bin/HLEd -i '+ mfl_1_parent_dir + '/' +episode+ '/' + mlf_1_pass + '/score.mlf -l \'*\' /dev/null ' + mfl_1_parent_dir + '/' +episode+ '/' + mlf_1_pass +'/rescore.mlf'
    
    os.system(hled_function_call)
    
    hres_function_call = './base/bin/HResults -t -f -I ' + mfl_1_parent_dir + '/' +episode+ '/' + mlf_1_pass + '/score.mlf lib/wlists/train.lst ' + mfl_2_parent_dir + '/' +episode + '/' +mlf_2_pass+ '/rescore.mlf'

    os.system(hres_function_call)
    
#generate a confusion network
def cnrescore(episode, lattice_parent_dir, lattice_pass):
    #converts a lattice for the episode into a confusion network
    #stores the confusition network in the output_lattice_parent_dir/episode/'lattice_pass_cn'/lattices
    cnrescore_function_call = './scripts/cnrescore.sh ' + episode + ' ' + lattice_parent_dir + ' ' + lattice_pass + ' ' + lattice_parent_dir
    os.system(cnrescore_function_call)
    while True:
        if subprocess.check_output('qstat') == '':
            return
	








