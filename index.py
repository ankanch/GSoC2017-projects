import time
import flask
import os
from flask import Flask, jsonify, redirect, render_template, request,make_response

app = Flask(__name__)

UPLOAD_FOLDER = ".\\Cache\\uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This is the entrance URL for the index page
@app.route('/')
def index():
    return render_template("index.html")


# This is the result URL
# For test, I use some selected data to show how it looks
@app.route('/result')
def result():
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
    #       [       [result name,   [result list]  ] ,
    #               [sample result, [[result one],[result two],[...],...]  ]
    #               ,....  ]
    return render_template("result.html",result_package=test_set)



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
        local_file_list = request.files.getlist('local_files[]')
        print(local_file_list)
        if len(local_file_list)>0 :
            # if file length not equal to zero, this means user had select to upload a file to analyze
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], local_file.filename.replace(" ",""))
            local_file.save(filepath)
            print("fielen=",len(local_file_list))
        print("no upload.")
    else:
        #no valid analyze type found? return error!.
        pass

    return redirect('/')

#used for test redirect
#@app.route('/redirect')
#def redirect():
#    return render_template("redirect.html",TARGET="/")

if __name__ == '__main__':
    #app.run(host='10.105.91.217')
    app.run(host='127.0.0.1',debug=True)