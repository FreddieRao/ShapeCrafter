import os
import math
import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import time
import tqdm
import numpy as np
import torch

from tags import *
from tree import *
from path import *
from load_file import *

# benepar.download('benepar_en3_large')

def doc_similarity(doc1, doc2):
    similarity = np.dot(doc1.vector, doc2.vector) / (np.linalg.norm(doc1.vector) * np.linalg.norm(doc2.vector))
    return similarity

def doc_list_similarity(doc1_list, doc2_list):
    doc1_feats = np.stack(doc1_list, axis=0)
    doc2_feats = np.stack(doc2_list, axis=0)

    doc1_feats = torch.from_numpy(doc1_feats)#.cuda()
    doc2_feats = torch.from_numpy(doc2_feats)#.cuda()

    doc1_feats = doc1_feats/doc1_feats.norm(dim=1)[:, None]
    doc2_feats = doc2_feats/doc2_feats.norm(dim=1)[:, None]

    similarity = (doc1_feats @ doc2_feats.T)

    return similarity.numpy()

def get_phrase_similarity_matrix(inputs):
    
    model, index_list, model_id_list, phrase_text_list, start_index, end_index, save_folder = inputs
    n_instance = len(index_list)
    instance_per_chunk = 2000
    n_chunk = math.ceil(n_instance / instance_per_chunk)
    a_index_list = index_list[start_index: end_index + 1]
    a_model_id_array = np.asarray([int(m.replace('-', '').replace('u', '11'), 16) for m in model_id_list[start_index: end_index + 1]])
    a_phrase_text_list = phrase_text_list[start_index: end_index + 1]
    
    a_embeddings = model.encode(a_phrase_text_list)


    for c_idx in tqdm.tqdm(range(0, n_chunk)): # For DEBUG
        c_start_index = c_idx * instance_per_chunk
        c_end_index = min((c_idx+1) * instance_per_chunk, n_instance)
        save_path = os.path.join(save_folder, "{}_{}x{}_{}.npz".format(str(start_index).zfill(6), str(end_index).zfill(6), str(c_start_index).zfill(6), str(c_end_index).zfill(6)))

        c_index_list = index_list[c_start_index: c_end_index + 1]
        c_model_id_array = np.asarray([int(m.replace('-', '').replace('u', '11'), 16) for m in model_id_list[c_start_index: c_end_index + 1]])
        c_phrase_text_list = phrase_text_list[c_start_index: c_end_index + 1]
        
        c_embeddings = model.encode(c_phrase_text_list)

        s_matrix = doc_list_similarity(a_embeddings, c_embeddings)

        mask = a_model_id_array[:, np.newaxis] - c_model_id_array[np.newaxis, :]
        s_matrix_mask = np.where(mask==0, 0, s_matrix)
    
        np.savez(save_path,
                s_matrix=s_matrix_mask,
                index_a=np.asarray(a_index_list),
                index_b=np.asarray(c_index_list)
                )
        print('Saved file:', save_path)

if __name__ == "__main__":
    ''' 
    Total Instances = n_process * instance_per_process
    instance_per_process: Number if Instances to process for each job. Decided by the number of instances in the dataset.
    n_process: Number of jobs required to process all the instances in the dataset.
    start_id: The id of the first job \in [0, n_process]
    end_id: The id of the last job \in [0, n_process]
    If you have one machine, set start_id=0, end_id=n_process.
    If you have N machines, for machine X, set start_id=int(n_process*X/N), end_id=int(n_process*(X+1)/N)
    '''

    import sys

    instance_per_process = 2000
    start_id = int(sys.argv[1])
    end_id = int(sys.argv[2])
    
    runon_phrse_path = PARSED_PHRASE_PATH
    similarity_folder = SIMILARITY_MATRIX_PATH


    # read runon sentence file
    _, index_list, model_id_list, phrase_text_list = read_valid_phrase_file(runon_phrse_path)
    
    # get similarity nlp model
    model = get_SentenceTransformer()
    
    # get_phrase_similarity_matrix((model, index_list, model_id_list, phrase_text_list, 0, 79, similarity_folder))
    # exit(0)

    inputs = []
    n_instance = len(index_list)
    n_process = math.ceil(n_instance / instance_per_process)
    end_id = end_id if (end_id < n_process) else (n_process)
    print('Total Number of Chunks to Process:', n_process)
    print(start_id)
    print(end_id)

    intput_list = []
    for p_idx in range(start_id, end_id):
        start_index = p_idx * instance_per_process
        end_index = min((p_idx+1) * instance_per_process, n_instance)
        intput_list.append((model, index_list, model_id_list, phrase_text_list, start_index, end_index, similarity_folder))

    from multiprocessing import Pool
    with Pool(16) as pool:
        pool.map(get_phrase_similarity_matrix, intput_list)
        pool.close()
        pool.join()
    
    # import multiprocessing as mp
    # ctx = mp.get_context('spawn')
    # q = ctx.Queue()
    # p = ctx.Process(target=get_phrase_similarity_matrix, args=intput_list)
    # p.start()
    # print(q.get())
    # p.join()