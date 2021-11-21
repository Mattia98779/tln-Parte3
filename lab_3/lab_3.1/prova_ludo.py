temp = brown.sents()[:1000]
candidate_sentences = []
for elem in temp:
  candidate_sentences.append(creaStr(elem))

nlp = spacy.load('en_core_web_sm')
#candidate_sentences2 = pd.read_csv("/content/wiki_sentences_v2.csv")
#candidate_sentences.shape
entity_pairs = []

for i in tqdm(candidate_sentences):
  entity_pairs.append(get_entities(i))

relations = [get_relation(i) for i in tqdm(candidate_sentences)]
source = [i[0] for i in entity_pairs]
# extract object
target = [i[1] for i in entity_pairs]
kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
G=nx.from_pandas_edgelist(kg_df, "source", "target",
                          edge_attr=True, create_using=nx.MultiDiGraph())


#plt.figure(figsize=(12,12))

#pos = nx.spring_layout(G)
#nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
#plt.show()

pippo = np.asarray([source,relations,target])
pluto = pd.DataFrame(pippo).T
paperino = pluto.loc[(pluto[0] != '') & (pluto[1] != '') & (pluto[2] != '') & (pluto[0] != ' ') & (pluto[1] != ' ') & (pluto[2] != ' ')]
paperino.to_csv("datapippo.csv")