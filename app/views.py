from flask import Flask, render_template, request, jsonify
import string
from pymongo import MongoClient
import re
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
    if(not city or not country):
        return;
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in word):
        return;
    result=db.USA.find( { "state": re.compile("^"+state), "city":re.compile("^"+city) } )
    return jsonify(result)


@app.route("/put", methods=['POST'])
def put():
    city = request.form.get('city')
    county = request.form.get('county')
    if(not city or not country):
        return;
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in word):
        return;
    result=db.command("db.USA.insert( { \"state\":\""+state+"\", \"city\":\""+city+"\" } )")

@app.route("/upload", methods=["POST"])
def upload():
    folder_name = request.form['superhero']
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, 'files/{}'.format(folder_name))
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)
