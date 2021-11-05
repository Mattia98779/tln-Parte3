from nltk.corpus import brown
import spacy
from nltk.wsd import lesk
import matplotlib.pyplot as plt
import numpy as np

nlp = spacy.load('en_core_web_sm')
transitive_verb =['make','made','making','makes']
l = brown.sents()
sentences = []
for s in l:
    if s != None:
        if any(verb in s for verb in transitive_verb):
            sentences.append(s)
print("n frasi= ", len(sentences))
tot = 0
# soggetto, oggetto
soggetti = []
oggetti = []
for sentence in sentences:
    test = ""
    for word in sentence:
        test += " " + word
    #print(test)
    doc = nlp(test)
    trovato = 0
    soggetto = None
    oggetto = None
    verbo = None
    for token in doc:
        if token.text in transitive_verb:
            verbo = token
            #print("verbo = ",token.text, token.dep_)
            for child in token.children:
                if child.dep_=="dobj":
                    soggetto = child
                    #print("complemento oggetto = ", child.text, child.dep_)
                if child.dep_ == "nsubj" or child.dep_=="nsubjpass":
                    oggetto = child
                    #print("soggetto = ", child.text, child.dep_)
    if soggetto != None:
        sog = lesk(sentence, soggetto.text)
        if not (isinstance(sog, type(None))):
            soggetti.append(sog.lexname().split(".")[1])
    if oggetto != None:
        ogg = lesk(sentence,oggetto.text)
        if not(isinstance(ogg, type(None))):
            oggetti.append(ogg.lexname().split(".")[1])

#clusterizzazione
dictSog = {}
for sog in soggetti:
    if sog in dictSog.keys():
        dictSog[sog] = dictSog[sog] + 1
    else:
        dictSog[sog] = 1
ordered_sog = dict(sorted(dictSog.items(), key=lambda item: item[1], reverse=True))
print(ordered_sog)

dictOgg = {}
for og in oggetti:
    if og in dictOgg.keys():
        dictOgg[og] = dictOgg[og] + 1
    else:
        dictOgg[og] = 1
ordered_ogg = dict(sorted(dictOgg.items(), key=lambda item: item[1], reverse=True))
print(ordered_ogg)

# grafico a torta, soggetti
plt.title("Soggetti")
plt.pie(list(ordered_sog.values())[:10], labels = list(ordered_sog.keys())[:10], autopct='%1.2f%%')
plt.show()

# grafico a torta, oggetti
plt.title("Oggetti")
plt.pie(list(ordered_ogg.values())[:10], labels = list(ordered_ogg.keys())[:10], autopct='%1.2f%%')
plt.show()

#grafici a barre
plt.title("Oggetti")
plt.bar(list(map(lambda x: x[:5],list(ordered_ogg.keys())))[:8], list(map(lambda x: x/len(oggetti)*100,list(ordered_ogg.values())))[:8], color='g')
plt.show()
plt.title("Soggetti")
plt.bar(list(map(lambda x: x[:5],list(ordered_sog.keys())))[:8], list(map(lambda x: x/len(soggetti)*100,list(ordered_sog.values())))[:8], color='g')
plt.show()

