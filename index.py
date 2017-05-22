import time
import flask
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



# This URL is used for normal analyze,which just input protein ids
# and select species
@app.route('/normal',methods=['POST'])
def normal_analyze():
    return redirect('/')

# This URL is for advance analyze,which will optimize a lot of
# settings or even upload coustom files to analyze
@app.route('/advance',methods=['POST'])
def advance_analyze():
    protein_id_list =  request.form['protein_id_list']
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename.replace(" ",""))
    file.save(filepath)
    return redirect('/')

#used for test redirect
#@app.route('/redirect')
#def redirect():
#    return render_template("redirect.html",TARGET="/")

if __name__ == '__main__':
    #app.run(host='10.105.91.217')
    app.run(host='127.0.0.1',debug=True)