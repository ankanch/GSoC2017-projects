import time
import flask
import os
from flask import Flask, jsonify, redirect, render_template, request,make_response,send_file
from Utilities import SessionManager

app = Flask(__name__)

UPLOAD_FOLDER = "./Cache/uploads"
RESULT_FOLDER = "./Cache/results"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This is the entrance URL for the index page
@app.route('/')
def index():
    return render_template("index.html")


# This is the result URL
# For test, I use some selected data to show how it looks
@app.route('/result/<sessionid>')
def result(sessionid):
    test_set=[[0,[["P15891","Q06604",427,436,"PAIPQKKSFL",0.94,4,0.95,4,1.0],
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
    return render_template("result.html",result_package=test_set,SESSIONID=sessionid)

@app.route('/download/<sessionid>')
def download(sessionid):
    # first,we have to check if the result user looking for is exist
    # normally,the  result file will have the same filename (session id )
    # with the upload folder
    if sessionid not in os.listdir(RESULT_FOLDER):
        return not_found("FIle not found on this server. The result you looking for might be removed.","/result/"+sessionid)
    # file exist, then we return then we check if an zipped file with the 
    # same name as the folder, if exist, return it. Otherwise, we have to 
    # make all files in current folder into a single zip file,then return it.
    if sessionid+".zip" in os.listdir(RESULT_FOLDER+"/"+sessionid):
        # return the exist zip file. 
        pass
    # compress all files then return it.


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
    

    if analyze_type == "normal":
        #user select normal analyze, which requires him to input protein id pairs and select species
        idpairs_normal = request.form['idpairs_normal']
        select_normal = request.form['select_normal']
    elif analyze_type == "advance":
        #user select advance analyze,which need to customize a lot of options.
        idpairs_advance = request.form['idpairs_advance']
        select_advance = request.form['select_advance']
        features = request.form.getlist('features[]')
        file_list = request.files.getlist('files[]')
        # check if user upload a file.
        if len(file_list)>0 :
            # if file length not equal to zero, this means user had select to upload a file to analyze
            # then we're going to traverse the file list to save them in Cache folder with sub-directory
            # named by session id. Therefore, 1).we need also generate a session id here.
            # 2).Then we make a directory with the name of seesion id
            # 3).At last,we save all the user upload files to the folder.
            print("User upload files.With length of ",len(file_list))
            sessionid = SessionManager.generateSessionID()
            file_target_dir = app.config['UPLOAD_FOLDER']+"/"+sessionid
            os.mkdir(file_target_dir)
            for file in file_list:
                filepath = os.path.join(file_target_dir, file.filename.replace(" ",""))
                file.save(filepath)
            print("files saved to ",file_target_dir,"\nStart running analyze...")
        else:
            # no files upload,use built in protein ids.
            print("No files uploaded.")
    else:
        #no valid analyze type found? return error!.
        server_fault("Analyze type not accepted!")

    return "1"

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
#used for test redirect
@app.route('/redirect')
def redirect():
    return render_template("redirect.html",TARGET="/")
#used for test error page
@app.route('/error')
def error():
    return render_template("error.html",MESSAGE="ERROR_MESSAGE")


if __name__ == '__main__':
    #app.run(host='10.105.91.217')
    app.run(host='127.0.0.1',debug=True)