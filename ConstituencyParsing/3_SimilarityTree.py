import os
import tqdm
import numpy as np

# from tags import *
# from tree import *
from path import *
from load_file import *

def analysis_similarity_score_distribution(similarity_folder):
    sim_score_dict = {
        '0.80': 0,
        '0.81': 0,
        '0.82': 0,
        '0.83': 0,
        '0.84': 0,
        '0.85': 0,
        '0.86': 0,
        '0.87': 0,
        '0.88': 0,
        '0.89': 0,
        '0.90': 0,
        '0.91': 0,
        '0.92': 0,
        '0.93': 0,
        '0.94': 0,
        '0.95': 0,
        '0.96': 0,
        '0.97': 0,
        '0.98': 0,
        '0.99': 0,
    }

    files = os.listdir(similarity_folder)
    for file in tqdm.tqdm(files):
        file_path = os.path.join(similarity_folder, file)
        index_a, index_b, s_matrix = load_similarity_matrix(file_path)
        for key in sim_score_dict:
            float_key = float(key)
            count = np.sum(np.where(np.logical_and(s_matrix >= float_key, s_matrix < (float_key + 0.01)), 1, 0))
            sim_score_dict[key] += count
    
    for key in sim_score_dict:
        print(key, sim_score_dict[key])

    score_list = list(sim_score_dict.keys())
    score_num_list = [sim_score_dict[_] for _ in sim_score_dict]

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    y_pos =  np.arange(len(score_list))
    hbars = ax.barh(score_list,score_num_list)
    ax.set_yticks(y_pos, labels=score_list, fontsize=2)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.bar_label(hbars, fontsize=2)
    plt.savefig('../results/similarity_score_distribution_xx.png', dpi=1200
        )

def select_similarity_phrases(similarity_folder, phrase_text_list, example_folder):
    sim_score_dict = {
        '0.80': 0,
        '0.81': 0,
        '0.82': 0,
        '0.83': 0,
        '0.84': 0,
        '0.85': 0,
        '0.86': 0,
        '0.87': 0,
        '0.88': 0,
        '0.89': 0,
        '0.90': 0,
        '0.91': 0,
        '0.92': 0,
        '0.93': 0,
        '0.94': 0,
        '0.95': 0,
        '0.96': 0,
        '0.97': 0,
        '0.98': 0,
        '0.99': 0,
    }

    files = os.listdir(similarity_folder)
    for file in tqdm.tqdm(files):
        file_path = os.path.join(similarity_folder, file)
        index_a, index_b, s_matrix = load_similarity_matrix(file_path)
        for key in sim_score_dict:
            example_path = os.path.join(example_folder, key + '.txt')
            float_key = float(key)
            rel_idxs =np.transpose(
                    np.nonzero(
                        np.where(np.logical_and(s_matrix >= float_key, s_matrix < (float_key + 0.01)), 
                            1, 0)
                        )
                    )
            with open(example_path, 'a+') as f:
                for i in range(rel_idxs.shape[0]):
                    rel_idx_a, rel_idx_b = index_a[rel_idxs[i, 0]], index_b[rel_idxs[i, 1]]
                    f.write(phrase_text_list[rel_idx_a] + '\t' + model_id_list[rel_idx_a] + '\n')
                    f.write('\t' + phrase_text_list[rel_idx_b] + '\t' + model_id_list[rel_idx_b]+ '\n')

def update_runon_phrase_with_similarity(similarity_folder, dst_path, df, index_list, model_id_list, phrase_text_list, score_thres=0.94):
    similar_model_id_list = [0] * len(index_list)
    similar_model_score_list = [0] * len(index_list)
    files = os.listdir(similarity_folder)
    for file in tqdm.tqdm(files):
        file_path = os.path.join(similarity_folder, file)
        index_a, index_b, s_matrix = load_similarity_matrix(file_path)
        rel_idxs =np.transpose(np.nonzero(np.where(s_matrix >= score_thres, 1, 0)))
        for i in range(rel_idxs.shape[0]):
            rel_idx_a, rel_idx_b = index_a[rel_idxs[i, 0]], index_b[rel_idxs[i, 1]]
            model_id_b = model_id_list[rel_idx_b]
            if similar_model_id_list[rel_idx_a] == 0:
                similar_model_id_list[rel_idx_a] = [model_id_b]
                similar_model_score_list[rel_idx_a] = [s_matrix[rel_idxs[i, 0], rel_idxs[i, 1]]]
            if model_id_b not in similar_model_id_list[rel_idx_a]:
                similar_model_id_list[rel_idx_a].append(model_id_b)
                similar_model_score_list[rel_idx_a].append(s_matrix[rel_idxs[i, 0], rel_idxs[i, 1]]) 

    df['similar_model_id'] = similar_model_id_list
    df['similar_model_score'] = similar_model_score_list
    write_pandas_file(dst_path, df)
            

if __name__ == "__main__":

    runon_phrse_path = PARSED_PHRASE_PATH
    runon_similar_phrse_path = SIMILAR_PHRASE_PATH
    similarity_folder = SIMILARITY_MATRIX_PATH
    
    if not os.path.isdir(similarity_folder):
        os.makedirs(similarity_folder)

    df, index_list, model_id_list, phrase_text_list = read_valid_phrase_file(runon_phrse_path)
    update_runon_phrase_with_similarity(similarity_folder, runon_similar_phrse_path, df, index_list, model_id_list, phrase_text_list)
    
    # Analyse Functions
    # analysis_similarity_score_distribution(similarity_folder)
    # example_folder = ''
    # select_similarity_phrases(similarity_folder, phrase_text_list, example_folder)
