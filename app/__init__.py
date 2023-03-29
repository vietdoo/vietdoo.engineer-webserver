from flask import Flask, jsonify, request, render_template, send_from_directory, g

import os, requests, torch, math, cv2
import numpy as np
import PIL

from flask import Flask
from flask_cors import CORS, cross_origin

import openai
import socket
import pymongo

from config import *
import mysql.connector



# Preparing SQL query to INSERT a record into the database.
conn = mysql.connector.connect(
   user = MYSQL_USER, password = MYSQL_PASSWORD, host = 'awsmysql.c3iit2fpwhsr.ap-southeast-1.rds.amazonaws.com', database = 'chatbot')

cursor = conn.cursor()



#conn.close()

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
app = Flask(__name__, static_folder='static',)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = os.path.basename('uploads')

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response

from app.homepage.controller import home_page as page_module
app.register_blueprint(page_module)

from app.detection.controller import detection_page as detection_module
app.register_blueprint(detection_module)

from app.api.controller import api_page as api_module
app.register_blueprint(api_module)

if socket.gethostname() in ('TheMaster'):
    print("LOCAL")
else:
    print("ONLINE")
    from app.rhymes.controller import rhymes_page as rhymes_module
    app.register_blueprint(rhymes_module)

from app.chatbot.controller import chatbot_page as chatbot_module
app.register_blueprint(chatbot_module)

from app import maps


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')