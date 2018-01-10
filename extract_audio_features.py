#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, getopt
import os
import csv
import numpy as np
import pandas as pd
import time
import pydub
import pickle
from tqdm import tqdm
from games_entrainment import helpers
from games_entrainment import features
from games_entrainment.tsa import entrainment
from games_entrainment import config
import threading
import multiprocessing
from multiprocessing.pool import ThreadPool

lock = threading.Lock()
pool = ThreadPool(15)

inputfile = ''
outputfile = ''

def load_list_key_ctm_wav_file(filename):
    file_list = {}
    with open(filename,'r') as stream:
        for line in stream:
            key, ctm_tmp, wav_tmp = line.strip().split()
            key = str(key)
            file_list[key] = [(ctm_tmp),(wav_tmp)]
    return file_list

def load_list_key_ctm_wav_gender_file(filename):
    file_list = {}
    with open(filename,'r') as stream:
        for line in stream:
            key, ctm_tmp, wav_tmp, l_gender, r_gender = line.strip().split()
            key = str(key)
            file_list[key] = [(ctm_tmp),(wav_tmp),(l_gender),(r_gender)]
    return file_list


def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

def join_entrainment_features (key, speechA, speechB):
        merge = {}

        for feature in features:
            try:
                A = helpers.create_tama(speechA, feature)
                B = helpers.create_tama(speechB, feature)

                if (A.count() and B.count() > config.SERIES_LENGTH_THRESHOLD):
                    l_AB, E_AB, l_BA, E_BA = entrainment(A, B, lags=range(-6, 6))
                    merge = merge_two_dicts(merge, { feature: pd.DataFrame ( { 'l_AB' : [l_AB], 'E_AB' : [E_AB], 'l_BA' : [l_BA], 'E_BA' : [E_BA]  }  ) } )
                else:
		    pass
                    return None

            except:
                print("create_tama error in file",key)
                return None

        return { key: [merge] }

def main(argv):
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print 'extract_audio_features.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'extract_audio_features.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile
    return (inputfile)

if __name__ == "__main__":

    inputfile = main(sys.argv[1:])
    print 'Input file is "', inputfile
    #'data/tlf/chile/lista_key_ctms_wavs_chile_test2.txt'
    file_list = load_list_key_ctm_wav_gender_file( inputfile )
    #with open('BI_dataframe_chile_interspeech.csv','rb') as csvfile:
    #    BI = csv.reader(csvfile, delimiter=' ', quotechar='|')
            #for row in spamreader:
    #            print ', '.join(row)
    res = []
    for key in ( tqdm(set(file_list.keys())) ):

        #key = r
        words_path = os.path.abspath(file_list[key][0])
        wav_path = os.path.abspath(file_list[key][1])
        l_gender = str(file_list[key][2]).lower()
        r_gender = str(file_list[key][3]).lower()
        print 'Channel A is detected as gender ', l_gender 
        print 'Channel A is detected as gender ', r_gender
        word_intervals = helpers.get_ctm_word_intervals(words_path,'_a')

        speechA = helpers.create_speech(
            wav_path=wav_path,
            word_intervals=word_intervals,
            gender=l_gender,
        )

        word_intervals = helpers.get_ctm_word_intervals(words_path,'_b')
        speechB = helpers.create_speech(
            wav_path=wav_path,
            word_intervals=word_intervals,
            gender=r_gender,
        )

        #for feature in features:
        join_entrainment_features
        res.append(pool.apply_async( join_entrainment_features, ( key, speechA, speechB )))

    merged_data = {}

    for r in tqdm(res):
        d = r.get()
        if d is not None:
            merged_data = merge_two_dicts(merged_data,d)

    pickle.dump(  merged_data , open( inputfile+".pkl", "wb" ) )
