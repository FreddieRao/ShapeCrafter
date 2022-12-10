import benepar, spacy
# NLP = spacy.load("en_core_web_md", exclude=["parser"])
# NLP.enable_pipe("senter")
NLP = spacy.load("en_core_web_md")

STOP_WORD = [' ', '  ', ';', 'table', "'d", "'ll", "'m", "'re", "'s", "'ve", 
'a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 
'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'bottom', 'but', 'by', 
'ca', 'call', 'can', 'cannot', 'could', 'did', 'do', 'does', 'doing', 'done', 'down', 'due', 'during', 
'each', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fifty', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 
'had', 'has', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i', 'if', 'in', 'indeed', 'into', 'is', 'it', 'its', 'itself', 'just', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 
'made', 'make', 'many', 'may', 'me', 'meanwhile', 'might', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', "n't", 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'n‘t', 'n’t', 
'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'quite', 
'rather', 're', 'really', 'regarding', 'same', 'say', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 
'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 
'under', 'unless', 'until', 'up', 'upon', 'us', 'used', 'using', 'various', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 
'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', '‘d', '‘ll', '‘m', '‘re', '‘s', '‘ve', '’d', '’ll', '’m', '’re', '’s', '’ve'
]

RELS = [
    'S', # T: (S (NP-SBJ Casey) (VP threw (NP the ball)))
    'SINV', # T: Marching past the reviewing stand were 500 musicians
    'SBAR', # T: (S (NP-SBJ (NP The person)(SBAR (WHNP-1 who)(S (NP-SBJ *T*-1)(VP threw(NP the ball)))))
    'RRC', # T: (reduced relative clause)
    'SBARQ', # T: wh-questions
    'SQ', # T: Other kinds of question. 
    'FRAG', # F: Fragements
    'ADJP', # T: Adjective Phrase
    'ADVP', # T: Adverb Phrase
    'CONJP', # T: as well as
    'INTJ', # F: Interjection
    'LST', # T: List marker
    'NP', # T: Noun Phrase
    'PP', # T: Prepositional Phrase
    'PRN', # T: Parenthetical.
    'PRT', # F: Particle
    'QP', # F: always come with NP
    'UCP', # T: Coordination of unlike syntactic categories 
    'VP', # T: Verb
    'WHADVP', # F: Wh-adverb Phrase
    'WHNP', # F: Wh-noun Phrase
    'WHPP', # F: Wh-prepositional Phrase.
    'NML', # F: mark internal NP structure
    'X', # F: Unknown, uncertain, or unbracketable.
    #--------Not in the dataset
    'S-CLF', # T: Declarative it -clefts
    # it -extraposition
    'NAC', # T: Not A Constituent
    'NX', # T:  Used within certain complex noun phrases to mark the head of the noun phrase
    'WHADJP', # F: Wh-adjective Phrase
]

def label_is_benepar_valid(label):
    VALID_RELS = [
        'S', # T: (S (NP-SBJ Casey) (VP threw (NP the ball)))
        'SINV', # T: Marching past the reviewing stand were 500 musicians
        'SBAR', # T: (S (NP-SBJ (NP The person)(SBAR (WHNP-1 who)(S (NP-SBJ *T*-1)(VP threw(NP the ball)))))
        'RRC', # T: (reduced relative clause)
        'SBARQ', # T: wh-questions
        'SQ', # T: Other kinds of question. 
        'ADJP', # T: Adjective Phrase
        'ADVP', # T: Adverb Phrase
        'CONJP', # T: as well as
        'LST', # T: List marker
        'NP', # T: Noun Phrase
        'PP', # T: Prepositional Phrase
        'PRN', # T: Parenthetical.
        'UCP', # T: Coordination of unlike syntactic categories 
        'VP', # T: Verb
        'S-CLF', # T: Declarative it -clefts
        'NAC', # T: Not A Constituent
        'NX', # T:  Used within certain complex noun phrases to mark the head of the noun phrase
    ]
    return label in VALID_RELS

def label_is_pos_special(label):
    INSIG_POS = [
        'CC', # coordinating conjunction
        'IN', # preposition/subordinating conjunction
        'FW', # foreign word
        'X',  # Mis Type
        'SYM', # Symbol
        'SPACE' # Space
    ]
    return label in INSIG_POS

def label_is_pos_punct(label):
    punct = [
    '``', 
    '.', 
    '"', 
    ':', 
    ',',
    # '-LRB-', 
    # '-RRB-', 
    ]
    return label in punct

def label_is_conjuction(label):
    CONJ_LABEL = [
    'CONJP', 
    'CC', 
    'IN', 
    'SPACE', 
    ]
    return label in CONJ_LABEL

def is_stopwords_phrase(phrase):
    is_stopword = True
    for word in NLP(phrase):
        is_stopword &= (word.text.lower() in STOP_WORD)
    return is_stopword

def get_BerkeleyNeuralParser():
    nlp = spacy.load('en_core_web_md')
    # nlp = spacy.load("en_core_web_md", exclude=["parser"])
    # nlp.enable_pipe("senter")
    # nlp.add_pipe("merge_punct")
    nlp.add_pipe('benepar', config={'model': 'benepar_en3_large'})
    return nlp

def get_RobertaEncoder():
    import spacy_sentence_bert
    nlp = spacy_sentence_bert.load_model('en_stsb_roberta_base')
    # nlp.remove_pipe("sentencizer")
    return nlp

def get_SentenceTransformer():
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('sentence-transformers/stsb-roberta-large')
    print('Model Loaded!')
    return model
    
if __name__ == "__main__":
    list_a = ['It ', ' table ']
    for phrase in list_a:
        is_stopword = is_stopwords_phrase(phrase)
        print(is_stopword)