from app import app
from flask import render_template, request, Blueprint
import os

from app.detection.source.utils import draw_rectangles, read_image, prepare_image
from app.detection.model import *

home_page = Blueprint('home', __name__, url_prefix='/')

@home_page.route('/')
def home():
  return render_template('index.html')

@home_page.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    image = read_image(file)
    
    image, text = run_model(image)
    to_send = prepare_image(image)
    
    return render_template('index.html', face_detected=len(text)>0, num_faces=text, image_to_show=to_send, init=True)
