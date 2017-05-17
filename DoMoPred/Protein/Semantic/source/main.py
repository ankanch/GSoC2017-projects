'''
Created on 2010-07-19

@author: Shobhit Jain

@contact: shobhit@cs.toronto.edu
'''
from ontology import GOGraph
import pickle
import os


def save_semantic_similarity(ontology_file, gene_file, ontology, code, gpath):
    '''
    Calls functions for loading and processing data.
    '''
    print gpath
    objs = {}
    ontology = ontology.split(",")
    g = GOGraph()
    onto_v = g._obo_parser(ontology_file)
    anno_v = g._go_annotations(gene_file, code)
    run = {'C': g._cellular_component, 'P': g._biological_process, 'F': g._molecular_function}
    ont = {'C': "Cellular Component", 'P': "Biological Process", 'F': "Molecular Function"}
    for i in ontology:
        fd = i + "-" + onto_v + "-" + anno_v + ".pck"
        if fd not in os.listdir(gpath):
            objs_file = open(gpath + "/%s" % (fd), "w")
            i = i.split(":")
            objs[i[0]] = run[i[0]]()
            objs[i[0]]._species()
            objs[i[0]]._clustering(float(i[1]))
            pickle.dump(objs[i[0]], objs_file)

    return objs


def load_semantic_similarity(CC, BP, MF):
    '''
    Calls functions for loading and processing data.
    '''
    objs = {}
    objs['C'] = pickle.load(open(CC))
    objs['P'] = pickle.load(open(BP))
    objs['F'] = pickle.load(open(MF))

    return objs


def return_details(result, geneA, geneB, detail):
    '''
    Formats the output for printing on screen or on file.
    '''
    domain_def = {'C':'Cellular Component', 'P':'Biological Process', 'F':'Molecular Function'}
    r = "\nSemantic similarity between " + geneA + " and " + geneB + " is:\n\n"
    for domain in result:
        r += " " + domain_def[domain] + ": " + str(result[domain][0]) + "\n"
        if detail:
            for data in result[domain][1]:
                r += "  GO id assigned to " + geneA + " is: " + data[0] + \
                     "\n  GO id assigned to " + geneB + " is: " + data[1] + \
                     "\n  LCA of assigned GO ids is: " + "|".join(result[domain][1][data]['lca']) + "\n\n"
    return r + "\n\n\n"


def return_detail(result, geneA, geneB, detail):
    '''
    '''
    for domain in result:
        r = geneA + '\t' + geneB + '\t' + str(result[domain][0]) + '\n'
    return r


def calculate_semantic_similarity(objs, geneA, geneB):
    '''
    Calls the function for calculating semantic similarity between
    genesA and genesB.
    '''

    return objs._semantic_similarity(geneA, geneB)


if __name__ == '__main__':
    path = '/Users/shobhit/Project/Yeast-SH3-Project/DoMo-Pred/Protein'
    objs = save_semantic_similarity(path + "/Db/gene_ontology.1_2.obo.txt", path +\
            "/Db/gene_association.sgd", "C:2.4,P:3.5,F:3.3", "", path + '/Db/')
