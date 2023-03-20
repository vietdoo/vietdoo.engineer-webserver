from app import app
from flask import render_template, request, Blueprint, jsonify , after_this_request
from config import *
import os
import openai
import json
from dotenv import load_dotenv
load_dotenv()

chatbot_page = Blueprint('chatbot', __name__, url_prefix='/chatbot')

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin

token = GPT_TOKEN
openai.api_key = token

print("token:", token)

def generate_response(prompt):
    result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature = 0.9
    )

    print("waiting response from OPEN AI.")

    message = result.choices[0].message['content']
    return message


@chatbot_page.route('/')
def home():
    return render_template('chatbot/index.html')

@chatbot_page.route('/dev')
def homedev():
    return render_template('chatbot/index.html')

@chatbot_page.route('/text')
def text():
    return "Chào Fen !"


@cross_origin()
@chatbot_page.route("/", methods=['GET', 'POST'])
def chatbot():
    
    data = request.get_json()
    prompt = data["prompt"]
    print(prompt)
    #message = generate_response(prompt)
    message = "Mời bạn quay lại sau nhé, Bơ đang uống sữa🧂"
    print(message)
    return message



@chatbot_page.route('/test')
def test():
    print('testing route: on')
    return generate_response("chào bạn")