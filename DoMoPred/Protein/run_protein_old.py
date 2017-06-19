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
