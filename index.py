import time
import flask
import os
from Utilities import globeVar
from flask import Flask, jsonify, redirect, render_template, request,make_response,send_file
from Utilities import SessionManager,ZipMaker,CallAnalyze


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = globeVar.VAR_PATH_UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = globeVar.VAR_PATH_RESULT_FOLDER

# This is the entrance URL for the index page
@app.route('/')
def index():
    Protein_id_list = CallAnalyze.Load_Protein_IDList()
    return render_template("index.html",PID=Protein_id_list)


# This is the result URL
# For test, I use some selected data to show how it looks
@app.route('/result/<sessionid>')
def result(sessionid):
    sample_result=[[0,[["P15891","Q06604",427,436,"PAIPQKKSFL",0.94,4,0.95,4,1.0],
                    ["P15891","Q06604",427,436,"PAIPQKKSFL",0.94,4,0.95,4,1.0],
                    ["P15891","Q06604",427,436,"PAIPQKKSFL",0.94,4,0.95,4,1.0],
                    ["P15891","Q06604",427,436,"PAIPQKKSFL",0.94,4,0.95,4,1.0]]],
               [1,[["P15800","Q06694",427,436,"PAIPQKKSFL",0.94,4,0.95,4,1.0],
                    ["P15800","Q06694",427,436,"PASDKYLFMS",0.94,4,0.95,4,1.0],
                    ["P15800","Q06694",427,436,"PMSHTKSALN",0.94,4,0.95,4,1.0]]]]
    #about result package.
    #result package should be a list of lists which contains a lot of different pairs protein-protein interaction result
    #the interaction result set made up of two part:result name(or id),result list
    #A typical result_package should be look like below:
    #       [       [result name ,[result list]  ] ,
    #               [sample result ,[[result one],[result two],[...],...]  ]
    #               ,....  ]
    if len(sessionid) < 5:
        # for debug
        return render_template("result.html",result_package=sample_result,SESSIONID=sessionid,TIME=["1.1.1.1","X"],PWM=True)
    # check session first
    if SessionManager.checkSession(sessionid):
        not_found("The session you're looking for isn't exist on this server.\n\
                it might be out of date or never had the session before.")
    # before we print the result, we have to check analyze type,
    # to know it is analyzed by protein id pairs or PWMs
    try:
        analyze_type = SessionManager.getType(sessionid)
    except:
        return server_fault("Invalid session.<br/>Cannot found the session you request.<br/> The session you are looking for might be expired.")
    if analyze_type == "type_normal" or analyze_type == "type_advance":
        # then we open result.txt of that session folder and output the data
        ff = open(globeVar.VAR_PATH_RESULT_FOLDER + "/" + sessionid + "/result.txt")
        data =  ff.readlines()
        ff.close()
        data = data[1:]
        final_data = []
        for lines in data:
            pd = lines.replace("\n","").split(",")
            final_data.append(pd)
        create_time = [SessionManager.getDate(sessionid),str(SessionManager.VAR_RESULT_LIFE)]
        return  render_template("result.html",result_package=final_data,SESSIONID=sessionid,TIME=create_time)
    elif SessionManager.getType(sessionid) == "type_pwm":
        pass
    

@app.route('/download/<sessionid>')
def download(sessionid):
    # first,we have to check if the result user looking for is exist
    # normally,the  result file will have the same filename (session id )
    # with the upload folder
    if sessionid not in os.listdir(globeVar.VAR_PATH_RESULT_FOLDER):
        return not_found("FIle not found on this server. The result you looking for might be removed.","/result/"+sessionid)
    
    # file exist, then we return then we check if an zipped file with the 
    # same name as the folder, if exist, return it. Otherwise, we have to 
    # make all files in current folder into a single zip file,then return it.
    # File name contains 3 parts:  prefix   +   session    + file-format
    #                    Example: "Dataset_" +  session id  + ".zip"
    filename = "Dataset_" + sessionid + ".zip"
    if filename in os.listdir(globeVar.VAR_PATH_RESULT_FOLDER+"/"+sessionid):
        # return the exist zip file. 
        print("no new zip")
        filepath = globeVar.VAR_PATH_RESULT_FOLDER.replace("./","")+ "/" + sessionid +"/"+filename
        response = make_response(send_file( filepath ))
        response.headers["Content-Disposition"] = ("attachment; filename=%s;" % filename)
        return response
    
    # compress all files then return it.
    # This will only be performed once. Becausethe next time user request
    # the result dataset with the same session id, it will return the exist file generate last time.
    print("new zip")
    targetfolder = globeVar.VAR_PATH_RESULT_FOLDER+"/"+ sessionid + "/"
    filename = "Dataset_%s.zip" % sessionid
    ZipMaker.make_zip(targetfolder,targetfolder+filename)
    response = make_response(send_file( targetfolder + filename ))
    response.headers["Content-Disposition"] = ("attachment; filename=%s;" % filename)
    return response


# This URL is for running analyze, both normal analyze and advance analyze
# In normal analyze, user need just input protein id pairs and select specices
# In advance analyze, user will need to optimize a lot of settings or even upload coustom files to analyze
# We use a hidden value post by a hidden filed to determine which knid of analyze user want to perform
@app.route('/runanalyze',methods=['POST'])
def run_analyzealyze():
    # first we have to query what kind of analyze user want to perform.
    # the analyze indicator is post with the value of the hidden filed analyze_type in HTML from of index.html
    # two type of analyze at this time:  1).normal   2).advance
    analyze_type =  request.form['analyze_type']

    # generate a session id for this analyze which will used to 
    # flag this analyzing as well as the folder name.
    # After we generate the session, we have to add it to the Session List which help us to manage.
    session = SessionManager.generateSessionID()
    SessionManager.addSession(session)

    # Path below is the path of the folder which store this run of analyzing.
    # And we create the folder here.
    # files will be stored: 1).analyze result 2).user uploads 3).domain.txt
    analyzing_target_dir = app.config['UPLOAD_FOLDER']+"/"+session
    os.mkdir(analyzing_target_dir)

    protein_ids = []
    invalid_ids = []

    # Start processing user's options on analyzing
    if analyze_type == "normal":
        SessionManager.setType(session,"type_normal")
        #user select normal analyze, which requires him to input protein id pairs and select species
        idpairs_normal = request.form['idpairs_normal']
        select_normal = request.form['select_normal']
        idpairs_normal = idpairs_normal.replace("\r","")
        if idpairs_normal.count("\n") == 0:
            idpairs_normal += "\n"

        # here we call functions to check if the ids user input satisfy the creteria that
        # every line must only contains two protein ids. Function below will help us extract 
        # both satisfied and unsatisfied protein ids.
        protein_ids,invalid_ids =  CallAnalyze.Extract_Protein_Ids(idpairs_normal)
        if len(protein_ids) < 1 or len(protein_ids[0]) < 2:
            return server_fault("Invalid Protein ID input.<br/> Please use comma,space as separtor.\
                    <br/>You may input less than two protein IDs or no valid protein ID pairs dectected!")
        print "protein_ids=",protein_ids,"\r\ninvalid_ids=",invalid_ids,"\r\ndata[0][0]=",protein_ids[0][0]
        #then we call function Analyzer_ProteinIDs from CallAnalyze to analyze
        CallAnalyze.Analyzer_ProteinIDs(session,protein_ids)

        # after analyze done, we then make a file of protein ids 
        # into result/sessionid folder
        CallAnalyze.Save_ProteinID_List_TO_File(session,protein_ids)
        
        return render_template("redirect.html",TARGET="result/"+session)
    elif analyze_type == "advance":
        SessionManager.setType(session,"type_advance")
        #user select advance analyze,which need to customize a lot of options.

        # first we need to get the file user uploaded, if user doesn't uploaded one,
        # then we need to check if user input the id pairs. By check the filename's length ,
        # we can determine wether a user uploaded a file.
        features = request.form.getlist('features[]')
        id_file = request.files["id_file"]
        feature_str = CallAnalyze.getFeatures(features)

        # check if user upload a file.
        if len(id_file.filename) > 0:
            # save the file to the disk first.
            filepath = os.path.join(analyzing_target_dir, id_file.filename.replace(" ",""))
            id_file.save(filepath)

            # then, we  secure the protein ids, get both valid and invalid protein ids
            # let Extract_Protein_Ids help us to reads the data,and run analyze for us.
            protein_ids,invalid_ids =  CallAnalyze.Extract_Protein_Ids(filepath,True) 
            if len(protein_ids) < 1 or len(protein_ids[0]) < 2:
                return server_fault("Invalid Protein ID input.<br/> Please use comma,space as separtor.\
                        <br/>You may input less than two protein IDs or no valid protein ID pairs dectected!")

            # at last, run the analyze
            CallAnalyze.Analyzer_ProteinIDs(session,protein_ids,feature_str)
            
        else:
            # no files upload,run analyze as normal
            print("No file uploaded.")
            idpairs_advance = request.form['idpairs_advance']
            select_advance = request.form['select_advance']
            idpairs_advance = idpairs_advance.replace("\r","")
            if idpairs_advance.count("\n") == 0:
                idpairs_advance += "\n"
    
            # secure the protein ids, get both valid and invalid protein ids
            protein_ids,invalid_ids =  CallAnalyze.Extract_Protein_Ids(idpairs_advance) 
            if len(protein_ids) < 1 or len(protein_ids[0]) < 2:
                return server_fault("Invalid Protein ID input.<br/> Please use comma,space as separtor.\
                        <br/>You may input less than two protein IDs or no valid protein ID pairs dectected!")

            # except, the features canbe changable here.
            CallAnalyze.Analyzer_ProteinIDs(session,protein_ids,feature_str)

            # after analyze done, we then make a file of protein ids 
            # into result/sessionid folder
            CallAnalyze.Save_ProteinID_List_TO_File(session,protein_ids)
        
        return redirect("/result/"+session)
    else:
        #no valid analyze type found? return error!.
        return server_fault("Analyze type not accepted!")

    return not_found(error="unknow analyze type.")

# error handlers for web interface.
# the two functions below are defined as 
# handler for 404 error and 500 error 
@app.errorhandler(404)
def not_found(error="The page you request not found on the server!",lastpage=""):
    return render_template("error.html",MESSAGE=error,LASTPAGE=lastpage),404

@app.errorhandler(500)
def server_fault(error,lastpage=""):
    return render_template("error.html",MESSAGE="Internal server error!<br>"+error,LASTPAGE=lastpage),500

################[function below used for test some features.]#####################3
###########[develop only. need to be commented on produce version]########################
#used for test error page
@app.route('/error')
def error():
    return render_template("error.html",MESSAGE="ERROR_MESSAGE")


if __name__ == '__main__':
    #app.run(host='192.168.81.218',port=80) # uncomment this line when running one beta.baderlab.org
    app.run(host='127.0.0.1',debug=True) # used for local test