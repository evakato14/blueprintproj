from flask import Flask, render_template, request, jsonify
import string
from pymongo import MongoClient
import re
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import watson_service
from bson.json_util import dumps
app = Flask(__name__)

client = MongoClient("mongodb://blueprint:aaaabbbb@blueprint-shard-00-00-jwwbc.mongodb.net:27017,blueprint-shard-00-01-jwwbc.mongodb.net:27017,blueprint-shard-00-02-jwwbc.mongodb.net:27017/test?ssl=true&replicaSet=Blueprint-shard-0&authSource=admin&retryWrites=true")
db=client.blueprint

apikey = 'CIh7yuw-FlXdpAyMBs2cMD9mX3-8OFt53uihYIvnMO04'
classifier_id = ''


# Set Classifier ID
def set_classifier():
    visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey=apikey)
    classifiers = visual_recognition.list_classifiers().get_result()
    for classifier in classifiers['classifiers']:
        if classifier['name'] == 'waste':
            if classifier['status'] == 'ready':
                return classifier['classifier_id']
            else:
                return ''
    create_classifier()
    return ''


# Create custom waste classifier
def create_classifier():
    visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey=apikey)
    with open('./resources/landfill.zip', 'rb') as landfill, open(
        './resources/recycle.zip', 'rb') as recycle, open(
            './resources/compost.zip', 'rb') as compost, open(
                './resources/negative.zip', 'rb') as negative:
        visual_recognition.create_classifier(
            'waste',
            Landfill_positive_examples=landfill,
            Recycle_positive_examples=recycle,
            Compost_positive_examples=compost,
            negative_examples=negative)
    return ''

visual_creds = watson_service.load_from_vcap_services('watson_vision_combined')
apikey = "CIh7yuw-FlXdpAyMBs2cMD9mX3-8OFt53uihYIvnMO04" # visual_creds['apikey']
#classifier_id = set_classifier()

@app.route("/")
def render():
    return render_template('index.html')

@app.route("/retrieve", methods=['POST'])
def retrieve():
    print("Test")
    state = request.form.get('state')
    city = request.form.get('city')
    county = request.form.get('county')
    if(not city or not state):
        return;
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in state):
        return;
    result=db.USA.find( { "state": re.compile("^"+state), "city":re.compile("^"+city) } )
    print(dumps(result))
    return jsonify(dumps(result))


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
        visual_recognition = VisualRecognitionV3('2018-03-19',
                                                 iam_apikey=apikey)
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

@app.route('/interface', methods=['GET', 'POST'])
def interface():
    if request.method == "GET":
        return render_template('interface.html')
    city = request.form.get('city')
    county = request.form.get('county')
    state = request.form.get('state')
    metals = request.form.get('metals')
    nometals = request.form.get('nometals')
    metals_info = request.form.get('metals_info')
    plastics = request.form.get('plastics')
    noplastics = request.form.get('noplastics')
    plastics_info = request.form.get('plastics_info')
    paper = request.form.get('paper')
    nopaper = request.form.get('nopaper')
    paper_info = request.form.get('paper_info')
    glass = request.form.get('glass')
    noglass = request.form.get('noglass')
    glass_info = request.form.get('glass_info')
    other = request.form.get('other')
    noother = request.form.get('noother')
    other_info = request.form.get('other_info')
    result=db.USA.insert_one( { "state":state, "city":city, "county":county, "metals":metals, "nometals":nometals, "metals_info":metals_info, "plastics":plastics, "noplastics":noplastics, "plastics_info":plastics_info,"paper":paper, "nopaper":nopaper, "paper_info":paper_info, "glass":glass, "noglass":noglass, "glass_info":glass_info, "noother":other, "other":noother, "other_info":other_info } )
    print(result)
    return;

    # return send_from_directory("images", filename, as_attachment=True)
