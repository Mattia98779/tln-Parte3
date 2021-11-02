import pandas as pd
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
import numpy as np

# lettura elenco di parole, e ottenimento synsets
data = pd.read_csv("WordSim353.csv", sep =',')
words = set(data["Word 1"].to_numpy().tolist())
synsets = []
for w in words:
    synsets += (wn.synsets(w))
data = set(synsets)

# studio della forma: lunghezza delle definizioni
lens = {}
for s in synsets:
    l = len(s.definition().split())
    if lens.keys().__contains__(l):
        lens[l] += 1
    else:
        lens[l] = 1
ordered = dict(sorted(lens.items(), key=lambda item: item[0]))
fig, ax = plt.subplots()
ax.plot(ordered.keys(), ordered.values(), label='linear')
ax.set_xlabel('lunghezza definizione')
ax.set_ylabel('conteggio')
ax.set_title("Studio Forma")
ax.legend()
plt.show()

#studio del contenuto: generico o specifico
profondita = {}
for s in synsets:
    definition = s.definition().split()
    p = 0
    count = 0
    for w in definition:
        senses = wn.synsets(w)
        for s in senses:
            p+=s.max_depth()
            count +=1
    depth =int(p / count)
    if profondita.keys().__contains__(depth):
        profondita[depth] += 1
    else:
        profondita[depth] = 1
ordered = dict(sorted(profondita.items(), key=lambda item: item[0]))
fig, ax = plt.subplots()
ax.plot(ordered.keys(), ordered.values(), label='linear')
ax.set_xlabel('profondità media')
ax.set_ylabel('conteggio')
ax.set_title("Studio Contenuto")
ax.legend()
plt.show()
print(1)