import pandas as pd
from nltk.corpus import wordnet as wn
import re

def similarity_score (def1, def2):
    score = len(def1.intersection(def2)) / max(len(def1), len(def2))
    return score

# lemmatizzazione e filtraggio stopwords
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

# calcolo similarità
similartys = []
for def_list in defs:
    result = 0
    count = 0
    for i in range(0,len(def_list)-1):
        for j in range(i+1, len(def_list)):
            result += similarity_score(def_list[i], def_list[j])
            count=count+1
    similartys.append(result/count)

# stampa similarità
print("courage = " + str(similartys[0]))
print("paper = " + str(similartys[1]))
print("apprehension = " + str(similartys[2]))
print("sharpner = " + str(similartys[3]))




