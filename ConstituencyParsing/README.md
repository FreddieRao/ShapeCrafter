## Text2Shape++ Dataset

- Download [Text2Shape](http://text2shape.stanford.edu/) dataset.
- Change the paths in `paths.py`.
- Install required libraries:

```
pip install benepar spacy
```

- Running the processing scripts:

```bash
# Parse each sentence in phrases
python 0_Sentence2Tree.py
# Collect phrase sequences
python 1_Tree2ValidPhrase.py
# Calculate semantic similarity between phrases.
# This is a multiprocessing script, and takes a long time to run. See the comments in the script for how to setting start_id and end_id.
python 2_CalculatePhraseSimilarity.py stard_id end_id
# Collect similar phrase sequences
python 3_SimilarityTree.py
# Collect valid phrase sequences
python 4_SeqentialPhrase.py
```