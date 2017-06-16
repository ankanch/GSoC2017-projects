import sys
#sys.path.append("../DoMoPred")
#import DoMoPred.run_pipeline as run_pipeline
#from DoMoPred.Classifier import classifier
#from DoMoPred.Peptide import run_peptide
#from DoMoPred.Protein import run_protein
# This script is used to call function which used for analyze from 
# the DoMo-Pred directly.

# globe variables 

# paths for built in data
PATH_PWMS = "../data/pwm_dir"
PATH_DOMAIN = "../data/domain.txt"
PATH_PROTEIN_LIST = ""
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

# this function is used to extract protein ids from user's uploaed file and user input
# the pramater is the file user upload or the list user input in input box.
# every line will be restricted to contains two protein ids
# if it's more than two protein id, the line will be stored in a list which 
# is tagged as unanalyzable. Therefore, the return value will be two list,
# one is the valid ids, the other one is invalids.
def Extract_Protein_Ids(data):
    if type(data) == file:
        # parameter is a file, function will open it then read the data
        return [],[]
    elif type(date) == str:
        # parameter is a string , function will split it by "\n", then read the dsta
        return [],[]
    else:
        # two empty list stands for error
        return [],[]

# this function is used to load protein id list.
# to reduce the I/O operations,
# this function will run once when the module was load
def Load_Protein_IDList():
    pass
        

if __name__ == "__main__":
    print ">>>>>>>>>>unit test for CallAnalyze Module<<<<<<<<<<<"
    print ">>>>>>>>>>unit test done for CallAnalyze Module<<<<<<<<<<<"