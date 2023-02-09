import requests
import pymongo
import sys
import json
from bson.json_util import dumps
from bson.json_util import loads
import urllib.request
urllib.request.urlretrieve("https://tigerlake.s3.ap-southeast-1.amazonaws.com/mongo.json", filename = "mongo.json")
print('Fetch new Json: OK')

#local
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

#remote
#myclient = pymongo.MongoClient("mongodb://128.199.251.39:27017/")

mydb = myclient["bigdata"]
chotot_lite = mydb["chotot_lite_fixed"]
print('Connect to mongodb: OK')

print('Delete:', chotot_lite.delete_many({}).deleted_count)
input_data = json.load(open('mongo.json'))
chotot_lite.insert_many(input_data)

print('Insert: OK')
