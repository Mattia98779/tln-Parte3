import re
import requests

import requests
no_words = []
file3 = open('utils/stop_words_FULL.txt', 'r')
Lines3 = file3.readlines()
for line in Lines3:
    no_words.append(line[:len(line)-1])
no_words = set(no_words)

all_words = set([])
testi = ['Andy-Warhol.txt','Ebola-virus-disease.txt','Life-indoors.txt','Napoleon-wiki.txt','Trump-wall.txt']
for text in testi:
    file1 = open('utils/docs/'+text, encoding="utf8")
    Lines = file1.readlines()
    for l in Lines:
        frase = re.sub(r"[^a-zA-Z0-9 ]", "", l).lower().split(" ")
        frase = list(set(frase).difference(no_words))
        all_words = all_words.union(frase)

print(len(all_words))
all_words = list(all_words)
file_out = open("utils/term_to_id", "w")
for w in all_words[:800]:
    r = requests.get(
        'https://babelnet.io/v6/getSynsetIds?lemma=apple&searchLang=EN&key=79fe0280-58ce-4cb6-81b1-f6fd68fa31e1')
    r = r.json()
    file_out.write("#"+w+"\n")
    for id in r:
        file_out.write(id["id"]+"\n")

print("1")
for w in all_words[800:1600]:
    r = requests.get(
        'https://babelnet.io/v6/getSynsetIds?lemma=apple&searchLang=EN&key=8649f3f9-76bd-4c96-8c78-d9db29cd97ec ')
    r = r.json()
    file_out.write("#"+w+"\n")
    for id in r:
        file_out.write(id["id"]+"\n")

print("2")
for w in list(all_words)[1600:]:
    r = requests.get(
        'https://babelnet.io/v6/getSynsetIds?lemma=apple&searchLang=EN&key=ca7295f6-732a-43f9-b8d1-28c234d18eef ')
    r = r.json()
    file_out.write("#"+w+"\n")
    for id in r:
        file_out.write(id["id"]+"\n")

#

#

