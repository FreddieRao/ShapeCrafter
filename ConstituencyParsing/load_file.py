import numpy as np
import json
import pandas as pd
import tqdm

def get_all_valid_data_text2shape(file_name):
    # Read Text2Shape CSV file and return texts_dict & texts_list
    df = pd.read_csv(file_name, usecols= ['modelId', 'description', 'category'])

    df = df.reset_index()  # make sure indexes pair with number of rows
    texts_dict = {}
    texts_list = []

    for index, row in tqdm.tqdm(df.iterrows()):
        if str(row['category']) == 'Chair':
            if str(row['modelId']) not in texts_dict:
                texts_dict[str(row['modelId'])] = []
            texts_dict[str(row['modelId'])].append(str(row['description']))
            texts_list.append(str(row['description']))
    
    print('# Text is:', len(texts_list))
    
    return texts_dict, texts_list

def read_valid_phrase_file(csv_file):
    # Read Runon Sentence CSV file and renturn mode_id & phrase_texts list
    df = pd.read_csv(csv_file)
    df = df.reset_index()  # make sure indexes pair with number of rows
    
    index_list = []
    model_id_list = []
    phrase_text_list = []

    for index, row in df.iterrows():
        index_list.append(index)
        model_id_list.append(row['model_id'])
        phrase_text_list.append(row['phrase_texts'])
        # if len(index_list) > 80:
        #     break #FOR DEBUG
    print('# {} Phrases loaded'.format(len(index_list)))
    return df, index_list, model_id_list, phrase_text_list

def read_tree_list_file(json_file):
    # Read Tree List Json file
    with open(json_file) as f:
        dict_list = json.load(f)
    return dict_list

def write_tree_list_file(w_file, dict_list):
    # Write Tree List Json file
    with open(w_file, 'w') as fout:
        json.dump(dict_list, fout)
    
def write_pandas_file(dst_path, data):
    # Write pandas file to CSV
    data.to_csv(dst_path)

def load_similarity_matrix(np_path):
    # Load Similarity Matrix, and file id
    with np.load(np_path) as data:
        s_matrix = data['s_matrix']
        index_a = data['index_a']
        index_b = data['index_b']
    
    return index_a, index_b, s_matrix

def read_csv(csv_file):
    # Read Runon Sentence CSV file and renturn mode_id & phrase_texts list
    df = pd.read_csv(csv_file)
    df = df.reset_index()  # make sure indexes pair with number of rows
    return df