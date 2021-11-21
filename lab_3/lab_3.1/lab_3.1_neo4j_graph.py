import re

from neo4j import GraphDatabase
import pandas as pd
from nltk.corpus import wordnet as wn

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("test", "test"))


def add_rel(tx, source, target, rel_name):
    tx.run(
        "MERGE (s:Term {name: $sub})"
        "MERGE (o:Term {name: $obj})"
        "MERGE (s)-[:" + rel_name.replace(" ", "_") + "]->(o)",
        sub=source, obj=target)


def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])



with driver.session() as session:

    input = pd.read_csv("datapippo.csv")
    c=0
    for row in input.itertuples():
        sogg = re.sub('[^A-Za-z0-9 ]+', '', row[2])
        ogg = re.sub('[^A-Za-z0-9 ]+', '', row[3])
        if (sogg != "" and ogg != ""):
            session.write_transaction(add_rel, sogg, ogg, 'NEXT')
driver.close()

