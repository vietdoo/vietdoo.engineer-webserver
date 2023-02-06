from . import app

@app.route('/search', subdomain='admin')
def api_search():
    return "Coding Practice Page"