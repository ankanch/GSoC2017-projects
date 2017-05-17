#/usr/bin/python
from numpy import array
import scipy.stats as st


def entropy_al2co(file_data, query, query_start, query_end, pos, i):
    positions = array(pos) + query_start
    result = []
    test = []
    for line in file_data:
        if line.startswith('*'):
            break
        line = line.strip().split()
        if line[1] != '-':
            result.append(float(line[i]))
            test.append(line[1])

    summ = 0
    for posn in positions:
        summ += result[posn]
    return summ / len(positions)


def score_mafft_alignment_al2co(file_data, query, query_start, query_end, pos):
    '''
    '''
    return st.norm.cdf(entropy_al2co(file_data, query, query_start, query_end,
                       pos, 8))
