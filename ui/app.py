from flask import Flask, render_template, url_for

app = Flask(__name__)

#@app.before_request
#def before_request():
    # When you import jinja2 macros, they get cached which is annoying for local
    # development, so wipe the cache every request.
#    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
#        app.jinja_env.cache = {}

@app.route('/')
def layout():
    return render_template('layout.html')

@app.route('/about')
def about():
    return render_template('about.html')