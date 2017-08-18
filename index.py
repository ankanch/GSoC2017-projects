import time
import flask
import os
import shutil
from Utilities import globeVar
from Utilities import message as Message
from flask import Flask, jsonify, redirect, render_template, request,make_response,send_file,Response
from Utilities import SessionManager,ZipMaker,CallAnalyze,graph


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = globeVar.VAR_PATH_UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = globeVar.VAR_PATH_RESULT_FOLDER

# This is the entrance URL for the index page
@app.route('/')
def index():
    #Protein_id_list = CallAnalyze.Load_Protein_IDList()
    #return render_template("index.html",PID=Protein_id_list)
    # default mode is PPI-Pred
    return redirect("/ppipred")

# render analyze by protein ids
@app.route('/ppipred')
def function_ppipred():
    Protein_id_list = CallAnalyze.Load_Protein_IDList()
    return render_template("function_PPI_Pred.html",PID=Protein_id_list)

# render analyze by PWMs
@app.route('/pwms')
def function_pwms():
    pwm_list = CallAnalyze.Load_PWMs_List()
    return render_template("function_PWMs.html",PWM=pwm_list)


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
        return render_template("result.html",result_package=sample_result,SESSIONID=sessionid,TIME=["1.1.1.1","X"],PWM=True,CUR_PWM_VIEW=sample_result[0][0])
    # check session first
    if SessionManager.checkSession(sessionid):
        not_found(Message.MSG_ERROR_SESSION_NOT_FOUND)
    # before we print the result, we have to check analyze type,
    # to know it is analyzed by protein id pairs or PWMs
    try:
        analyze_type = SessionManager.getType(sessionid)
    except:
        return server_fault(Message.MSG_ERROR_INVALID_SESSION)

    folder_path = globeVar.VAR_PATH_RESULT_FOLDER + "/" + sessionid
    if analyze_type == "type_normal" or analyze_type == "type_advance":
        # then we open result.txt of that session folder and output the data
        # outputs types are : tabular,text and color density
        # result type will be flaged in the first line of the result.txt
        ff = open( folder_path + "/result.txt")
        input_ids = [line.replace("\n","") for line in open(folder_path + "/input_protein_ids.txt")][1:]
        css_selector_str = ""
        for idp in input_ids:
            idp = idp.split(",")
            css_selector_str+= " #"+idp[0]+", #"+idp[1]+","
        css_selector_str = css_selector_str[:len(css_selector_str)-1]
        print(css_selector_str)
        print(input_ids)
        data =  ff.readlines()
        ff.close()
        result_type = data[:1][0].replace("#","").replace("\n","").replace("\r","")
        data = data[2:]
        final_data = []
        for lines in data:
            pd = lines.replace("\n","").split(",")
            final_data.append(pd)
        create_time = [SessionManager.getDate(sessionid),str(SessionManager.VAR_RESULT_LIFE)]
        if result_type == globeVar.VAR_RESULTTYPE_TABULAR:
            return  render_template("result.html",result_package=final_data,SESSIONID=sessionid,TIME=create_time,INPUT_NODES=css_selector_str,TABULAR=True)
        elif result_type == globeVar.VAR_RESULTTYPE_TEXT:
            return  render_template("result.html",result_package=final_data,SESSIONID=sessionid,TIME=create_time,INPUT_NODES=css_selector_str,TEXT=True)
        elif result_type == globeVar.VAR_RESULTTYPE_COLOR:
            # here we have do a convert, the color cell's color is from RGB(204,255,204) to RGB(0,255,0)
            # therefor, we will made the convert here
            row_num = 0
            ele_num = 0
            for row in final_data:
                for ele in row:
                    if ele_num > 2 and ele_num < 7:
                        if ele != "None":
                            XSC = int(float(ele)*204)
                            print "XSC=",XSC,"\tfloat(ele)=",float(ele),"\tele=",ele
                            if XSC < 0:
                                XSC*=-1
                            final_data[row_num][ele_num] = 204 - XSC
                    ele_num+=1
                ele_num = 0
                row_num+=1
            print final_data
            return  render_template("result.html",result_package=final_data,SESSIONID=sessionid,TIME=create_time,INPUT_NODES=css_selector_str,COLOR=True)
    elif SessionManager.getType(sessionid) == "type_pwm":
        # get all result files then read them one by one
        result_file_list = [x for x in os.listdir(folder_path) if x.find("_result.txt")>-1]
        result = []
        for index,rfile in enumerate(result_file_list):
            ff = open(folder_path + "/" + rfile)
            dta =  ff.readlines()
            ff.close()
            # split the data
            pdata = [x.replace("\n","").split("\t") for x in dta]
            result_name = pdata[1][0]
            result.append([result_name,pdata[1:]])    # result_name stores the name of this result.
        create_time = [SessionManager.getDate(sessionid),str(SessionManager.VAR_RESULT_LIFE)]
        return render_template("result.html",result_package=result,SESSIONID=sessionid,TIME=create_time,PWM=True,CUR_PWM_VIEW=result_name)
    

@app.route('/download/<sessionid>')
def download(sessionid):
    # first,we have to check if the result user looking for is exist
    # normally,the  result file will have the same filename (session id )
    # with the upload folder
    if sessionid not in os.listdir(globeVar.VAR_PATH_RESULT_FOLDER):
        return not_found(Message.MSG_ERROR_FILE_NOT_FOUND,"/result/"+sessionid)
    
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

    #get public field between normal analyze and advance analyze
    idpairs = request.form['idpairs']
    species = request.form['species']
    idpairs = idpairs.replace("\r","")
    if idpairs.count("\n") == 0:
        idpairs += "\n"

    # Start processing user's options on analyzing
    if analyze_type == "normal":
        SessionManager.setType(session,"type_normal")

        # here we call functions to check if the ids user input satisfy the creteria that
        # every line must only contains two protein ids. Function below will help us extract 
        # both satisfied and unsatisfied protein ids.
        protein_ids,invalid_ids =  CallAnalyze.Extract_Protein_Ids(idpairs)
        if len(protein_ids) < 1 or len(protein_ids[0]) < 2:
            return server_fault(Message.MSG_ERROR_INVALID_PROTEIN_IDS)
        #then we call function Analyzer_ProteinIDs from CallAnalyze to analyze
        CallAnalyze.Analyzer_ProteinIDs(session,protein_ids)

        # after analyze done, we then make a file of protein ids 
        # into result/sessionid folder
        CallAnalyze.Save_ProteinID_List_TO_File(session,protein_ids,species)
        graph.generate_graph(session)
        
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

        # get result type which describes how to display the result to users
        output_type = request.form['outputs']

        # check if user upload a file.
        if len(id_file.filename) > 0:
            # save the file to the disk first.
            filepath = os.path.join(analyzing_target_dir, id_file.filename.replace(" ",""))
            id_file.save(filepath)

            # then, we  secure the protein ids, get both valid and invalid protein ids
            # let Extract_Protein_Ids help us to reads the data,and run analyze for us.
            protein_ids,invalid_ids =  CallAnalyze.Extract_Protein_Ids(filepath,True) 
            if len(protein_ids) < 1 or len(protein_ids[0]) < 2:
                return server_fault(Message.MSG_ERROR_INVALID_PROTEIN_IDS)

            # at last, run the analyze
            CallAnalyze.Analyzer_ProteinIDs(session,protein_ids,feature_str,output_type)
            
        else:
            # no files upload,run analyze as normal
            print("advance:No file uploaded.")
    
            # secure the protein ids, get both valid and invalid protein ids
            protein_ids,invalid_ids =  CallAnalyze.Extract_Protein_Ids(idpairs) 
            if len(protein_ids) < 1 or len(protein_ids[0]) < 2:
                return server_fault(Message.MSG_ERROR_INVALID_PROTEIN_IDS)

            # except, the features canbe changable here.
            CallAnalyze.Analyzer_ProteinIDs(session,protein_ids,feature_str,output_type)

            # after analyze done, we then make a file of protein ids 
            # into result/sessionid folder
            CallAnalyze.Save_ProteinID_List_TO_File(session,protein_ids,species)
            graph.generate_graph(session)
        # return the result
        
        return redirect("/result/"+session)
    else:
        #no valid analyze type found? return error!.
        return server_fault("Analyze type not accepted!")

    return not_found(error="unknow analyze type.")


# this function is used to run analyze by PWMs
@app.route('/runanalyze_pwms',methods=['POST'])
def runanalyze_pwms():
    if request.method == 'POST':
        # coe below is used to detect if user want to use built in domain data and PWMs data.
        use_builtin_pwms =  'true'
        use_built_in_domain = 'true'
        try:
            use_builtin_pwms = request.form['use_builtin_pwms']
        except:
            use_builtin_pwms = 'false'
        try:
            use_built_in_domain = request.form['use_builtin_domain']
        except:
            use_built_in_domain = 'false'

        # request for real data used for analyzing
        built_in_pwms = request.form["pwms"]
        pwmfilelist = None
        if use_builtin_pwms == 'false':
            pwmfilelist = request.files.getlist("file[]")
        dofile = None
        UBI = True # UBI stands for [use built in] domain file
        if use_built_in_domain == 'false':
            UBI = False
            dofile = request.files['domainfile']

        # request features that want to used in analyze
        features = request.form.getlist('features[]')
        feature_str = CallAnalyze.getFeatures(features)

        #generate session id for organising the upload files
        #all files that upload are in the same session folder
        session = SessionManager.generateSessionID()
        SessionManager.addSession(session)
        store_path = app.config['UPLOAD_FOLDER']+"/"+session 
        os.makedirs(store_path)
        SessionManager.setType(session,"type_pwm")

        # domain file
        if UBI == False:
            # save user uploaded domain file to the target session folder
            dofile.save(store_path + "/domain.txt")
        else:
            # copy internal domain file to the target session folder
            shutil.copy2("./data/domain.txt",store_path + "/domain.txt" )
        # here, we check wether user slect to use built in PWMs or they want to use their own.
        # if the variable built_in_pwms not null, then we assume user choose use built-in, otherwise,their own
        pwmfiles = []
        if use_builtin_pwms == 'false':
            # user choose to use their own PWMs
            # then save uploaded pwmfile for further pocess
            for file in pwmfilelist:
                file_path = os.path.join(store_path + "/", file.filename.replace(" ","_") )
                file.save(file_path)
                pwmfiles.append(file_path)
        else:
            # user choose to use built in PWMs
            pwm_ids = [x for x in built_in_pwms.split(",") if len(x)>0]

            # then we copy these built-in PWMs to seesion folder
            for pwm in pwm_ids:
                pwm_path = store_path + "/" + pwm 
                shutil.copy2(globeVar.VAR_PATH_PWMS+pwm,pwm_path)
                pwmfiles.append(pwm_path)
                    # start analyze
        
        # then we run the normal analyze.
        print "feature_string=",feature_str
        CallAnalyze.Analyzer_PWMs(session,[False,pwmfiles],store_path+"/domain.txt",feature_str)
        
        #after operation above,data had been put into cache/output/pwmfilename
        return redirect("/result/"+session)


    print Message.MAS_ERROR_METHOD_NOT_SUPPORT
    return not_allowed()

# error handlers for web interface.
# the two functions below are defined as 
# handler for 404 error and 500 error 
@app.errorhandler(404)
def not_found(error=Message.MSG_ERROR_PAGE_NOT_FOUND,lastpage=""):
    return render_template("error.html",MESSAGE=error,LASTPAGE=lastpage),404

@app.errorhandler(500)
def server_fault(error,lastpage=""):
    return render_template("error.html",MESSAGE="Internal server error!<br>"+str(error),LASTPAGE=lastpage),500

@app.errorhandler(403)
def not_allowed(error=Message.MSG_ERROR_NOT_ALLOWED,lastpage=""):
    return render_template("error.html",MESSAGE=error,LASTPAGE=lastpage),403

################[function below used for test some features.]#####################3
###########[develop only. need to be commented on produce version]########################
#used for test error page
@app.route('/error')
def error():
    return render_template("error.html",MESSAGE="ERROR_MESSAGE")

@app.route('/test_cyto')
def test_cyto():
    return render_template("test_cyto.html")

@app.route('/getgexf/<session>')
def send_gexf(session):
    ff = open(globeVar.VAR_PATH_RESULT_FOLDER+"/"+session+"/network.gexf")
    data = ff.read()
    ff.close()
    return Response(data, mimetype='text/plain')

@app.route('/getjson/<session>')
def send_json(session):
    ff = open(globeVar.VAR_PATH_RESULT_FOLDER+"/"+session+"/network.json")
    data = ff.read()
    ff.close()
    return Response(data, mimetype='text/plain')

if __name__ == '__main__':
    if "mode.server" in os.listdir("./"):
        # when a specific file in current dir,bind IP below  
        # running on beta.baderlab.org
        print ">>>Running as server mode,use http://beta.baderlab.org to visit."
        app.run(host='192.168.81.218',port=80)
    else:
        # local machine for test
        print ">>>Running on local machine."
        app.run(host='127.0.0.1',debug=True)