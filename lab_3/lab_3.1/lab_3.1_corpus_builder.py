from nltk.corpus import brown
import spacy
from nltk.wsd import lesk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from nltk.corpus import wordnet as wn

l = brown.sents()
sentences = []
for s in l[:100]:
    if s != None:
        sentences.append(s)
print("n frasi= ", len(sentences))
tot = 0
source = []
target = []

for s in tqdm(sentences):
    for word in range(1, len(s)):
        source_lemma = wn.morphy(s[word-1])
        if source_lemma != None:
            source.append(source_lemma.lower())
        else:
            source.append(s[word-1].lower())
        target_lemma = wn.morphy(s[word])
        if target_lemma != None:
            target.append(target_lemma.lower())
        else:
            target.append(s[word].lower())

pippo = np.asarray([source, target])
pluto = pd.DataFrame(pippo).T
paperino = pluto.loc[(pluto[0] != '') & (pluto[1] != '') & (pluto[0] != ' ') & (pluto[1] != ' ')]
paperino.to_csv("datapippo.csv")