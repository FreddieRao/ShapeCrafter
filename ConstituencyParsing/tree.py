from tags import *

class ConstituencyTree:
    def __init__(self):
        self.text = None
        self.label = None
        self.children = [] # list of tree
 
# This function is here just to test
def preOrder(node):
    if (node == None):
        return
    for child in node.children:
        preOrder(child)
 
def findIndex(Str, si, ei):
    if (si > ei):
        return -1
 
    # Inbuilt stack
    s = []
    for i in range(si, ei + 1):
        
        # if open parenthesis, push it
        if (Str[i] == '('):
            s.append(Str[i])
 
        # if close parenthesis
        elif (Str[i] == ')'):
            if (s[-1] == '('):
                s.pop(-1)
 
                # if stack is empty, this is
                # the required index
                if len(s) == 0:
                    return i
    # if not found return -1
    return -1
 
# function to conStruct tree from String
 
def merge_to_left_tree(left_tree, cur_node):
    # merge current node to left node, and update left node tree
    left_tree.text = left_tree.text + cur_node.text

    if len(left_tree.children) > 0:
        left_tree.children[-1] = merge_to_right_tree(left_tree.children[-1], cur_node)
    return left_tree

def merge_to_right_tree(right_tree, cur_node):
    # merge current node to right tree, and update right node tree
    right_tree.text = cur_node.text + right_tree.text
    if len(right_tree.children) > 0:
        right_tree.children[0] = merge_to_right_tree(right_tree.children[0], cur_node)

    return right_tree

def upgrade_with_left_tree(tree, left_tree, right_tree):
    # tree children = left grandchildern + right_tree
    new_children = []
    for grandchildern in left_tree.children:
        new_children.append(grandchildern)
    new_children.append(right_tree)

    tree.children = new_children

    return tree
    
def upgrade_with_right_tree(tree, right_tree, left_tree):
    # tree children = right grandchildern + left child
    new_children = [left_tree]
    for grandchildern in right_tree.children:
        new_children.append(grandchildern)

    tree.children = new_children

    return tree

# function to conStruct tree from String
 

def treeFromString(Str, si, ei):
    # Str: Whole String
    # si: index of left bracket
    # ei: index of right bracket
    # Base case
    
    if (si > ei):
        return None
 
    # new root, start with '('
    if Str[si] =='(':
        root = ConstituencyTree()
        root.label = Str[si+1: si+Str[si: ei+1].find(' ')] # label is between '(' & ' '
        root.text = ''
        lbr = si
        c_si = si+Str[si: ei+1].find(' ') + 1
    
    # find the index of its complement ')'
    rbr = findIndex(Str, si, ei)
    c_ei = rbr - 1

    # Create Leaf or SubTree
    if Str[c_si] != '(': # Leaf
        root.text = Str[c_si: c_ei+1].replace('-LRB-', '(').replace('-RRB-', ')') + ' '
    else:  # New SubTree
        lbr = c_si
        subtree_se_list = []
        while lbr < c_ei:
            rbr = findIndex(Str, lbr, c_ei)
            subtree_se_list.append((lbr, rbr))
            lbr = rbr + 2

        for subtree_se in subtree_se_list:
            s_si, s_ei = subtree_se
            # call for left subtree
            subtree = treeFromString(Str, s_si, s_ei)
            root.children.append(subtree)
            root.text += subtree.text
    return root

def treeFromDict(dict_input, node_str, sibling_text='', is_rightest=False, return_str=True, return_tree=True):
    
    node_texts = []
    node_phrases = []
    node_ids = []

    node = ConstituencyTree()
    node.label = dict_input['label']
    node.text = dict_input['text']
    node.children = []

    csibling_text = sibling_text
    for c_idx, child in enumerate(dict_input['children']):
        cnode_str = node_str + '-' + str(c_idx)
        if c_idx == len(dict_input['children']) - 1:
            cis_rightest = True
        # elif c_idx == len(dict_input['children']) - 2 and label_is_pos_punct(dict_input['children'][c_idx + 1]['label']):
        #     cis_rightest = True
        else:
            cis_rightest = False
        cnode, cnode_phrases, cnode_texts, cnode_ids = treeFromDict(child, cnode_str, csibling_text, cis_rightest, return_str, return_tree)
        
        csibling_text += child['text']
        if return_tree:
            node.children.append(cnode)

        if return_str:
            node_phrases += cnode_phrases
            node_texts += cnode_texts
            node_ids += cnode_ids
    
    if not is_rightest:
        if len(node_texts) > 0:
            cur_phrase = dict_input['text'].replace(node_texts[-1], '')
            
        else:
            cur_phrase = dict_input['text']
        node_phrases = node_phrases + [cur_phrase]
        node_texts = node_texts + [sibling_text + dict_input['text']]
        node_ids = node_ids + [node_str]
        
    return node, node_phrases, node_texts, node_ids

def construct_constituency_tree_from_string(str_input):
    # input: benepar parse_string
    # output: tree structure
    tree = treeFromString(str_input, 0, len(str_input)-1)
    return tree

def construct_constituency_tree_from_dict(dict_input):
    # input: benepar parse_string
    # output: tree structure
    node_str = '0'
    tree, tree_phrases, tree_texts, tree_ids = treeFromDict(dict_input, node_str=node_str, return_str=True, return_tree=True)
    return dict(
        tree=tree, 
        node_texts=tree_texts, 
        node_ids=tree_ids
    )

def construct_constituency_tree_from_dict_list(dict_list_input, consect_tree=False):
    # input: benepar parse_string
    # output: tree structure
    org_tree_ids = list(range(len(dict_list_input)))
    tree_list = []
    node_phrases_list = []
    node_texts_list = []
    node_ids_list = []
    start_tree_idx_list = []
    cur_tree_idx_list = []

    for s_idx in range(len(dict_list_input)):
        
        sibling_text = ''
        tree_ids = org_tree_ids[s_idx:] + org_tree_ids[:s_idx]
        cur_dict_list_input = dict_list_input[s_idx:] + dict_list_input[:s_idx]

        for t_idx, dict_input in enumerate(cur_dict_list_input):
            node_str = '0'
            tree, tree_phrases, tree_texts, tree_node_ids = treeFromDict(dict_input, node_str=node_str, sibling_text=sibling_text, is_rightest=False, return_str=True, return_tree=True)
            if consect_tree:
                sibling_text = tree_texts[-1]
            
            if s_idx == 0:
                tree_list.append(tree)
            
            node_phrases_list += tree_phrases
            node_texts_list += tree_texts
            node_ids_list += tree_node_ids
            start_tree_idx_list += [s_idx] * len(tree_texts)
            cur_tree_idx_list += [tree_ids[t_idx]] * len(tree_texts)
        
        if not consect_tree:
            break

    return dict(    
        tree_list=tree_list, 
        node_phrases_list=node_phrases_list, 
        node_texts_list=node_texts_list, 
        node_ids_list=node_ids_list,
        start_tree_idx_list=start_tree_idx_list,
        cur_tree_idx_list=cur_tree_idx_list
    )

if __name__ == "__main__":
    input_str = '(NP (NP (JJ modern) (NN chair)) (PP (IN with) (NP (NP (NP (JJ    ) (JJ red) (JJ cubic) (NN base)) (-LRB- -LRB-) (NP (DT no) (NNS legs)) (-RRB- -RRB-)) (CC and) (NP (NP (JJ black) (JJ rectangular) (NN back)) (PP (IN with) (NP (NP (DT a) (JJ parabolic) (NN shape)) (VP (VBG attaching) (PP (IN to) (NP (NP (DT the) (NN bottom)) (PP (IN of) (NP (DT the) (NN base))))))))))) (. .))'
    input_dict_list = [{"text": "the chair is very decorative , and can be used as a dining room table chair . ", "label": "S", "children": [{"text": "the chair is very decorative , and can be used as a dining room table chair ", "label": "VP", "children": [{"text": "the chair is very decorative ", "label": "VP", "children": []}, {"text": ", ", "label": ",", "children": []}, {"text": "and can be used as a dining room table chair ", "label": "VP", "children": []}]}, {"text": ". ", "label": ".", "children": []}]}]
    construct_constituency_tree_from_dict_list(input_dict_list)
