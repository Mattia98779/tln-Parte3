import pandas as pd
from nltk.corpus import wordnet as wn
import re

def hyponyms_lvl(synset, lvl):
    hyponyms = []
    if lvl == 0:
        return []
    else:
        app = synset.hyponyms()
        for s in app:
            hyponyms.append(s)
            hyponyms+=hyponyms_lvl(s, lvl-1)
    return hyponyms

def create_context (frase):
    frase = list(set(frase).difference(no_words))
    ctx_lemmas = []
    for w in frase:
        ctx_lemmas.append(wn.morphy(w.lower()))
    ctx_lemmas2 = list(filter(lambda x: x != None, ctx_lemmas))
    return set(ctx_lemmas2)

def lesk(candidates, context):
    best_sense = candidates[0]
    max_overlap = 0
    context = set(context)
    for sense in candidates:
        signature = []
        #for example in sense.examples():
        #    signature = signature + example.split()
        for glos in sense.definition().split():
            signature = signature + re.sub(r"[^a-zA-Z0-9]","",glos).split()
        signature = set(signature)
        filtered = create_context(signature)
        overlap = len(filtered.intersection(context))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense
    return best_sense

def preprocessing (frase):
    frase = list(set(re.sub(r"[^a-zA-Z0-9 ]", "", frase).split()).difference(no_words))
    ctx_lemmas = []
    for w in frase:
        lemma = wn.morphy(w.lower())
        if lemma == None:
            ctx_lemmas.append(w.lower())
        else:
            ctx_lemmas.append(lemma)
    return set(ctx_lemmas)

# lettura stop words
file3 = open('stop_words_FULL.txt', 'r')
Lines3 = file3.readlines()
no_words = []
for line in Lines3:
    no_words.append(line[:len(line)-1])
no_words = set(no_words)

# lettura definizioni
df = pd.read_csv ('defs.csv')
# courage, paper, apprehension, sharpener
defs = [[],[],[],[]]
for i in df.itertuples():
    defs[0].append(preprocessing(i[2]))
    defs[1].append(preprocessing(i[3]))
    defs[2].append(preprocessing(i[4]))
    defs[3].append(preprocessing(i[5]))

for def_list in defs:
    words = {}
    context = []
    for definizione in def_list:
        for word in definizione:
            if words.keys().__contains__(word):
                words[word] += 1
            else:
                words[word] = 1
    ordered = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
    frequent_words = list(ordered.keys())[:5]
    app_synsets = []
    for fw in frequent_words:
        app_synsets += wn.synsets(fw)
    app_synsets = set(app_synsets)
    candidate_synsets = []
    for s in app_synsets:
        candidate_synsets += hyponyms_lvl(s, 5)
    sense = lesk(candidate_synsets, list(ordered.keys())[:5])
    print(sense)