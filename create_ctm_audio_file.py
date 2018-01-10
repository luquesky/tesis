#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import base64
import zlib
from array import array
import sys
import os
import csv
import numpy as np
import pandas as pd
import threading
#from games_entrainment import helpers
#from joblib import Parallel, delayed
import multiprocessing
from multiprocessing.pool import ThreadPool
import pickle
from tqdm import tqdm
import time

lock = threading.Lock()


def load_list_key_file(filename):
    file_list = {}
    with open(filename,'r') as stream:
        for line in stream:
            key, data_file = line.strip().split()
            key = str(key)
            file_list[key] = data_file
    return file_list


def load_ctm_and_wav_from_file_and_merge(ctm_filename, wav_filename):
    ctm_data = load_ctm_file(ctm_filename)
    wav_data = load_wav_from_file(wav_filename)
    try:
        key_wav = list(wav_data.keys())[0]
        key_ctm  = list(ctm_data.keys())[0]
    except:
        print("Error loading", ctm_filename, wav_filename, ctm_data, wav_data)
        return None
  
    if key_yaml == key_ctm:
        return { key_ctm : merge_wav_and_ctm( yaml_data[key_ctm], ctm_data[key_ctm]) }
    else:
        print("ERROR: las dos claves no son iguales")
        return None


def joint_read_ctm_wav_from_key_file_list(ctm_list_filename, wav_list_filename):
    ctm_list = load_list_key_file(ctm_list_filename)
    wav_list = load_list_key_file(wav_list_filename)
    
    merged_data = {}
    #pool = ThreadPool(64)
    pool = multiprocessing.Pool(56)
    res = []
    
    for key in ( set(ctm_list.keys()) & set(wav_list.keys()) ):
        
        #load_ctm_and_wav_from_file_and_merge
        ''.join
        #load_ctm_and_yaml_from_file_and_merge(ctm_list[key], yaml_list[key])
        res.append(pool.apply_async(''.join, ([str(ctm_list[key]), str(wav_list[key])]) ))

    for r in tqdm(res):
        d = r.get()
        if d is not None:
            merged_data = {**merged_data, **d}
    return merged_data

merged_list = joint_read_ctm_wav_from_key_file_list( './data/tlf/chile/lista_key_ctms_chile.txt' ,'./data/tlf/chile/lista_key_wav_chile.txt')
import csv

with open("./data/tlf/chile/merged_list.txt", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(merged_list)

#words_path = os.path.abspath("../../data/tlf/Script09.ctm")
#wav_path = os.path.abspath("../../data/tlf/Script09.wav")

#word_intervals = helpers.get_ctm_word_intervals(words_path)

#word_intervals[:10]
