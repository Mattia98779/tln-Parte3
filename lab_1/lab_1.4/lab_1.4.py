from nltk.corpus import brown
a = ["give", "gives", "gave"]
l = brown.sents()
c=0
for s in l:
    if s != None:
        if a[0] in s or a[1] in s or a[2] in s:
            c+=1
print(c)