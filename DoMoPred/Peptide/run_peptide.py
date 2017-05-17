''' Load genomic pipeline '''

from Disordered import *
from Surface import *
from Peptide import *
from PWMsearch import *
from Structure import *
from numpy import loadtxt, log2, array, savetxt, column_stack

PATH = os.getenv("WORK_DIR_PEP") + 'Db'


def process_genome_file():
    '''process the protein file and generate a dictionary of sequences'''

    file = open(PATH + '/yeast_protein.fasta')
    uid, seq, data = ("", "", {})
    for line in file:
        if line.startswith(">"):
            if uid in data:
                data[uid] = seq
                seq = ""
            uid = line.strip().strip(">")
            if uid not in data:
                data[uid] = ""
            else:
                print "duplicate %s" % uid
        else:
            seq += line.strip()
    data[uid] = seq
    return data


def setup_peptide():
    '''
    Setup feature datasets.
    '''
    disd, surf, pepd, strt = (None, None, None, None)

    print "\nSetting up genomic features .... \n"
    print "   Setting up disorder .... "
    disd = load_disorder(PATH)

    print "   Setting up surface .... "
    surf = load_surface(PATH)

    print "   Setting up peptide .... "
    pepd = load_peptide(PATH)

    print "   Setting up structure .... "
    strt = load_structure(PATH)

    return disd, surf, pepd, strt


# def information_content(column):
#    '''Return information cotent of column'''
#
#    return abs(sum(column * log(column)))

def before_entropy(background):
    '''
    '''
    return -sum(background * log2(background))


def after_entropy(column):
    '''
    '''
    return -sum(column * log2(column))


def read_pwms(pwm_path, bck_path, edge_threshold=0.5, inner_threshold=0.4, extra=False):
    '''
    Return PWM as array and its significant positions
    Note: made changes in entropy
    '''

    barray = loadtxt(bck_path)
    farray = loadtxt(pwm_path, delimiter='\t', skiprows=1, dtype=str)
    column = farray[:, 0]
    farray = farray[:, 1:]
    farray = farray.astype(float)
    farray = farray / 20

    background = before_entropy(barray)

    ic = []
    for i in range(farray.shape[1]):
        ic.append(background - after_entropy(farray[:, i]))


    max_ic = max(ic)
    ic = array(ic) / max_ic

    i = 0
    while ic[i] < edge_threshold:
        i += 1

    j = 0
    len_ic = len(ic)
    while ic[len_ic - 1 - j] < edge_threshold:
        j += 1

    #end = farray.shape[1] + j + 1

    trimmed = farray[:, i: (len_ic - j)]
    if trimmed.shape[1] < 4:
        trimmed = farray
    else:
        ic = ic[i: (len_ic - j)]

    pos = []
    for idx, val in enumerate(ic):
        if val >= inner_threshold:
            pos.append(idx)

    if extra:
        sig = '-'.join(map(str, pos))
        savetxt('../trimmed_pwm/%s-(%s)'%(pwm_path.split('/')[-1], sig), column_stack((column, trimmed)), fmt='%s')

    return trimmed, tuple(pos)


def run_pwm(pwm_file, genome, tol, *args):
    '''
    '''

    features = [disorder_score, surface_score, peptide_score, structure_score]

    pwm, pos = read_pwms(pwm_file, PATH + '/yeast.background')
    # print pwm, pos
    initialize_database(PATH + '/yeast_protein.pwm',
                        PATH + '/yeast.background')
    length = initialize_pwm(pwm)
    tol = get_threshold(tol)
    hits = search_database(tol)
    # print hits
    pwm_name = open(pwm_file).readline().strip('#').strip()

    results = []
    int_set = []
    for hit in hits:
        query = hit
        for start, end in hits[hit]:
            score = hits[hit][(start, end)] / 100.0
            pep_seq = genome[query][start:end]

            tmp = [score]
            for idx, data in enumerate(args):
                if data:
                    if idx == 3:
                        val = features[idx](data[0], pep_seq, data[1][0],
                                            data[1][1], data[1][2])
                    else:
                        val = features[idx](query, start, end, data, pos)
                    tmp.append(val)

            results.append(tmp)
            int_set.append([pwm_name, query, start + 1, end, pep_seq])

    results = array(results)
    max_scr = max(results[:, 0])
    results[:, 0] /= max_scr

    # print results
    return results, array(int_set)

if __name__ == '__main__':

    for pwm in os.listdir('../pwm_dir/'):
        print pwm
        read_pwms('../pwm_dir/' + pwm, 'Db/yeast.background')
