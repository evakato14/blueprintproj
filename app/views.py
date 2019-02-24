from flask import Flask, render_template, request, jsonify
import string
from pymongo import MongoClient
import re
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import watson_service
from bson.json_util import dumps
import json
import os
import numpy as np
import time
np.random.seed(42)
app = Flask(__name__)

client = MongoClient("mongodb://blueprint:aaaabbbb@blueprint-shard-00-00-jwwbc.mongodb.net:27017,blueprint-shard-00-01-jwwbc.mongodb.net:27017,blueprint-shard-00-02-jwwbc.mongodb.net:27017/test?ssl=true&replicaSet=Blueprint-shard-0&authSource=admin&retryWrites=true")
db=client.blueprint

apikey = 'CIh7yuw-FlXdpAyMBs2cMD9mX3-8OFt53uihYIvnMO04'
classifier_id = ''

timed = time.time()

def loadGloveEmbeddings():
    #Load Glove, a model of words to numbers
    # Stores a dictionary of words, with numbers corresponding
    print('Indexing word vectors.')
    BASE_DIR = 'C:\\Users\\azhan\\Downloads' #where glove file is
    GLOVE_DIR = BASE_DIR + '\\'
    #GLOVE_DIR = BASE_DIR + '\\glove.6B\\'#accesses glove file
    embeddings_index = {} #opens Glove
    f = open(os.path.join(GLOVE_DIR, 'glove.6B.50d.txt'), encoding="utf8")
    for line in f:
        values = line.split()
        word = values[0]#sets the word to 0th value in array
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    #index mapping words in the embeddings set
    #to their embedding vector
    f.close()
    return embeddings_index

def vectorDist(vec):
    sum = 0
    for val in vec:
        sum = sum + val ** 2
    return sum

embeddings_index = loadGloveEmbeddings()
print(time.time()-timed)

visual_creds = watson_service.load_from_vcap_services('watson_vision_combined')
apikey = "CIh7yuw-FlXdpAyMBs2cMD9mX3-8OFt53uihYIvnMO04" # visual_creds['apikey']
classifier_id = "waste_395176449" #set_classifier()

@app.route("/")
def render():
    return render_template('index.html')

@app.route("/retrieve", methods=['POST'])
def retrieve():
    print("Test")
    state = request.form.get('state')
    city = request.form.get('city')
    county = request.form.get('county')
    material = request.form.get('material')
    material = material.lower();
    if not city or not state or material not in embeddings_index:
        return;
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in state):
        return;
    result=db.USA.find( { "state": re.compile("^"+state), "city":re.compile("^"+city) } )
    #print(dumps(result))
    print(result[0])
    fin = result[0]
    minimumY = 50000.0
    minimumN = 50000.0
    pos_yes = ''
    pos_no = ''
    exclude = set(string.punctuation)

    for items in fin['metals'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        print(distan)
        if distan < minimumY:
            minimumY = distan
            pos_yes = "metals"
    for items in fin['paper'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumY:
            minimumY = distan
            pos_yes = "paper"
    for items in fin['glass'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumY:
            minimumY = distan
            pos_yes = "glass"
    for items in fin['plastics'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumY:
            minimumY = distan
            pos_yes = "plastics"
    for items in fin['other'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumY:
            minimumY = distan
            pos_yes = "other"
    for items in fin['nometals'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumN:
            minimumN = distan
            pos_no = "nometals"
    for items in fin['nopaper'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumN:
            minimumN = distan
            pos_no = "nopaper"
    for items in fin['noglass'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumN:
            minimumN = distan
            pos_no = "noglass"
    for items in fin['noplastics'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumN:
            minimumN = distan
            pos_no = "noplastics"
    for items in fin['noother'].split():
        items = ''.join(ch for ch in items if ch not in exclude)
        if(items.lower() not in embeddings_index):
            continue;
        distan = vectorDist(embeddings_index[material.lower()]-embeddings_index[items.lower()])
        if distan < minimumN:
            minimumN = distan
            pos_no = "noother"
    finalResult = ''
    if(minimumN<=minimumY):
        finalResult = "This item cannot be recycled in "+fin['city']+", "+fin['state']+". The following items cannot be recycled: " + fin[pos_no]
    else:
        finalResult = "This item can be recycled in "+fin['city']+", "+fin['state']+". The following items of the same type can be recycled: " + fin[pos_no]
    print(pos_yes + " | "+ pos_no)
    return jsonify({'success': finalResult} )
    # return dumps(result)


@app.route("/put", methods=['POST'])
def put():
    city = request.form.get('city')
    county = request.form.get('county')
    if not city or not country:
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
            print('Error')
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

# API destination
@app.route('/api/sort', methods=['POST'])
def sort():
    try:
        images_file = request.files.get('images_file', '')
        visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey=apikey)
        global classifier_id
        if classifier_id == '':
            classifier_id = set_classifier()
            if classifier_id == '':
                return json.dumps(
                    {"status code": 500, "result": "Classifier not ready",
                        "confident score": 0})
        parameters = json.dumps({'classifier_ids': [classifier_id]})
        url_result = visual_recognition.classify(
                         images_file=images_file,
                         parameters=parameters).get_result()
        if len(url_result["images"][0]["classifiers"]) < 1:
            return json.dumps(
                    {"status code": 500, "result": "Image is either not "
                        "a waste or it's too blurry, please try it again.",
                        "confident score": 0})
        list_of_result = url_result["images"][0]["classifiers"][0]["classes"]
        result_class = ''
        result_score = 0
        for result in list_of_result:
            if result["score"] >= result_score:
                result_score = result["score"]
                result_class = result["class"]
        return json.dumps(
            {"status code": 200, "result": result_class,
                "confident score": result_score})
    except Exception:
        return json.dumps(
            {"status code": 500, "result": "Not an image",
                "confident score": 0})

    # return send_from_directory("images", filename, as_attachment=True)
