import string
from pymongo import MongoClient

client = MongoClient("mongodb+srv://blueprint:aaaabbbb@blueprint-jwwbc.mongodb.net/blueprint?retryWrites=true")
#"mongodb://blueprint:aaaabbbb@blueprint-shard-00-00-jwwbc.mongodb.net:27017,blueprint-shard-00-01-jwwbc.mongodb.net:27017,blueprint-shard-00-02-jwwbc.mongodb.net:27017/blueprint?ssl=true&replicaSet=Blueprint-shard-0&authSource=admin&retryWrites=true"
db=client.blueprint

result=db.USA.insert_one( { "state":"state1", "city":"city1", "county":None} )
