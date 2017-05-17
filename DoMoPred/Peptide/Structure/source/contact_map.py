import os
import nwalign as nw

# http://ligin.weizmann.ac.il/cma/ --- maps are generated using this tool
#

AA = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
      "GLU": "E", "GLN": "Q", "GLY": "G", "HIS": "H", "ILE": "I",
      "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
      "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}


def read_contact_maps(path):
    '''
    '''
    models = {}
    for fname in os.listdir(path):
        fdata = open(path + fname).readlines()
        mod = fname.rstrip(".txt")
        if mod not in models:
            models[mod] = {}
            for line in fdata[2:]:
                line = line.strip().split(" ")
                line = [x for x in line if x != '']
                line[0] = AA[line[0]]
                line[2] = AA[line[2]]
                if float(line[4]) > 0:
                    models[mod][(int(line[1][:-1]), int(line[3][:-1]))] =\
                     float(line[4])
    return models


def read_model_sequences(path):
    '''
    '''
    seq_data = {}
    for fname in os.listdir(path):
        fdata = open(path + fname).readlines()
        mod = fname.rstrip(".pdb")
        if mod not in seq_data:
            seq_data[mod] = {}
            for line in fdata:
                if line.startswith("SEQRES"):
                    line = line.strip().split()
                    if line[2] not in seq_data[mod]:
                        seq_data[mod][line[2]] = []
                    for aa in line[4:]:
                        seq_data[mod][line[2]].append(AA[aa])
    return seq_data


def load_structure(path):
    '''
    '''

    models = read_contact_maps(path + '/map_txt/')
    seqdat = read_model_sequences(path + '/map_seq/')
    matrix = path + '/BLOSUM62'

    return models, seqdat, matrix


def contact_map_helper(alignment):
    '''
    '''
    matches = []
    for i in range(len(alignment[0])):
        if alignment[0][i] == alignment[1][i]:
            matches.append(i + 1)
    return matches


def structure_score(dom, pep, models, model_seqs, mat):
    '''
    '''
    model_max = {"1SSH": 49.900, "1ZUK": 61.800, "1N5Z": 48.100,
                 "2KYM": 47.100, "2RQW": 56.800, "2VKN": 51.100}
    model_scr = []
    for model in model_seqs:
        dom_align = nw.global_align(dom, "".join(model_seqs[model]["D"]),
                                    gap_open=-100, gap_extend=-1,
                                    matrix=mat)
        dom_matches = contact_map_helper(dom_align)

        pep_align = nw.global_align(pep, "".join(model_seqs[model]["P"]),
                                    gap_open=-100, gap_extend=-1,
                                    matrix=mat)
        pep_matches = contact_map_helper(pep_align)

        score = 0
        count = 0
        # max_model = sum(models[model].values())
        for i in models[model]:
            if i[0] in dom_matches and i[1] in pep_matches:
                score += models[model][i]
                count += 1

        if count == 0:
            model_scr.append(0)
        else:
            model_scr.append((score / float(model_max[model])) / count)

    return max(model_scr)


if __name__ == '__main__':

    models = read_contact_maps("../map_txt/")
    model_seqs = read_model_sequences("../map_seq/")
