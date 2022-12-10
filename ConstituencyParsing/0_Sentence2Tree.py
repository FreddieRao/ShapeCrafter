import os
import json
import tqdm
from tags import *
from tree import *
from path import *
from load_file import *

# Sentence to tree dict
def traverse_tree(phrase_tree):
    phrase_dict = {} # dict{text: Str, label: Tuple, child: List}
    phrase_dict['text'] = phrase_tree.text
    phrase_dict['label'] = phrase_tree.label
    
    merging_label = False
    merging_conjuction = True
    while merging_conjuction:
        phrase_dict['children'] = []
        for c_idx, child in enumerate(phrase_tree.children):
            
            if merging_label:
                continue
            
            child_dict = traverse_tree(child)

            if not label_is_pos_punct(child_dict['label']) and \
                not label_is_pos_special(child_dict['label']) and \
                not label_is_benepar_valid(child_dict['label']): # Stop Parsing invalid pos and invalid phrase
                phrase_dict['children'] = []
                break

            elif label_is_conjuction(child_dict['label']) or \
                       is_stopwords_phrase(child_dict['text']): # Merge conjunction, stopwords to right
                
                if c_idx == len(phrase_tree.children) - 1: # rightest
                    if len(phrase_tree.children) == 1 :
                        phrase_dict['children'] = []
                        break
                    elif len(phrase_tree.children) == 2 :
                        if len(phrase_tree.children[c_idx - 1].children) > 0:
                            phrase_tree = upgrade_with_left_tree(phrase_tree, phrase_tree.children[c_idx - 1], phrase_tree.children[c_idx])
                            merging_label = True
                        else:
                            phrase_dict['children'] = []
                            break
                    else: # len(phrase_tree.children) > 2
                        phrase_tree.children[c_idx - 1] = merge_to_left_tree(phrase_tree.children[c_idx - 1], phrase_tree.children[c_idx])
                        _ = phrase_tree.children.pop(c_idx)
                        merging_label = True
                
                else: # some right nodes remains
                    if len(phrase_tree.children) == 2 :
                        if len(phrase_tree.children[c_idx + 1].children) > 0:
                            phrase_tree = upgrade_with_right_tree(phrase_tree, phrase_tree.children[c_idx + 1], phrase_tree.children[c_idx])
                            merging_label = True
                        else:
                            phrase_dict['children'] = []
                            break
                    else: # len(phrase_tree.children) > 2
                        phrase_tree.children[c_idx + 1] = merge_to_right_tree(phrase_tree.children[c_idx + 1], phrase_tree.children[c_idx])
                        _ = phrase_tree.children.pop(c_idx)
                        merging_label = True

            elif label_is_pos_punct(child_dict['label']): # Merge punct to left
                
                if c_idx == 0: # leftest
                    if len(phrase_tree.children) == 2 :
                        if len(phrase_tree.children[c_idx + 1].children) > 0:
                            phrase_tree = upgrade_with_right_tree(phrase_tree, phrase_tree.children[c_idx + 1], phrase_tree.children[c_idx])
                            merging_label = True
                        else:
                            phrase_dict['children'] = []
                            break
                    else: # len(phrase_tree.children) > 2
                        phrase_tree.children[c_idx + 1] = merge_to_right_tree(phrase_tree.children[c_idx + 1], phrase_tree.children[c_idx])
                        _ = phrase_tree.children.pop(c_idx)
                        merging_label = True
                
                else: # some left nodes remains
                    if len(phrase_tree.children) == 2 :
                        if len(phrase_tree.children[c_idx - 1].children) > 0:
                            phrase_tree = upgrade_with_left_tree(phrase_tree, phrase_tree.children[c_idx - 1], phrase_tree.children[c_idx])
                            merging_label = True
                        else:
                            phrase_dict['children'] = []
                            break
                    else: # len(phrase_tree.children) > 2
                        phrase_tree.children[c_idx - 1] = merge_to_left_tree(phrase_tree.children[c_idx - 1], phrase_tree.children[c_idx])
                        _ = phrase_tree.children.pop(c_idx)
                        merging_label = True
            else:
                phrase_dict['children'].append(child_dict)

        if merging_label:
            merging_label = False
        else:
            merging_conjuction = False
    # print(phrase_dict)
    return phrase_dict

def get_tree_from_sentence(nlp, text):
    # input: parser, text, writing path
    # output: 
    text = text.strip()
    # text = text.lower()
    doc = nlp(text)
    sents = list(doc.sents)

    sent_dict_list = []
    for sent in sents:
        # print(sent._.parse_string)
        sent_tree = construct_constituency_tree_from_string(sent._.parse_string)
        sent_dict = traverse_tree(sent_tree)
        sent_dict_list.append(sent_dict)
        # print(sent_dict)
    return sent_dict_list

def save_tree_dict(nlp, texts_dict, dst_path):
    for text_id in tqdm.tqdm(texts_dict):
        w_folder = os.path.join(dst_path, text_id)
        if not os.path.exists(w_folder):
            os.makedirs(w_folder)
        for t_id, text in enumerate(texts_dict[text_id]):
            w_file = os.path.join(w_folder, str(t_id).zfill(3) + '.json')
            dict_list = get_tree_from_sentence(nlp, text)
            write_tree_list_file(w_file, dict_list)


if __name__ == "__main__":
    import sys


    file_name = TEXT2SHAPE_PATH
    dst_path = PARSED_TREE_DICT_PATH

    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)

    # read text2shape csv file
    texts_dict, texts = get_all_valid_data_text2shape(file_name)
    # texts = ['A lounge or sofa chair.It is double cushion chair.It is grey and golden colour.The back rest is very spacious.']
    
    # parse csv file
    parser = get_BerkeleyNeuralParser()
    # parse_sentence_to_tree(parser, texts[0])
    save_tree_dict(parser, texts_dict, dst_path)