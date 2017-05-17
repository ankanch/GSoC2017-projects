import PWMSearch as psearch
import os, numpy, random

def initialize_database(seqdb, bg):
	'''
	set sequence db file and background file
	'''
	#print "loading sequence database and backgound file....."
	if not os.path.exists(seqdb):
		print "Sequence db not found"
		return -1
	if not os.path.exists(bg):
		print "Backgound file not found", bg
		return -1
	psearch.SequenceDB(seqdb)
	psearch.BackGround(bg)
	#print "Done loading."
	return 1


def initialize_background(bg):
        '''
        set background file
        '''
        if not os.path.exists(bg):
            print "Backgound file not found", bg
            return -1
        psearch.BackGround(bg)
        print "Done background."
        return 1

def initialize_sequence(seq):
        '''
        '''
        #print "Loading sequence"
        psearch.Sequence(seq)
        #print "Done sequence."
        return 1


def process_pep(fname):
	'''
	Convert peptide file (BRAIN/LOLA/MUSI output) to frequency matrix
	'''
	map = {"A":0, "C":1, "D":2, "E":3, "F":4, "G":5, "H":6, "I":7, "K":8, \
	       "L":9, "M":10, "N":11, "P":12, "Q":13, "R":14, "S":15, "T":16, \
               "V":17, "W":18, "Y":19}
	pep_file = open(fname).readlines()
        data = numpy.zeros((20, len(pep_file[12].strip().split("\t")[1][-5:])), dtype = 'i')
        for line in pep_file[12:]:
                line = line.strip().split("\t")[1][-5:]
                for i,j in enumerate(line):
                        if j in map:
                            data[map[j]][i] += 1
	return data.tolist()


def process_pwm(fname):
	'''
	Convert PWM file (BRAIN/LOLA/MUSI output) to frequency matrix
	'''
        map = {"A":0, "C":1, "D":2, "E":3, "F":4, "G":5, "H":6, "I":7, "K":8, \
               "L":9, "M":10, "N":11, "P":12, "Q":13, "R":14, "S":15, "T":16, \
               "V":17, "W":18, "Y":19}
        pep_file = open(fname).readlines()
        data = numpy.zeros((20, len(pep_file[1].strip().split("\t")[1:])), dtype = 'i')
        for line in pep_file[1:]:
                line = line.strip().split("\t")
                for i,j in enumerate(line[1:]):
                        data[map[line[0]]][i] = (float(j) / 20) * 1000
        for col, col_sum in enumerate(numpy.sum(data, axis = 0)):
                if col_sum != 1000:
                        for i in range(1000 - col_sum):
                                row = random.randint(0, 19) # this is the part which could give different results
                                data[row][col] += 1
        return data.tolist()



def initialize_pwm_file(fname):
	'''
	Load processed pwm file
	'''
	print "Loading PWM " + fname + "...."
	if not os.path.exists(fname):
		print "PWM file not found"
		return -1
	data = process_pwm(fname)
	length = len(data[0])
	psearch.LoadPWM(data)
	print "Done PWM."
	return length


def initialize_pwm(pwm):
    '''
    Load PWM
    '''
    #pwm = (pwm / 20.0) * 1000
    pwm = pwm * 1000
    pwm = pwm.astype(int)
    for col, col_sum in enumerate(numpy.sum(pwm, axis = 0)):
        if col_sum != 1000:
            for i in range(1000 - col_sum):
                row = random.randint(0, 19) # this is the part which could give different results
                pwm[row][col] += 1
    length = pwm.shape[1]
    pwm = pwm.tolist()
    psearch.LoadPWM(pwm)
    return length


def search_database(tol, all = 0):
	'''
	search for a give pval
	'''
	#print "Searching with pval " + str(pval) + "...."
	match = psearch.ScanDB(tol, all)
	#print "Search finished"
	return match


def get_threshold(pval):

    tol = psearch.Threshold(pval)

    return tol


