'''
Created on 2011-11-16

@author: shobhit
'''
from numpy import zeros, sum, math, save, load
import os
import cPickle as pickle


class SeqSignature(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.clusters = {}
        self.signature = {}
        self.contingency = None
        self.signatcount = None
        self.sequence = {}

    def create_sequence_signature(self, interpro_structure_file, interpro_file,
                                  sequence_file, interaction_file, out_path):
        '''
        '''

        file1 = open(interpro_structure_file)
        file2 = open(interpro_file)
        file3 = open(sequence_file)
        file4 = open(interaction_file)
        self.create_signature_cluster(file1, file2)
        self.create_signature_information(file3, out_path)
        self.create_contingency_table(file4, out_path)

    def sequence_signature(self, gene):
        '''
        Given a gene (str) return a set (ssig) of sequence signatures.
        self.sequence is a dictionary with gene as keys.
        '''

        ssig = set()
        if gene in self.sequence:
            return self.sequence[gene]
        return ssig

    def create_contingency_table(self, file_data, out_path):
        '''
        Create the contingency table for positive dataset.
        '''

        self.contingency = zeros((len(self.signature), len(self.signature)),
                                 dtype=int)
        self.signatcount = zeros((len(self.signature)), dtype=int)
        for line in file_data:
            line = line.strip().split()
            if line[0] in self.sequence and line[1] in self.sequence:

                for i in self.sequence[line[0]]:
                    self.signatcount[self.signature[i]] += 1

                for j in self.sequence[line[1]]:
                    self.signatcount[self.signature[j]] += 1

                for i in self.sequence[line[0]]:
                    for j in self.sequence[line[1]]:
                        self.contingency[self.signature[i]][self.signature[j]]\
                                         += 1

        save(out_path + '/contingency.npy', self.contingency)
        save(out_path + '/signatcount.npy', self.signatcount)

    def load_sequence_signature(self, path):
        '''
        Load data tables at given path.
        '''

        if os.path.exists(path + '/contingency.npy'):
            self.contingency = load(path + '/contingency.npy')
            if os.path.exists(path + '/signatcount.npy'):
                self.signatcount = load(path + '/signatcount.npy')
                if os.path.exists(path + '/signature_information.pck'):
                    with open(path + '/signature_information.pck', 'rb') as fp:
                        self.sequence = pickle.load(fp)
                        if os.path.exists(path + '/signature.pck'):
                            with open(path + '/signature.pck', 'rb') as fp:
                                self.signature = pickle.load(fp)

    def create_signature_information(self, file_data, out_path):
        '''
        Sequence signature for all proteins based on cluster.
        '''
        count = 0
        for line in file_data:
            line = line.strip().split()
            if line[0] not in self.sequence:
                self.sequence[line[0]] = set()
            if line[1] != '':
                signature = line[1]
                if signature in self.clusters:
                    signature = self.clusters[signature]
                    self.sequence[line[0]].add(signature)
                    if signature not in self.signature:
                            self.signature[signature] = count
                            count += 1

        with open(out_path + '/signature_information.pck', 'wb') as fp:
            pickle.dump(self.sequence, fp)
        with open(out_path + '/signature.pck', 'wb') as fp:
            pickle.dump(self.signature, fp)

    def create_signature_cluster(self, file1, file2):
        '''
        '''

        clusters = {}
        for line in file1:
            line = line.strip().split(":")
            line = line[0].split("-")
            if len(line) == 1:
                parent = line[-1]
            node = line[-1]
            if node not in clusters:
                clusters[node] = parent

        for line in file2:
            line = line.strip().split()
            if line[0] in clusters:
                self.clusters[line[0]] = clusters[line[0]]
            else:
                self.clusters[line[0]] = line[0]

    def calculate_entropy(self, sigA, sigB):
        '''
        '''
        if sigA == [] or sigB == []:
            return None
        sum_xy = []
        N = float(sum(self.contingency))
        n = float(sum(self.signatcount))
        for a in sigA:
            for b in sigB:
                i = self.signature[a]
                j = self.signature[b]
                if i != j:
                    p_xy = (self.contingency[i][j] + self.contingency[j][i])/N
                else:
                    p_xy = self.contingency[i][j] / N
                p_x = self.signatcount[i] / n
                p_y = self.signatcount[j] / n
                if p_xy != 0:
                    # print "  ", a, b, math.log(p_xy/(p_x * p_y), 2)
                    sum_xy.append(math.log(p_xy/(p_x * p_y), 2))
                else:
                    # print "  ", a, b, 0.0
                    sum_xy.append(0.0)
        return sum(sum_xy)


if __name__ == '__main__':
    '''
    '''

    PATH = '../Data/'
    signs = SeqSignature()
    signs.create_sequence_signature(PATH + "tree.txt",
                                    PATH + "names.txt",
                                    PATH + "out.txt",
                                    PATH + "dip_positive_all.txt",
                                    '../db')
