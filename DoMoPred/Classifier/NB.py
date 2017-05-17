'''
Created on 2011-04-25

@author: shobhit

Based on Tom Mitchell
'''
import os, sys
from numpy import array, unique, bincount, ndarray
from decimal import *
getcontext().prec = 2

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class NB():
    '''
    Naive bayes classifier class
    '''


    def __init__(self, type):
        '''
        type is a list of lists - num/char, min (opt), max (opt)
        '''
        self.type = type
        self.tdata = None
        self.tlabl = None
        self.lentd = None
        self.label = {}
        self.prior = {}
        self.lhood = {}
        self.bins = {}


    def train(self, data):
        '''
        process training data
        '''
        if type(data) == list:
            self.tdata, self.tlabl = self.process_list(data)
        elif type(data) == ndarray:
            self.tdata, self.tlabl = data[:, :-1], data[:, -1]
        else:
            if not os.path.exists(data):
                raise Error("file path does not exists")
            else:
                file = open(data)
                self.tdata, self.tlabl = self.process_file(file)
        self.lentd = len(self.tdata)
        self.labels()
        self.prior_prob()
        self.binning()
        self.likelihood_prob()


    def process_list(self, data):
        '''
        '''
        data = array(data)
        #return data[:, 1 : -1], data[:, -1]
        return data[:, :-1], data[:, -1]


    def process_file(self, file):
        '''
        file should have 1st column as identifier, 2nd .. colums as
        evidence, last column as label
        '''
        data = []
        label = []
        for line in file:
            if not line.startswith("#"):
                line = line.strip().split("\t")
                if len(line) < 3:
                    raise Error("file not in format")
                else:
                    data.append(line[1:-1])
                    label.append(line[-1])
        return array(data), array(label)


    def labels(self):
        '''
        '''
        for i in unique(self.tlabl):
            self.label[i] = list(self.tlabl).count(i)


    def prior_prob(self):
        '''
        prior probability - multinomial distribution - label frequency
        '''
        for i in self.label:
            self.prior[i] =  self.label[i] / float(self.lentd)


    def likelihood_prob(self, m_est = 1):
        '''
        likelihood - multinomial distribution - class frequency - m-estimates
        '''
        for i in self.bins:
            self.lhood[i] = {}
            value = len(unique(self.tdata[:, i]))
            uprior = 1.0 / value
            for j in self.bins[i]:
                self.lhood[i][j] = (self.bins[i][j] + (m_est * uprior)) / float(self.label[j[1]] + m_est)


    def create_intervals(self, minimum, maximum, n):
        '''
        '''
        intervals = []
        i = minimum
        count = 0
        inc = (maximum - minimum)/Decimal(str(n))
        while i < maximum:
            intervals.append((i, i+inc))
            i += inc
            count += 1
        return intervals


    def test_interval(self, value, interval):
        '''
        '''
        return interval[0] <= value <= interval[1]


    def create_bins(self, attribute, intervals):
        '''
        '''
        self.bins[attribute] = {}
        for label in self.label:
            for interval in intervals:
                if (interval, label) not in self.bins[attribute]:
                    self.bins[attribute][(interval, label)] = 0


    def binning(self, num_bins = 10):
        '''
        '''
        for i in range(self.tdata.shape[1]):
            minimum, maximum = ('', '')
            if self.type[i][0] == "num":
                try:
                    minimum = Decimal(str(self.type[i][1]))
                    maximum = Decimal(str(self.type[i][2]))
                except:
                    if minimum == '' or maximum == '':
                        lst = filter(lambda a: a != 'None', self.tdata[:, i])
                        minimum = min(map(Decimal, lst))
                        maximum = max(map(Decimal, lst))
                        #minimum = min(map(Decimal, self.tdata[:, i]))
                        #maximum = max(map(Decimal, self.tdata[:, i]))
                intervals = self.create_intervals(minimum, maximum, num_bins)
            elif self.type[i][0] == "char":
                intervals = unique(self.tdata[:, i])
            else:
                raise Error("Unknown data type: only use num or char")

            self.create_bins(i, intervals)

            for j in range(self.tdata.shape[0]):
                #### take care of None ###
                if self.tdata[j][i] == 'None':
                    continue
                #######
                bin_name = ''
                if self.type[i][0] == "num":
                    for k in intervals:
                        if self.test_interval(float(self.tdata[j][i]), k):
                            bin_name = k
                elif self.type[i][0] == "char":
                    bin_name = self.tdata[j][i]
                else:
                    raise Error("Unknown data type: only use num or char")
                label = self.tlabl[j]

                if bin_name != '':
                    self.bins[i][(bin_name, label)] += 1


    def test(self, case, prior = None):
        '''
        '''
        posterior = []
        norm = 0
        #print self.lhood
        for label in self.label:
            if prior != None:
                if label not in prior:
                    raise Error("label not found in prior")
                prob = float(prior[label])
            else:
                prob = self.prior[label]
            for i in range(len(case)):
                flag = 1
                if case[i] == 'None' or case[i] == None:
                    pass
                elif self.type[i][0] == "char":
                    if (case[i], label) in self.lhood[i]:
                        prob = prob * self.lhood[i][(case[i], label)]
                        flag = 0
                elif self.type[i][0] == "num":
                    for j in self.lhood[i]:
                        if j[1] == label:
                            if self.test_interval(float(case[i]), j[0]):
                                prob = prob * self.lhood[i][j]
                                flag = 0
                if flag:
                    # Missing data
                    prob = prob * 1
            posterior.append((prob, label))
            norm += prob

        return {posterior[0][1]: posterior[0][0] / norm, posterior[1][1]: posterior[1][0] / norm}




if __name__ == "__main__":
    #classifier = NB([["char"], ["char"], ["char"], ["char"]])
    classifier = NB([["num"], ["num"], ["num"]])
    classifier.train("train_num.txt")
    #print classifier.test(['Sunny', 'Cool', 'Normal', 'Weak'])
    print classifier.test([6, 130, 8])
    #print classifier.test([1.0, 1.0, 1.0, 1.0])

