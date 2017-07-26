import networkx as nx
import csv
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

def generate_graph(session):
    raw = globeVar.VAR_PATH_RESULT_FOLDER+"/"+session + "/input_protein_ids.txt"
    ff = open(raw)
    nodes = []
    for line in ff:
        nodes.extend(line.replace("\n","").split(","))
    print("nodes=",nodes)
    des = globeVar.VAR_PATH_RESULT_FOLDER+"/"+session + "/network.gexf"
    G = load_graph(globeVar.VAR_PATH_IREFWEB_ALL)
    H = sub_graph(G, nodes)
    nx.write_gexf(H,des)


if __name__ == '__main__':
    '''
    '''
    G = load_graph("." + globeVar.VAR_PATH_IREFWEB_ALL)
    nodes = random.sample(G.nodes(), 100)
    print(nodes)
    H = sub_graph(G, nodes)
    # save as gexf file
    nx.write_gexf(H,"../data/test_data/test.gexf")
    print(H.edges())