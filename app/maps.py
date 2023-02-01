from app import app
from flask import render_template

@app.route('/maps')
def maps():
  return render_template('maps.html')
