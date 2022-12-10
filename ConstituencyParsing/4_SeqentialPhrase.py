import os
import tqdm
import numpy as np
import json

# from tags import *
# from tree import *
from path import *
from load_file import *


def write_phrase_sequence(file_path, sentphrase_seqence_path):
    df = read_csv(file_path)
    index_list = []
    model_id_list = []
    phrase_text_list = []
    valid_list = []
    start_tree_list = []

    for index, row in df.iterrows():
        index_list.append(index)
        model_id_list.append(row['model_id'])
        phrase_text_list.append(row['file_id'])
        valid_list.append(row['is_valid'])
        start_tree_list.append(row['start_tree_id'])
    print("# {} Phrases Loaded!".format(len(index_list)))

    cur_model_id , cur_file_id, cur_start_tree_id = None, None, None
    all_id_list = []
    acc_id_list = []
    max_len = 0

    for idx, model_id, file_id, is_valid, start_tree_id in tqdm.tqdm(zip(index_list, model_id_list, phrase_text_list, valid_list, start_tree_list)):
        if model_id != cur_model_id or file_id != cur_file_id or start_tree_id != cur_start_tree_id:
            cur_model_id , cur_file_id, cur_start_tree_id = model_id, file_id, start_tree_id
            all_id_list.append(acc_id_list)
            length = len(acc_id_list)
            max_len = length if length > max_len else max_len
            acc_id_list = []
        if is_valid:
            acc_id_list.append(idx)

    max_len = length if length > max_len else max_len
    all_id_list.append(acc_id_list) # append the last valid seq list
    _ = all_id_list.pop(0)

    print("# {} Max Length of Seqeuence!".format(max_len))
    with open(sentphrase_seqence_path, 'w') as f:
        json.dump(all_id_list, f)
    
    with open(sentphrase_seqence_path, 'r') as f:
        all_id_list = json.load(f)
    print('# {} Sequence List Loaded!'.format(len(all_id_list)))

def write_phrase_shapeglot_sequence(file_path, sentphrase_seqence_path):
    df = read_csv(file_path)
    index_list = []
    model_id_list = []
    phrase_text_list = []
    valid_list = []
    start_tree_list = []

    for index, row in df.iterrows():
        index_list.append(index)
        model_id_list.append(row['model_id'])
        phrase_text_list.append(row['file_id'])
        valid_list.append(row['is_valid'])
        start_tree_list.append(row['start_tree_id'])
    print("# {} Phrases Loaded!".format(len(index_list)))

    cur_model_id , cur_file_id, cur_start_tree_id = None, None, None
    all_id_list = []
    acc_id_list = []
    max_len = 0

    for idx, model_id, file_id, is_valid, start_tree_id in tqdm.tqdm(zip(index_list, model_id_list, phrase_text_list, valid_list, start_tree_list)):
        if model_id != cur_model_id or file_id != cur_file_id or start_tree_id != cur_start_tree_id or start_tree_id != 0:
            cur_model_id , cur_file_id, cur_start_tree_id = model_id, file_id, start_tree_id
            if len(acc_id_list) > 0:
                all_id_list.append(acc_id_list)
                length = len(acc_id_list)
                max_len = length if length > max_len else max_len
                acc_id_list = []
        if is_valid:
            acc_id_list.append(idx)

    max_len = length if length > max_len else max_len
    if len(acc_id_list) > 0:
        all_id_list.append(acc_id_list) # append the last valid seq list

    print("# {} Max Length of Seqeuence!".format(max_len))
    with open(sentphrase_seqence_path, 'w') as f:
        json.dump(all_id_list, f)
    
    with open(sentphrase_seqence_path, 'r') as f:
        all_id_list = json.load(f)
    print('# {} Sequence List Loaded!'.format(len(all_id_list)))

if __name__ == "__main__":
    phrase_valid_file_path = SIMILAR_PHRASE_PATH
    sentphrase_seqence_path = VALID_ID_PATH
    write_phrase_shapeglot_sequence(phrase_valid_file_path, sentphrase_seqence_path)
