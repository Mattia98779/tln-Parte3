import re
from nltk.corpus import wordnet as wn

def blue(filtered, gold):
    gold_terms = []
    for el in gold:
        gold_terms.append(el[:len(el)-1])
    candidate_terms = []
    for el in filtered:
        candidate_terms += re.sub(r"[^a-zA-Z0-9 ]", "", el[0]).lower().split(" ")
    candidate_terms = set(candidate_terms).difference(no_words)
    blue = len(set(gold_terms).intersection(candidate_terms)) / len(set(candidate_terms))
    return blue

def rogue(filtered, gold):
    gold_terms = []
    for el in gold:
        gold_terms.append(el[:len(el) - 1])
    candidate_terms = []
    for el in filtered:
        candidate_terms += re.sub(r"[^a-zA-Z0-9 ]", "", el[0]).lower().split(" ")
    candidate_terms = set(candidate_terms).difference(no_words)
    rogue = len(set(gold_terms).intersection(candidate_terms)) / len(set(gold_terms))
    return rogue

def get_vect_from_term(term):
    vets = []
    all_ids = term_to_id[term]
    for id in all_ids:
        if id in dict_vet.keys():
            vets.append(dict_vet[id])
    return vets



def weigthed_overlap(v1,v2):
    v1_filt = list(map(lambda x: x.split("_")[0], v1))
    v2_filt = list(map(lambda x: x.split("_")[0], v2))
    commons = set(v1_filt).intersection(set(v2_filt))
    i =  1
    nom = 0
    denom = 0
    for elem in commons:
        rank1 = v1_filt.index(elem)+1
        rank2 = v2_filt.index(elem)+1
        nom += pow(rank1+rank2,-1)
        denom += pow(2*i,-1)
        i += 1

    return nom/denom if denom != 0 else 0


def disambiguazione (context, dup):
    best_sense = dup[0][2:]
    max_overlap = 0
    for current in dup:
        for l in Lines4:
            pippo = l.split("\t")[0]
            if current[0] == pippo:
                signature = re.sub(r"[^a-zA-Z0-9 ]", "", l.split("\t")[1]).split()
                signature = set(signature)
                overlap = len(signature.intersection(context))
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_sense = current[1:]
    return best_sense


def unify_vet (vettori):
    vet = []
    for v in vettori:
        for el in v:
            if (el == ""):
                print(2)
            vet.append(el)
    #prendo la seconda parte del termine nasari e ordino in base al suo valore
    vet.sort(key= lambda x: float(x.split("_")[1]),reverse=True)
    return vet

def create_context_titolo(frase):
    vettori = create_context(frase)
    final = vettori
    frase = ""
    final = list(map(lambda x: x.split("_")[0], final))
    for s in final:
        frase += " "+s
    return create_context(frase)

def create_context (frase):
    frase = re.sub(r"[^a-zA-Z0-9 ]", "", frase).lower().split(" ")
    frase = list(set(frase).difference(no_words))
    vettori = []
    for w in frase:
        dup_vet = get_vect_from_term(w)
        if (len(dup_vet)>1):
            vettori.append(disambiguazione(frase, dup_vet))
        elif (len(dup_vet)==1):
            vettori.append(dup_vet[0][2:])
    return unify_vet(vettori)

def selectTopic(paragraph):
    topic = ""
    for p in paragraph:
        for sentence in p.split("."):
            if len(set(sentence.lower().split(" ")).intersection(set(cues_words))) > 0:
                topic = topic +" "+sentence
    return topic


#leggo i file
file2 = open('utils/NASARI_vectors/dd-small-nasari-15.txt', encoding="utf8")
Lines2 = file2.readlines()
file3 = open('utils/stop_words_FULL.txt', 'r')
Lines3 = file3.readlines()
file4 = open('utils/babelnet.txt', encoding="utf8")
Lines4 = file4.readlines()
file5 = open('utils/cues_words.txt', encoding="utf8")
cues_words = file5.readlines()
cues_words = list(map(lambda x: x[:len(x)-1].lower(), cues_words))
no_words = []
testi = ['Andy-Warhol.txt','Ebola-virus-disease.txt','Life-indoors.txt','Napoleon-wiki.txt','Trump-wall.txt']
for line in Lines3:
    no_words.append(line[:len(line)-1])
no_words = set(no_words)
dict_vet = {}
term_to_id = {}
file6 = open('utils/term_to_id', encoding="utf8")
lines6 = file6.readlines()
word = "###"
ids = []
for l in lines6:
    if l[0]=="#":
        term_to_id[word]=ids
        word = l[1:len(l)-1]
        ids = []
    else:
        ids.append(l[:len(l)-1])


# 1=title - 2=cue word
metodo_riassunto = 1

for l in Lines2:
    elems = l.split(';')
    elems = list(filter(lambda a: a != '' and a !='\n', elems))
    dict_vet[elems[0]]= elems[2:]

for text in testi:
    titolo = []
    i = 0
    file1 = open('utils/docs/'+text, encoding="utf8")
    Lines = file1.readlines()
    while len(titolo)<=0 :
        if (Lines[i][0] != '#' and Lines[i][0]!='\n'):
            titolo = Lines[i]
        i=i+1
    paragraph = []
    for l in Lines:
        if (l[0] != '#' and l[0]!='\n'):
            paragraph.append(l)
    if metodo_riassunto==1:
        topic = create_context_titolo(titolo)
    else:
        topic = create_context(selectTopic(paragraph))
    val = 0
    final = []


    for p in paragraph:
        p_context = create_context(p)
        wo_val = weigthed_overlap(topic,p_context)
        final.append([p, p_context,wo_val])
    final_temp = final
    final_temp.sort(key= lambda x: x[2],reverse=True)
    perc=[10,20,30]
    file = open("utils/riassunti/"+text+"_short", "w")
    for size in perc:
        file.write("Riassunto con"+str(size)+"%:\n")
        calcolo = int(len(final_temp) - len(final_temp) * size / 100)
        filtered = final_temp[:calcolo]
        for elem in final:
            if elem in filtered:
                file.write(elem[0])
        gold = open('utils/reference_summary/' + text + '_reference', encoding="utf8")
        lines = gold.readlines()
        print (text+ " Riassunto %= "+str(size))
        print ("blue = "+str(blue(filtered, lines)))
        print ("rogue = "+str(rogue(filtered, lines))+"\n")