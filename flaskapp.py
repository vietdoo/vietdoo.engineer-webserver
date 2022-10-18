
import os, requests, torch, math, cv2
import numpy as np
import PIL

if os.getcwd()=="/content":
  os.chdir("YOLOv6")

from yolov6.utils.events import LOGGER, load_yaml
from yolov6.layers.common import DetectBackend
from yolov6.data.data_augment import letterbox
from yolov6.utils.nms import non_max_suppression
from yolov6.core.inferer import Inferer

from typing import List, Optional

from flask import Flask,jsonify,request,render_template,send_from_directory
from source.utils import draw_rectangles, read_image, prepare_image
#from source.source import detect_faces_with_ssd, run_model

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
    image = run_model(image)
    to_send = prepare_image(image)
    faces = [1, 2]
    return render_template('index.html', face_detected=len(faces)>0, num_faces=len(faces), image_to_show=to_send, init=True)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
