'''
Created on 2010-07-27

@author: Shobhit Jain

@contact: shobhit@cs.toronto.edu
'''

import sys
import os
import getopt
from main import load_semantic_similarity, calculate_semantic_similarity
from mapping import *


def _usage():
    '''
    Details on how to use TCSS.
    '''
    print "\n\n tcss.py [-options] geneA geneB\
    \n or \n tcss.py [-options] -i input_file"
    print "\n -options \
    \n    -i [file name] or --input [=file name]       Input file (two genes separted by comma per line)\
    \n    -o [file name] or --output [=file name]      Output file\
    \n    -c [domain:cutoff] or                        Domain [C/P/F], cutoff [int/float] in any combination\
    \n         --topology-cutoff [=domain:cutoff]      (default: C:2.4,P:3.5,F:3.3)\
    \n    --detail                                     Detailed output (default: False)\
    \n    --gene [=file name]                          Gene annotation file (default: SGD file provided)\
    \n    --go [=file name]                            Gene Ontology (GO) obo file (default: GO file provided)\
    \n    --drop [=evidence code]                      GO evidence code not to be used \
    \n    -h or --help                                 Usage\n\n\n"



def _command_line_arguments(argv):
    '''
    Process the command line arguments. Returns options variable.
    '''
    options = {'args':None, 'input':None, 'output':None, 'detail':None, 'ontology':'', \
               'gene':'', 'go':'', 'drop':''}
    try:
        opts, args = getopt.getopt(argv, "hi:o:c:", ["help", "input=", "output=", "topology-cutoff=", \
                                                     "detail", "ontology=", "gene=", "go=", "drop="])
    except getopt.GetoptError:
        _usage()
        sys.exit(2)
    if len(opts) == len(args) == 0:
        _usage()
        sys.exit()
    if 1 < len(args) < 3:
        options['args'] = args
    if len(args) > 2:
        _usage()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            _usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            if os.path.isfile(arg):
                if len(args) > 0:
                    print "Excluding arguments:", args
                    options['args'] = None
                options['input'] = arg
            elif os.path.isdir(arg):
                options['input'] = arg
            else:
                print 'Input file not found'
                sys.exit()
        elif opt in ("-o", "--output"):
            options['output'] = arg
        elif opt in ("-c", "--ontology"):
            options['ontology'] = arg
        elif opt in ("--detail"):
            options['detail'] = True
	elif opt in ("--drop"):
	    options['drop'] = arg
        elif opt in ("--gene"):
            if os.path.isfile(arg):
                options['gene'] = arg
            else:
                print 'Gene annotation file not found'
                sys.exit()
        elif opt in ("--go"):
            if os.path.isfile(arg):
                options['go'] = arg
            else:
                print 'GO file not found'
                sys.exit()
        else:
            _usage()
            sys.exit()
    if options['args'] == None and options['input'] == None:
        _usage()
        sys.exit()
    return options


def return_details(result, geneA, geneB):
    '''
    '''
    return geneA + '\t' + geneB + '\t' + str(result) + '\n'


def return_detail(result, geneA, geneB, detail = True):
    '''
    Formats the output for printing on screen or on file.
    '''
    domain_def = {'C':'Cellular Component', 'P':'Biological Process', 'F':'Molecular Function'}
    r = "\nSemantic similarity between " + geneA + " and " + geneB + " is: " + str(result[0]) + "\n"
    print result
    if detail and result[1]:
        for data in result[1]:
            r += "  GO id assigned to " + geneA + " is: " + data[0] + \
                 "\n  GO id assigned to " + geneB + " is: " + data[1] + \
                 "\n  LCA of assigned GO ids is: " + "|".join(result[1][data]['lca']) + "\n\n"
    return r + "\n\n\n"


def load_semantic(path):
    '''
    '''

    mappings = mapper(path + "/map_sgd.txt")
    objs = load_semantic_similarity(path + "/cc.pck", path +
                                    "/bp.pck", path + "/mf.pck")
    #objs = save_semantic_similarity(path + "/gene_ontology.1_2.obo.txt", path +\
    #        "/gene_association.sgd", "C:2.4,P:3.5,F:3.3", "", path)
    return objs, mappings


def semantic_score(a, b, data, gene = True):
    '''
    Run TCSS when input file is not provided.
    '''

    objs = data[0]
    gene2protein = data[1]
    result = {}
    if a in gene2protein and b in gene2protein:
        if gene:
            val = []
            for i in gene2protein[a]:
                for j in gene2protein[b]:
                    val.append(calculate_semantic_similarity(objs, i, j)[0])
            return max(val)


        else:
            return calculate_semantic_similarity(objs, a, b)[0]
    else:
        return None



def output_results(result, outfile):
    '''
    Output the results on screen or on file.
    '''
    if outfile:
        try:
            for domain in result:
            	file = open(outfile + "." + domain, 'w')
            	file.write(result[domain])
            	file.close()
        except:
            print "Cannot open output file: check path or permissions \n Printing results on screen"
    else:
        pass



if __name__ == '__main__':

    options = _command_line_arguments(sys.argv[1:])

    # Set dpath to input dir
    dpath = options["input"]
    # Set opath to output dir
    opath = options["output"]
    # Change the list parameters
    for onto in ["P:4.0", "C:3.0", "F:3.6"]:
        print onto
        objs = load_semantic_similarity("Semantic/human/go.txt", "Semantic/human/goa_human.txt", onto, "")
        for file in os.listdir(dpath):
            print file
	    input_file_run(objs, dpath + file, opath + "%s"%(file))

