import os
import math
import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import time
import tqdm
import json
import pandas as pd
import numpy as np

from tags import *
from tree import *
from path import *
from load_file import *

# benepar.download('benepar_en3_large')


def get_valid_phrases_from_tree(src_path, dst_path):
    # Tree dict to phrase list
    all_model_ids = []
    all_file_ids = []
    
    all_start_tree_ids = []
    all_cur_tree_ids = []
    all_node_ids = []
    all_phrase_phrases = []
    all_phrase_texts = []

    model_ids = os.listdir(src_path)

    for model_id in tqdm.tqdm(model_ids):
        model_path = os.path.join(src_path, model_id)

        file_ids = os.listdir(model_path)
        for file_id in file_ids:
            file_path = os.path.join(model_path, file_id)
            dict_list = read_tree_list_file(file_path)
            out = construct_constituency_tree_from_dict_list(dict_list, consect_tree=True)
            num_texts = len(out['node_texts_list'])
            all_model_ids+= [model_id] * num_texts
            all_file_ids += [file_id] * num_texts
            all_start_tree_ids += out['start_tree_idx_list']
            all_cur_tree_ids += out['cur_tree_idx_list']
            all_node_ids += out['node_ids_list']
            all_phrase_texts += out['node_texts_list']
    
    all_phrase_text_ = [''] + all_phrase_texts[: len(all_phrase_texts)-1]
    for text_, text in zip(all_phrase_text_, all_phrase_texts):
        phrase = text.replace(text_, '')
        all_phrase_phrases.append(phrase)

    data_list = []
    for model_id, file_id, start_tree_id, cur_tree_id, node_id, phrase_phrase, phrase_text in tqdm.tqdm(zip(all_model_ids, all_file_ids, all_start_tree_ids, all_cur_tree_ids, all_node_ids, all_phrase_phrases, all_phrase_texts)):
        if is_stopwords_phrase(phrase_phrase):
            data_list.append([model_id, file_id, 0, start_tree_id, cur_tree_id, node_id, phrase_phrase, phrase_text])
        else:
            data_list.append([model_id, file_id, 1, start_tree_id, cur_tree_id, node_id, phrase_phrase, phrase_text])
    
    data = pd.DataFrame(
        data_list
        , 
        columns=[
            'model_id', 
            'file_id', 
            'is_valid', 
            'start_tree_id', 
            'cur_tree_id', 
            'traverse_child_id', 
            'phrase_phrase',
            'phrase_texts'
        ]
    )
    write_pandas_file(dst_path, data)    

# Phrase list to similarity matrix
def analysis_runon_phrase_file(csv_file):
    df = pd.read_csv(csv_file, usecols= ['model_id', 'phrase_texts'])
    df = df.reset_index()  # make sure indexes pair with number of rows

    length_dict = {}

    for index, row in df.iterrows():
        print(index)
        text = row['phrase_texts']
        length = len(text.split(' '))
        if str(length) not in length_dict:
            length_dict[str(length)] = 1
        else:
            length_dict[str(length)] += 1
    
    length_list = np.array([int(key) for key in length_dict ])
    length_num_list = np.array([length_dict[key] for key in length_dict ])
    sorted_args = np.argsort(length_list)
    length_list = length_list[sorted_args]
    length_num_list = length_num_list[sorted_args]

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    y_pos =  np.arange(len(length_list))
    hbars = ax.barh(length_list,length_num_list)
    ax.set_yticks(y_pos, labels=length_list, fontsize=2)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.bar_label(hbars, fontsize=2)
    plt.savefig('results/phrase_length.png', dpi=1200
        )


if __name__ == "__main__":
    dst_path = PARSED_TREE_DICT_PATH
    runon_phrse_path = PARSED_PHRASE_PATH

    # write runon sentence file from TreeDict
    get_valid_phrases_from_tree(dst_path, runon_phrse_path)