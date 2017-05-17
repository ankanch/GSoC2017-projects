import os
import tarfile
from parse_alignment import *


def load_peptide(path):
    '''
    '''

    tar = tarfile.open(path + "/yeast_al2co_all.tar.gz", "r:gz")
    db = {}
    for tarinfo in tar:
        if tarinfo.isfile():
            file_data = tar.extractfile(tarinfo).readlines()
            pid = tarinfo.name.strip("output_all/")  # .strip(".out")
            db[pid] = file_data

    return db


def peptide_conservation_db(query, db, start, end, pos):
    '''
    '''

    if query in db:
        if len(db[query]) == 0:
            return None
        return score_mafft_alignment_al2co(db[query], query, start, end, pos)
    return None


def peptide_score(query, start, end, db, pos):
    '''
    '''

    return peptide_conservation_db(query, db, start, end, pos)


if __name__ == '__main__':
    os.environ["WORK_DIR_GEN"] = "../../"
    setup = read_peptide()
    print peptide_conservation("YPR054W", setup, -1, -1)
