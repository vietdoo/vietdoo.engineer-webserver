from app import app
from flask import render_template, request, Blueprint, g
import os
import pymongo
api_page = Blueprint('api', __name__, url_prefix='/api')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bigdata"]
chotot_lite = mydb["chotot_lite_fixed"]

@api_page.route('/v1.0/content/', methods=['GET'])
def get_html():
    url = request.args.get('url')
    print(url)
    r = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

    return r.content

@api_page.route('/v1.0/houses/', methods=['GET'])
def get_mongo():
 
    dist = request.args.get('dist')
    low = request.args.get('low')
    high = request.args.get('high')
    
    if (not low or not high):
      low = 0
      high = 2**50
    
    print("Filter: ", low, high, dist)  
    myquery = {}

    if (dist):
      myquery = {"$and":[ {"dist": dist}, {"price": {"$gt": int(low)}}, {"price": {"$lt": int(high)}}]}
    
    query_cursor = chotot_lite.find(myquery, {'_id': False})
    ans =  list(query_cursor)
    
    return ans
