from NB import *
import numpy

def create_classifier(training1, training2):
    '''
    '''
    gen_clas = NB([["num", 0, 1], ["num", 0, 1], ["num", 0, 1], ["num", 0, 1]])
    cel_clas = NB([["num", 0, 1], ["num", 0, 1], ["num", 0, 1], ["num", -1, +1], ["num", '', '']])

    gen_clas.train(training1)
    cel_clas.train(training2)

    return gen_clas, cel_clas


def process_standard(file_name, add, idx = 2):
    '''
    '''
    data = numpy.loadtxt(file_name, dtype = str, delimiter = "\t")
    data = data[:, idx:]
    data = numpy.column_stack((data, [add] * data.shape[0]))
    return data


def get_traning_data(pos_path, neg_path):
    '''
    '''
    pos = process_standard(pos_path, "positive")
    neg = process_standard(neg_path, "negative")
    training = numpy.row_stack((pos, neg))

    return training


def get_classifier():
    '''
    '''
    PATH = os.getenv("WORK_DIR_CLS")
    training1 = get_traning_data(PATH + 'gen_standard/positive.txt', PATH + 'gen_standard/negative.txt')
    training2 = get_traning_data(PATH + 'cel_standard/positive.txt', PATH + 'cel_standard/negative.txt')

    return create_classifier(training1, training2)


def bayes(prob1, prob2):
    '''
    '''

    tmp = {}
    for class_label in prob1:
        tmp[class_label] = (prob1[class_label] * prob2[class_label]) / 0.5

    # print prob1, prob2
    den = sum(tmp.values())
    for class_label in tmp:
        tmp[class_label] /= den

    return tmp
