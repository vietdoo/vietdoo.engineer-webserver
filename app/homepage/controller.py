from app import app
from flask import render_template, request, Blueprint

home_page = Blueprint('home', __name__, url_prefix='/')

@home_page.route('/')
def home():
  return render_template('homepage/index.html')


@home_page.route('/', subdomain ='practice')
def practice():
    return "Coding Practice Page"