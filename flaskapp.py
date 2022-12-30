<<<<<<< HEAD
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

@app.route('/')
def home():
  return render_template('index.html')

# @app.route('/detect', methods=['POST'])
# def detect():
#     file = request.files['image']
#     image = read_image(file)
#     faces = run_model(image, model5)
#     return jsonify(detections = faces)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = read_image(file)
    
    image, text = run_model(image)
    to_send = prepare_image(image)
    
    return render_template('index.html', face_detected=len(text)>0, num_faces=text, image_to_show=to_send, init=True)

@app.route('/api/v1.0/houses/', methods=['GET'])
def get_mongo():
    
    dist = request.args.get('dist')
    print(dist)
    
    myquery = {}
    if (dist):

    	myquery = { "dist": dist }
    query_cursor = chotot_lite.find(myquery, {'_id': False})
    
    return list(query_cursor)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')

    
=======
import os, requests, torch, math, cv2
import numpy as np
import PIL

from flask import Flask,jsonify,request,render_template,send_from_directory
from source.utils import draw_rectangles, read_image, prepare_image
from model import *

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
app = Flask(__name__, static_folder='static',)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = os.path.basename('uploads')

@app.route('/')
def home():
  return render_template('index.html')

# @app.route('/detect', methods=['POST'])
# def detect():
#     file = request.files['image']
#     image = read_image(file)
#     faces = run_model(image, model5)
#     return jsonify(detections = faces)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = read_image(file)
    
    image, text = run_model(image)
    to_send = prepare_image(image)
    
    return render_template('index.html', face_detected=len(text)>0, num_faces=text, image_to_show=to_send, init=True)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
>>>>>>> origin/main
