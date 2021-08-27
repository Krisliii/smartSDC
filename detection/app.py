from flask import Flask, render_template, request, make_response
from random import randrange
from flask.json import jsonify
import getCountFromBlob 
import os

app = Flask(__name__, static_folder="templates")
#data = randrange(0, 60)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/randomData")
def randomData():
    #data = randrange(0, 60)
    data = getCountFromBlob.getCountData()
    print( data)
    return jsonify({"random_number": data})

if __name__ == "__main__":
    app.run() 
