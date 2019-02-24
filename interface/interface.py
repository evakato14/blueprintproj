from flask import Flask, render_template, request
import string
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient("mongodb+srv://blueprint:aaaabbbb@blueprint-jwwbc.mongodb.net/blueprint?retryWrites=true")
#"mongodb://blueprint:aaaabbbb@blueprint-shard-00-00-jwwbc.mongodb.net:27017,blueprint-shard-00-01-jwwbc.mongodb.net:27017,blueprint-shard-00-02-jwwbc.mongodb.net:27017/blueprint?ssl=true&replicaSet=Blueprint-shard-0&authSource=admin&retryWrites=true"
db=client.blueprint

@app.route("/")
def render():
    return render_template('interface.html')

@app.route('/retrieve', methods=['POST'])
def retrieve():
    print("Recieved")
    city = request.form.get('city')
    county = request.form.get('county')
    state = request.form.get('state')
    metals = request.form.get('metals')
    metals_info = request.form.get('metals_info')
    plastics = request.form.get('plastics')
    plastics_info = request.form.get('plastics_info')
    paper = request.form.get('paper')
    paper_info = request.form.get('paper_info')
    glass = request.form.get('glass')
    glass_info = request.form.get('glass_info')
    other = request.form.get('other')
    other_info = request.form.get('other_info')
    result=db.USA.insert_one( { "state":state, "city":city, "county":county, "metals":metals, "metals_info":metals_info, "plastics":plastics, "plastics_info":plastics_info,"paper":paper, "paper_info":paper_info, "glass":glass, "glass_info":glass_info, "other":other, "other_info":other_info } )

if __name__ == '__main__':
    app.run(debug=True)
