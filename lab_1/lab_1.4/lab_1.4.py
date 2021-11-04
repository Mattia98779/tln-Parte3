from nltk.corpus import brown
import spacy
from nltk.wsd import lesk
from spacy import displacy
from spacy.symbols import nsubj, VERB

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
# frase, soggetto, verbo, oggetto
frasi = []
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
                    trovato +=1
                if child.dep_ == "nsubj" or child.dep_=="nsubjpass":
                    oggetto = child
                    #print("soggetto = ", child.text, child.dep_)
                    trovato +=1
    if trovato==2:
        tot+=1
        print(tot)
        frasi.append([sentence,soggetto,verbo,oggetto])
print(frasi[0])
senso = lesk(frasi[0][0], frasi[0][1].text)
print(senso)
print(senso.lexname())
