import time
import flask
from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    #app.run(host='10.105.91.217')
    app.run(host='127.0.0.1',debug=True)