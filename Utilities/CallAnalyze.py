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
VAR_PWMS_LIST = []

# paths for built in data
PATH_DOMAIN = "./data/domain.txt"
PATH_RESULTS = "./Cache/"
# constant for mode selection
MODE_USE_BUILT_IN = 1   # use built in pwms and domains
MODE_USE_UPLOAD = 2     # use user upload files

# set up globe data used for analyze
print ">>>set up globe analyze data..."
VAR_GEN_DATA = run_peptide.setup_peptide()
VAR_CEL_DATA = run_protein.setup_protein()
print ">>>done."

# this function is used to call analyze functions directly from DoMo-Pred source code.
# need 4 paramaters: 
#                   sessionid: current session id 
#                   pwmfiles: [usebuilt-in,[file list]]             
#                                                     - a list with two elements one boolean,one list
#                   domainfile: a str indicates where the path of domain file is
#                   features: [feature 1, feature 2, ... ,feature n]
#                                                     - a list of features with the type of string.
#                                                       decided which feature used for analyze
def Analyzer_PWMs(session,pwmfiles,domainfile,features):
    """
    The return value stands for nothing
    """
    # we have to check if use built in data
    if pwmfiles[0] == True:
        # use built in PWMs
        return True
    else:
        # use user uploaded files
        #print 'file name',str(pwmfiles)
        options = {'domain': domainfile, 'p-value': 1e-05}
        #gen_data = run_peptide.setup_peptide()
        #print "features=",features
        gen_data,cel_data = chooseFeatures(features)
        #gen_data = run_peptide.setup_peptide_with_selections(features) # select to use which peptide features.
        #cel_data = run_protein.setup_protein_with_feature_selection(features)
        for filename in pwmfiles[1]:
            RP.pwm_runner(filename, options['domain'], options['p-value'],filename+"_result.txt", gen_data, cel_data)
        print 'analyze finished!'
        return True
    return False

# this function is used to analyze by protein ids
# given a list of protein ids and this function will
# return the interaction result between proteins
# this function will call  run_standalone_protein(prot_set, output=None) 
# from run_pipline directly and the result will be stored in the folder 
# of which named by session id under results folder
def Analyzer_ProteinIDs(sessionid,protein_id_set,features_to_use="ABCDE",result_type="tabular"):
    # first we have to check if the folder with the session id exist
    # if not, make it
    result_list = os.listdir(PATH_RESULTS)
    if sessionid not in result_list:
        os.makedirs(PATH_RESULTS + sessionid)
    
    # then we call run_standalone_protein to analyze it. and wtire results to file
    output,pred,pro_set,feature_scroes = RP.run_standalone_protein_with_features_selection(protein_id_set,features_to_use,PATH_RESULTS + sessionid + "/result.txt")

    # USED FOR DEBUG print "\n>>>feature_score:\n",feature_scroes

    with open(output,"w") as ff:
        # we will not include nagative score
        head = "#\tcellular location\tbiological process\tmolecular function\tgene expression\tsequence signature\tscore\n"
        head = "#" + result_type + "\n" + head
        ff.write(head)
        feature_code = ["A","B","C","D","E"]
        feature_used = ["A","B","C","D","E"]
        for pro_pair,pred_result,fss in zip(pro_set,pred,feature_scroes):
            astr = pro_pair[0] + "," + pro_pair[1] + ","
            #    features used for analyze          positive
            for x in pred_result[1]:
                feature_used[ feature_code.index(x) ] =  "@1"
            feanamestr = ""
            for sc in fss:
                feanamestr += str(sc) + ","
            astr += feanamestr + str(round(pred_result[0]["positive"],2))  # round the scroe to decimal
            ff.write(astr + "\n")

    return True

# this function is used to get user selected features
# post back from the index page
# this function will return a single string that can be used as the third parameters of Analyzer_ProteinIDs
def getFeatures(fea_list):
    fstr = ""
    for fea in fea_list:
        fstr += globeVar.VAR_FEATURES[str(fea)]
    return fstr

# this function is used to choose features to use in analyze
def chooseFeatures(sel_features,xtype="PWM"):
    """
    if it is PWM, then return two feature lists, one for peptide, the other for protein.

    if it is PPI-pred, then return one list.
    """
    if xtype == "PWM":
        # DoMo-Pred
        peptide_feature_code = "LMNO"
        protein_feature_code = "PQR"
        # sleect peptide features
        pepfea = [None,None,None,None]
        profea = [None,None,None]
        for code in sel_features:
            if code in peptide_feature_code:
                i = peptide_feature_code.index(code)
                pepfea[i] = VAR_GEN_DATA[i]
            elif code in protein_feature_code:
                i = protein_feature_code.index(code)
                profea[i] = VAR_CEL_DATA[i]
        return pepfea,profea
    else:
        # PPI-Pred
        feature_code = "ABCDE"

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

def Load_PWMs_List():
    global VAR_PWMS_LIST
    v = os.listdir(globeVar.VAR_PATH_PWMS)
    VAR_PWMS_LIST = v
    return v

def Save_ProteinID_List_TO_File(session,pairlist,pro_type="Yeast"):
    ff = open(globeVar.VAR_PATH_RESULT_FOLDER+"/"+session+"/input_protein_ids.txt","w")
    ff.write(pro_type+"\r\n")
    astr = ""
    for pair in pairlist:
        astr += pair[0] + "," + pair[1] + "\n"
    ff.write(astr)
    ff.close()

        
Load_Protein_IDList()
