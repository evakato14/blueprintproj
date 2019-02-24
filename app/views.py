from flask import Flask, render_template, request
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient("mongodb://blueprint:aaaabbbb@blueprint-shard-00-00-jwwbc.mongodb.net:27017,blueprint-shard-00-01-jwwbc.mongodb.net:27017,blueprint-shard-00-02-jwwbc.mongodb.net:27017/test?ssl=true&replicaSet=Blueprint-shard-0&authSource=admin&retryWrites=true")
db=client.blueprint

@app.route("/")
def render():
    return render_template('index.html')

@app.route("/retrieve", methods=['POST'])
def retrieve():
    city = request.form.get('city')
    county = request.form.get('county')

@app.route("/put")
def render():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
