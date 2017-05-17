'''
Created on 2011-11-16

@author: shobhit
'''
from sequence_signature import SeqSignature
from numpy import log
import math


def load_sequence(path):
    '''
    Load sequence signature data.
    '''

    signs = SeqSignature()
    signs.load_sequence_signature(path)

    return signs


def sequence(a, b, signs):
    '''
    '''
    signA = list(signs.sequence_signature(a))
    signB = list(signs.sequence_signature(b))
    value = signs.calculate_entropy(signA, signB)
    if value:
        reval = log(value)
        if math.isnan(reval):
            return None
        return reval
    return value
