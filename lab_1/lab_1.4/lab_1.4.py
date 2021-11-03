from nltk.corpus import brown
import spacy
nlp = spacy.load('en_core_web_sm')
a = ["give", "gives", "gave", "given", "giving"]
l = brown.sents()
sentens = []
for s in l:
    if s != None:
        if any(verb in s for verb in a):
            sentens.append(s)

doc = nlp(str(sentens[0]))
for sent in doc:
    for token in sent:
        if token.is_alpha:
            print (token.orth_, token.tag_, token.head.lemma_)