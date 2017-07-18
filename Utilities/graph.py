import networkx as nx
import csv
import random
import globeVar

# this script is used to generate networks based on protein paires.

irefweb_all_path = globeVar.VAR_PATH_IREFWEB_ALL

def load_graph():
    '''
    '''

    with open(irefweb_all_path, 'rb') as inputfile:
        results = list(csv.reader(inputfile, delimiter='\t'))

    G = nx.Graph()
    G.add_edges_from(results)

    return G


def sub_graph(G, nodes):
    '''
    '''

    return G.subgraph(nodes)


if __name__ == '__main__':
    '''
    '''
    irefweb_all_path = "../data/irefweb_all.pos"
    G = load_graph()
    nodes = random.sample(G.nodes(), 100)
    H = sub_graph(G, nodes)
    # save as gexf file
    nx.write_gexf(H,"../data/test_data/test.gexf")
    print(H.edges())