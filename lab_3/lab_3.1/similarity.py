from neo4j import GraphDatabase
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("test", "test"))


#Prendo tutti i nodi
def get_Allnodes(tx):
    nodes=[]
    result = tx.run(
        "MATCH (n:Term) RETURN n.name"
    )
    for elem in result:
        nodes.append(elem[0])
    return nodes
#


# Prendo relazioni entranti
def left_rel(tx, target):
    left = []
    result = tx.run(
        "MATCH (s:Term {name: $obj})"
        "MATCH (w:Term)-[:NEXT]->(s)"
        "RETURN w.name as name",
        obj=target)
    for elem in result:
        left.append(elem[0])
    return left
#Prendo relazioni in uscita
def right_rel(tx, target):
    right = []
    result= tx.run(
        "MATCH (s:Term {name: $obj})"
        "MATCH (w:Term)<-[:NEXT]-(s)"
        "RETURN w.name as name",
        obj=target)
    for elem in result:
        right.append(elem[0])
    return right

def jaccard(a,b):
    a = set(a)
    b = set(b)
    intSize = len(a.intersection(b))
    unionSize = len(a.union(b))
    return intSize / unionSize if unionSize != 0 else 0

# we define paradigmatic similarity as the average of the Jaccard coefficents of the `left1` and `right1` sets
def paradigSimilarity(w1, w2,session):
    left1= session.read_transaction(left_rel,w1)
    left2= session.read_transaction(left_rel,w2)
    right1= session.read_transaction(right_rel,w1)
    right2=session.read_transaction(right_rel,w2)
    return (jaccard(left1, left2) + jaccard(right1, right2)) / 2.0

def add_sim(tx,sub,obj,sim):
    tx.run(
        "MERGE (s:Term {name: $sub})"
        "MERGE (o:Term {name: $obj})"
        "MERGE (s)-[r:SIM]->(o)  SET r.paradig = $sim;",
        sub=sub, obj=obj,sim=sim)

#print(paradigSimilarity("the", "was"))


with driver.session() as session:
    nodes = session.read_transaction(get_Allnodes)
    # for i in range(len(nodes)-1):
    #     for j in range(i+1,len(nodes)):
    #         sim = paradigSimilarity(nodes[i],nodes[j],session)
    #         print()
    #         session.write_transaction(add_sim,nodes[i],nodes[j],sim)
driver.close()
