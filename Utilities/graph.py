import networkx as nx
from networkx.readwrite import  json_graph
import csv
import json
import random
import globeVar

# this script is used to generate networks based on protein paires.

def load_graph(gpath):
    '''
    '''

    with open(gpath, 'rb') as inputfile:
        results = list(csv.reader(inputfile, delimiter='\t'))

    G = nx.Graph()
    G.add_edges_from(results)

    return G


def sub_graph(G, nodes):
    '''
    '''

    return G.subgraph(nodes)

def generate_graph(session,dtype="json"):
    raw = globeVar.VAR_PATH_RESULT_FOLDER+"/"+session + "/input_protein_ids.txt"
    ff = open(raw)
    nodes = []
    for line in ff:
        nodes.extend(line.replace("\n","").split(","))
    G = load_graph(globeVar.VAR_PATH_IREFWEB_ALL)
    H = sub_graph(G, nodes)
    if dtype == "json":
        des = globeVar.VAR_PATH_RESULT_FOLDER+"/"+session + "/network.json"
        jsondata = convert2cytoscapeJSON(H)
        f = open(des ,"w")
        f.write(jsondata)
        f.close()
        return True
    elif dtype == "gexf":
        des = globeVar.VAR_PATH_RESULT_FOLDER+"/"+session + "/network.gexf"
        nx.write_gexf(H,des)
        return True
    else:
        return False

# this function is used to convert networkx to Cytoscape.js JSON format
# returns string of JSON
def convert2cytoscapeJSON(G):
    # load all nodes into nodes array
    final = {}
    final["nodes"] = []
    final["edges"] = [] 
    for node in G.nodes():
        nx = {}
        nx["data"] = {}
        nx["data"]["id"] = node
        nx["data"]["label"] = node
        final["nodes"].append(nx.copy())
    #load all edges to edges array
    for edge in G.edges():
        nx = {}
        nx["data"]={}
        nx["data"]["id"]=edge[0]+edge[1]
        nx["data"]["source"]=edge[0]
        nx["data"]["target"]=edge[1]
        final["edges"].append(nx)
    return json.dumps(final)

if __name__ == '__main__':
    '''
    '''
    G = load_graph("." + globeVar.VAR_PATH_IREFWEB_ALL)
    nodes = random.sample(G.nodes(), 100)
    #print(nodes)
    H = sub_graph(G, nodes)
    # save as gexf file
    nx.write_gexf(H,"../data/test_data/test.gexf")
    # save as json file
    print(" start tranfer nodes")
    dta = convert2cytoscapeJSON(H)
    f = open("../Cache/YoitE1s5FUmu6kxVNjMBPdR37bXhHrOIPx5Ut704X8mkYHv3150030118758/network.json","w")
    f.write(dta)
    f.close()