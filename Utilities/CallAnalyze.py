import os
import sys
import copy
sys.path.append("./DoMoPred")
import globeVar
import run_pipeline as RP
from Classifier import classifier
from Peptide import run_peptide
from Protein import run_protein
# This script is used to call function which used for analyze from 
# the DoMo-Pred directly.

# globe variables 

# here is a list saving protein ids
VAR_PROTEIN_ID_LIST = []  

# paths for built in data
PATH_DOMAIN = "./data/domain.txt"
PATH_RESULTS = "./Cache/"
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

# this function is used to analyze by protein ids
# given a list of protein ids and this function will
# return the interaction result between proteins
# this function will call  run_standalone_protein(prot_set, output=None) 
# from run_pipline directly and the result will be stored in the folder 
# of which named by session id under results folder
def Analyzer_ProteinIDs(sessionid,protein_id_set,features_to_use="ABCDE"):
    # first we have to check if the folder with the session id exist
    # if not, make it
    result_list = os.listdir(PATH_RESULTS)
    if sessionid not in result_list:
        os.makedirs(PATH_RESULTS + sessionid)
    
    # then we call run_standalone_protein to analyze it. and wtire results to file
    output,pred,pro_set = RP.run_standalone_protein_with_features_selection(protein_id_set,features_to_use,PATH_RESULTS + sessionid + "/result.txt")
    #output,pred,pro_set = RP.run_standalone_protein(protein_id_set,PATH_RESULTS + sessionid + "/result.txt")
    ff = open(output,"w")
    # we will not include nagative score
    head = "#\tcellular location\tbiological process\tmolecular function\tgene expression\tsequence signature\tscore\n"
    ff.write(head)
    feature_code = ["A","B","C","D","E"]
    feature_used = ["A","B","C","D","E"]
    for pro_pair,pred_result in zip(pro_set,pred):
        astr = pro_pair[0] + "," + pro_pair[1] + ","
        #    features used for analyze          positive
        for x in pred_result[1]:
            feature_used[ feature_code.index(x) ] =  "@1"
        feanamestr = ""
        for x in feature_used:
            if x != "@1":
                feanamestr += "@0,"
            else:
                feanamestr += "@1,"
        feature_used = copy.copy(feature_code)
        astr += feanamestr + str(round(pred_result[0]["positive"],2))  # round the scroe to decimal
        ff.write(astr + "\n")
    ff.close()

    return True

# this function is used to get user selected features
# post back from the index page
# this function will return a single string that can be used as the third parameters of Analyzer_ProteinIDs
def getFeatures(fea_list):
    fstr = ""
    for fea in fea_list:
        fstr += globeVar.VAR_FEATURES[str(fea)]
    return fstr

# this function is used to extract protein ids from user's uploaed file and user input
# the pramater is the file user upload or the list user input in input box.
# every line will be restricted to contains two protein ids
# if it's more than two protein id, the line will be stored in a list which 
# is tagged as unanalyzable. Therefore, the return value will be two list,
# one is the valid ids, the other one is invalids.
def Extract_Protein_Ids(data,is_file=False):
    valid = []
    invalid = []
    if is_file:
        print "file"
        # parameter is a file, function will open it then read the data
        # then the parameter data will be the content of the file
        # first line is the species, following with protein id pairs, two protein ids in one line.
        ff = open(data,"r")
        a_species = ff.readline()
        data = ff.read()
        ff.close()
    # parameter is a string , function will split it by "\n", then read the dsta
    pairs = data.split("\n")
    for ids in pairs:
        # here we can use space,comma and ; as the separtor of protein ids
        ids = ids.replace(" ",",").replace(";",",").replace("\r","")
        idd = ids.split(",")
        idd = [ x for x in idd if len(x)>0 ]
        if len(idd) != 2:
            invalid.append(idd)
            continue
        all_exist = True
        for pid in idd:
            if pid not in VAR_PROTEIN_ID_LIST:
                invalid.append(idd)
                all_exist = False
                break
        if all_exist :
            valid.append(idd)
    return valid,invalid

# this function is used to load protein id list.
# to reduce the I/O operations,
# this function will run once when the module was load
def Load_Protein_IDList():
    global VAR_PROTEIN_ID_LIST
    # open protein id file to read
    ff = open(globeVar.VAR_PATH_PROTEIN_ID_DATABASE,"r")
    linedata =  ff.readlines()[1:]
    VAR_PROTEIN_ID_LIST = [ x.split('\t')[0] for x in linedata ]
    return VAR_PROTEIN_ID_LIST

def Save_ProteinID_List_TO_File(session,pairlist):
    ff = open(globeVar.VAR_PATH_RESULT_FOLDER+"/"+session+"/input_protein_ids.txt","w")
    astr = ""
    for pair in pairlist:
        astr += pair[0] + "," + pair[1] + "\n"
    ff.write(astr)
    ff.close()
        
Load_Protein_IDList()
