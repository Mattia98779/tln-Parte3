import re

from neo4j import GraphDatabase
import pandas as pd
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("test", "test"))


def add_rel(tx, sub, obj , rel_name):
    print(sub)
    tx.run("MERGE (s:Term {name: $sub})"
           "MERGE (s)-[:"+rel_name.replace(" ","_")+"]->(o:Term {name: $obj})",
           sub=sub, obj=obj,)

with driver.session() as session:

    input = pd.read_csv("datapippo_test.csv")
    c=0
    for row in input.itertuples():
        sogg = re.sub('[^A-Za-z0-9 ]+', '', row[2])
        rel = re.sub('[^A-Za-z0-9 ]+', '', row[3])
        ogg = re.sub('[^A-Za-z0-9 ]+', '', row[4])
        if (sogg != "" and rel != "" and ogg != ""):
            session.write_transaction(add_rel, sogg, ogg ,rel)
driver.close()