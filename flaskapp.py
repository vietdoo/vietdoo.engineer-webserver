
import os, requests, torch, math, cv2
import numpy as np
import PIL

from flask import Flask,jsonify,request,render_template,send_from_directory
from source.utils import draw_rectangles, read_image, prepare_image
from model import *
from flask_cors import CORS, cross_origin

import pymongo

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
app = Flask(__name__, static_folder='static',)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = os.path.basename('uploads')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bigdata"]
chotot_lite = mydb["chotot_lite"]
chotot_lite = mydb["chotot_lite_fixed"]

@app.route('/')
def home():
  return render_template('index.html')

@app.route("/", subdomain="test")
def static_index():
    """Flask supports static subdomains
    This is available at static.your-domain.tld"""
    return "static.your-domain.tld"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = read_image(file)
    
    image, text = run_model(image)
    to_send = prepare_image(image)
    
    return render_template('index.html', face_detected=len(text)>0, num_faces=text, image_to_show=to_send, init=True)

@app.route('/api/v1.0/content/', methods=['GET'])
def get_html():
    url = request.args.get('url')
    print(url)
    r = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

    return r.content

@app.route('/api/v1.0/houses/', methods=['GET'])
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
      #myquery = {"price": {"$gt": low}}
      #myquery = {"$and":[ {"dist": dist}, {"price": {"$gt": low}}, {"price": {"$lt": high}}]}
      myquery = {"$and":[ {"dist": dist}, {"price": {"$gt": int(low)}}, {"price": {"$lt": int(high)}}]}
     # myquery = { "dist": dist, "price": {"$gt": low}, "price": {"$gt": low}}
     # myquery = { "dist": dist}
    
    
    query_cursor = chotot_lite.find(myquery, {'_id': False})
    ans =  list(query_cursor)
    #info = {'avg_price': 10000000, 'list_len': len(ans)}
    
    #ans.append(info)
    
    return ans
  
@app.route('/maps')
def maps():
  return render_template('maps.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0')

