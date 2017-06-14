import sys
sys.path.append("../DoMoPred")
import run_pipeline as run_pipeline
from Classifier import classifier
from Peptide import run_peptide
from Protein import run_protein
# This script is used to call function which used for analyze from 
# the DoMo-Pred directly.

# globe variables 

# paths for built in data
PATH_PWMS = "../data/pwm_dir"
PATH_DOMAIN = "../data/domain.txt"
# constant for mode selection
MODE_USE_BUILT_IN = 1   # use built in pwms and domains
MODE_USE_UPLOAD = 2     # use user upload files

# this function is used to call analyze functions directly from DoMo-Pred source code.
# need 4 paramaters: 
#                   sessionid: current session id 
#                   pwmfiles: [usebuilt-in,[file list]]             
#                                                     - a list with two elements one boolean,one list
#                   domainfile: [usebuilt-in,domain file name]    
#                                                     - a list with two elements one boolean,one string
#                   features: [feature 1, feature 2, ... ,feature n]
#                                                     - a list of features with the type of string.
#                                                       decided which feature used for analyze
def Analyzer(sessionid,pwmfiles,domainfile,features):
    # we have to check if use built in data
    if pwmfiles[0] == True:
        # use built in PWMs
        pass
    else:
        # use user uploaded files
        # then we check how many PWMs user had uploaded
        if len(pwmfiles[1]) == 1:
            # user just uploaded a single file
            pass
        else:
            # user uploaed many files
            pass


if __name__ == "__main__":
    print ">>>>>>>>>>unit test for CallAnalyze Module<<<<<<<<<<<"
    print ">>>>>>>>>>unit test done for CallAnalyze Module<<<<<<<<<<<"