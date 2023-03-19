from app import app
from flask import render_template, request, Blueprint, jsonify 
import os
import openai
import json

chatbot_page = Blueprint('chatbot', __name__, url_prefix='/chatbot')

from flask import Flask, render_template, request, redirect, url_for, send_from_directory

token = os.getenv('GPTAPI')
openai.api_key = token

print("token:", token)

def generate_response(prompt):
    result = openai.ChatCompletion.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7
    )

    # response = openai.Completion.create(
    #     engine="text-davinci-003", prompt=prompt, max_tokens=20, n=1,stop=None,temperature=0.7
    # )
    # message = response.choices[0].text.strip()
    # return message

    message = result.choices[0].message['content']
    return message

@chatbot_page.route('/')
def home():
    return render_template('chatbot/index.html')

@chatbot_page.route('/text')
def text():
    return "Chào Fen !"

@chatbot_page.route("/response", methods=["POST"])
def chatbot():
    data = request.get_json()
    prompt = data["prompt"]
    message = generate_response(prompt)
    print(message)
    return message

