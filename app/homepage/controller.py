from app import app
from flask import render_template, redirect, request, Blueprint

home_page = Blueprint('home', __name__, url_prefix='/')

@home_page.route('/')
def home():
  return render_template('homepage/index.html')

@home_page.route('/cv')
def test():
  #return '<iframe src="https://docs.google.com/gview?url=https://vietdoo.me/assets/documents/DoQuocViet_DE.pdf&embedded=true" style="width:100%; height:100%;" frameborder="0"></iframe>'
  #return send_from_directory(app.config['UPLOAD_FOLDER'], 'homepage/DoQuocViet_DE.pdf')
  return '<title>Do Quoc Viet | Data Engineer</title>  <object data="../static/homepage/DoQuocViet_DE.pdf" type="application/pdf" width="100%" height="100%"><embed src="https://vietdoo.me/assets/documents/DoQuocViet_DE.pdf" type="application/pdf"><p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://vietdoo.me/assets/documents/DoQuocViet_DE.pdf">Download PDF</a>.</p></embed> </object>'  


