import os
import sys
import getopt
import numpy

os.environ["WORK_DIR_PEP"] = os.getcwd() + '/Peptide/'
os.environ["WORK_DIR_PRO"] = os.getcwd() + '/Protein/'
os.environ["WORK_DIR_CLS"] = os.getcwd() + '/Classifier/'

from Classifier import classifier
from Peptide import run_peptide
from Protein import run_protein
from datetime import datetime
import logging

logging.basicConfig(filename='pipeline.log', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logging.captureWarnings(True)


def usage():
    '''
    Details on how to use pipeline.
    '''
    print "\n\n python2.7 run_pipeline.py -i [PWM data] -o [Output file/dir]" +\
          " -p [p-value] -d [Domain data file]\n\n"

    print " Options:\n -i    Path to PWM file or directory\n" +\
          " -o    Path to output file or directory\n" +\
          " -p    P-value threshold for PWM scanning (default: 1e-05)\n" +\
          " -d    Path to file containing domain information\n"


def command_line_arguments(argv):
    '''
    Process the command line arguments. Returns options variable.
    '''
    options = {'output': None, 'pwm': None, 'domain': None, 'p-value': 1e-05}

    try:
        opts, args = getopt.getopt(argv, "i:o:p:d:")

    except getopt.GetoptError:
        usage()
        sys.exit()

    if len(opts) == 0:
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt in ("-h"):
            usage()
            sys.exit()
        elif opt in ("-i"):
            if os.path.isfile(arg) or os.path.isdir(arg):
                options['pwm'] = arg
            else:
                print '\nPWM input file found\n'
        elif opt in ("-o"):
            options['output'] = arg
        elif opt in ("-p"):
            try:
                pval = float(arg)
            except:
                print '\nInvalid p-value. Using default 1e-05.\n'
            else:
                options['p-value'] = pval
        elif opt in ("-d"):
            if os.path.isfile(arg):
                options['domain'] = arg
            else:
                print '\nDomain sequence file not found. Skipping Structure \
                Score.\n'

    if not options['pwm']:
        usage()
        sys.exit()

    return options


def write_file(path, cel_pred, pro_set, detail=True):
    '''
    '''
    write_file = open(path, 'w')
    if detail:
        write_file.write('Domain\tPeptide\tStart\tStop\tSequence\tPeptide Score\tPeptide Count\tProtein Score\tProtein Count\tScore\n')
        for idx, (com, pep, pot, npe, npr) in enumerate(cel_pred):
            write_file.write(pro_set[idx][0] + '\t' + pro_set[idx][1] + '\t'
                             + pro_set[idx][2] + '\t' + pro_set[idx][3] + '\t'
                             + pro_set[idx][4] + '\t'
                             + str(round(pep['positive'], 2)) + '\t'
                             + str(npe) + '\t'
                             + str(round(pot['positive'], 2)) + '\t'
                             + str(npr) + '\t'
                             + str(round(com['positive'], 2)) + '\n')

    else:
        write_file.write('Domain\tPeptide\tScore\n')
        for idx, val in enumerate(cel_pred):
            write_file.write(pro_set[idx][0] + '\t' + pro_set[idx][1] + '\t'
                             + str(round(val['positive'], 2)) + '\n')

    write_file.close()


def write_std(cel_pred, pro_set, detail=False):
    '''
    '''
    print 'Domain\tPeptide\tScore\n'
    for idx, val in enumerate(cel_pred):
        print pro_set[idx][0] + '\t' + pro_set[idx][1] + '\t' +\
            str(round(val['positive'], 2))


def peptide_module(pwm, domain, pval, data):
    '''
    blah blah
    '''
    # data = run_peptide.setup_peptide()
    gnom = run_peptide.process_genome_file()
    fnam = os.path.basename(pwm)

    if domain:
        seq_data = dict(numpy.loadtxt(domain, delimiter='\t', dtype='S'))
        if fnam not in seq_data:
            print '\nSkipping Structure Score. Domain sequence'\
                + '%s not found.\n' % fnam
            structure = None
        else:
            if data[3]:
                structure = (seq_data[fnam], data[3])
            else:
                structure = None
    else:
        structure = None
        print '\nDomain sequence file not found. Skipping Structure Score.\n'

    peptide, pep_set = run_peptide.run_pwm(pwm, gnom, pval, data[0], data[1],
                                           data[2], structure)

    return peptide, pep_set


def protein_module(pep_set, data):
    '''
    '''
    protein, pro_set = run_protein.run_features(pep_set, (data[0][0]["C"], data[0][1]),
        (data[0][0]["P"], data[0][1]), (data[0][0]["F"], data[0][1]), data[1], data[2])

    return protein, pro_set


def pwm_runner(pwm, domain, pval, output, gen_data, cel_data):
    '''
    '''
    peptide, pep_set = peptide_module(pwm, domain, pval, gen_data)
    protein, pro_set = protein_module(pep_set, cel_data)

    assert (pep_set == pro_set).all(), 'Problem.. gen cel not same'

    gen_clas, cel_clas = classifier.get_classifier()

    pred = []
    for idx, (case1, case2) in enumerate(zip(peptide, protein)):
        num_pep = 4 - list(case1).count(None)
        num_pot = 5 - list(case2).count(None)

        post1 = gen_clas.test(case1[1:])
        post2 = cel_clas.test(case2)

        post = classifier.bayes(post1, post2)
        pred.append((post, post1, post2, num_pep, num_pot))

    if output:
        write_file(output, pred, pro_set)
    else:
        write_std(pred, pro_set)


def process_options(options):
    '''
    '''
    if os.path.isfile(options['pwm']):
        print '\nProcessing PWM: %s\n' % (os.path.basename(options['pwm']))
        if options['output'] and os.path.isdir(options['output']):
            out_path = options['output'] + '/' + options['pwm'] + '_' +\
                       str(options['p-value'])
        else:
            out_path = options['output']

        gen_data = run_peptide.setup_peptide()
        cel_data = run_protein.setup_protein()
        pwm_runner(options['pwm'], options['domain'], options['p-value'],
                   out_path, gen_data, cel_data)

    elif os.path.isdir(options['pwm']):
        if not options['output'] or not os.path.isdir(options['output']):
            print '\nOutput dirctory not present. Creating output directory.'
            outdir = str(datetime.now()).replace(' ', '_').replace(':', '-') +\
                '.out'
            os.makedirs(outdir)
        else:
            outdir = options['output']

        gen_data = run_peptide.setup_peptide()
        cel_data = run_protein.setup_protein()
        for pwm_file in os.listdir(options['pwm']):
            print '\nProcessing PWM: %s\n' % (pwm_file)
            pwm_path = options['pwm'] + '/' + pwm_file
            out_path = outdir + '/' + pwm_file + '_' + str(options['p-value'])
            pwm_runner(pwm_path, options['domain'], options['p-value'],
                       out_path, gen_data, cel_data)


if __name__ == '__main__':

    options = command_line_arguments(sys.argv[1:])
    process_options(options)
