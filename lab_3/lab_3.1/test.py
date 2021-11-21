import re
import pandas as pd
import spacy
from spacy.matcher import Matcher
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from spacy import displacy
import numpy as np
from nltk.corpus import brown
import re
from neo4j import GraphDatabase
import pandas as pd


def get_entities(sent):
    ## chunk 1
    ent1 = ""
    ent2 = ""

    prv_tok_dep = ""  # dependency tag of previous token in the sentence
    prv_tok_text = ""  # previous token in the sentence

    prefix = ""
    modifier = ""

    #############################################################

    for tok in nlp(sent):
        ## chunk 2
        # if token is a punctuation mark then move on to the next token
        if tok.dep_ != "punct":
            # check: token is a compound word or not
            if tok.dep_ == "compound":
                prefix = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " " + tok.text

            # check: token is a modifier or not
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " " + tok.text

            ## chunk 3
            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""

                ## chunk 4
            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text

            ## chunk 5
            # update variables
            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text
    #############################################################

    return [ent1.strip(), ent2.strip()]


def get_relation(sent):
    doc = nlp(sent)

    # Matcher class object
    matcher = Matcher(nlp.vocab)

    # define the pattern
    pattern = list(
        [list([{'DEP': 'ROOT'}, {'DEP': 'prep', 'OP': "?"}, {'DEP': 'agent', 'OP': "?"}, {'POS': 'ADJ', 'OP': "?"}])])

    matcher.add("matching_1", pattern)

    matches = matcher(doc)
    k = len(matches) - 1

    span = doc[matches[k][1]:matches[k][2]]

    return (span.text)


def creaStr(frase):
    test = ''
    for word in frase:
        test += " " + word.lower()
    return test


def print_rel(tx, verb, ogg):
    #print("domanda =", verb, ogg)
    for record in tx.run("MATCH (n:Term)-[:" + verb.replace(" ","_") + "]->(co) where co.name = $oggetto RETURN (n.name)", oggetto=ogg):
        print("risposta =", record[0], verb, ogg)


nlp = spacy.load('en_core_web_sm')
# candidate_sentences2 = pd.read_csv("/content/wiki_sentences_v2.csv")
# candidate_sentences.shape


continua = True
while continua:
    question = input("Inserire la domanda: ")
    if question == "exit":
        break
    candidate_sentences = [question]
    entity_pairs = []
    for i in candidate_sentences:
        entity_pairs.append(get_entities(i))

    relations = [get_relation(i) for i in candidate_sentences]
    source = [i[0] for i in entity_pairs]
    # extract object
    target = [i[1] for i in entity_pairs]
    kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
    G = nx.from_pandas_edgelist(kg_df, "source", "target",
                                edge_attr=True, create_using=nx.MultiDiGraph())
    driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("test", "test"))
    with driver.session() as session:
        session.read_transaction(print_rel, relations[0], target[0])
    driver.close()

print("FINITO")
