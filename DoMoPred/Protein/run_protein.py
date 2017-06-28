''' Load protein pipeline '''

from Semantic import *
from Expression import *
from Sequence import *
from numpy import array

PATH = os.getenv("WORK_DIR_PRO") + 'Db'

def setup_protein():
    '''
    Setup feature datasets.
    '''
    semt, expn, sign = (None, None, None)

    print "\nSetting up protein features .... \n"
    print "  Setting up cellular location .... "
    print "  Setting up biological process .... "
    print "  Setting up molecular function .... "
    semt = load_semantic(PATH)

    print "  Setting up expression ...."
    expn = load_expression(PATH)

    print "  Setting up sequence signature ....\n\n"
    sign = load_sequence(PATH)

    return semt, expn, sign


def run_features(prot_set, *args):
    '''
    fetaure data
    '''

    features = [semantic_score, semantic_score, semantic_score, expression, sequence]

    results = []
    int_set = []

    for prot1, prot2, s, e, seq in prot_set:
        tmp = []
        for idx, data in enumerate(args):
            if data:
                val = features[idx](prot1, prot2, data)
                tmp.append(val)
        results.append(tmp)
        int_set.append([prot1, prot2, s, e, seq])

    return array(results), array(int_set)


def run_features_standalone(prot_set, *args):
    '''
    fetaure data
    '''

    features = [semantic_score, semantic_score, semantic_score, expression, sequence]

    results = []
    int_set = []

    for prot1, prot2 in prot_set:
        tmp = []
        for idx, data in enumerate(args):
            if data:
                val = features[idx](prot1, prot2, data)
                tmp.append(val)
                print "\n====\n",val
        results.append(tmp)
        int_set.append([prot1, prot2])
    return array(results), array(int_set)

# this function need one more parameters specify which features to use
# example: features = "ABCDE" refers to use all five features
# this function will return an extra varialbe(leftmost) to infer which features used for analyze
def run_features_standalone_with_features_selection(prot_set,features_to_use, *args):
    '''
    fetaure data
    we have to make sure that every parameters in args corresponds to the right features 
    '''

    feature_code = "ABCDE"
    #feature code:     A               B               C             D         E
    features = [semantic_score, semantic_score, semantic_score, expression, sequence]

    #select featues to use

    results = []
    int_set = []

    for prot1, prot2 in prot_set:
        tmp = []
        for idx, data in enumerate(args):
            if data and feature_code[idx] in features_to_use:  # make sure user select to use this feature
                                                               # we're bypass these unselected features here
                val = features[idx](prot1, prot2, data)
                tmp.append(val)
            else:
                tmp.append(None)
        results.append(tmp)
        int_set.append([prot1, prot2])
    return [x for x in features_to_use if x in feature_code],array(results), array(int_set)