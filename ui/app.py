from flask import Flask, render_template, url_for, request, session, flash, redirect
import os
import json
import io
from time import time

app = Flask(__name__)
app.secret_key = str(os.urandom(24))
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')


@app.route('/', methods=['GET','POST'])
def layout():
    if not 'new' in session:
        session['new'] = True
        session['path'] = ''
        session['to_build'] = False
        session['build'] = False
        session['query'] = False
        session['results'] = []
        session['user'] = 'andy'
        session['in_ts'] = 0
        session['out_ts'] = 0  
    return redirect(url_for('index'))

@app.route('/index', methods=['GET','POST'])
def index():
    input = readjson()
    if not input == 0:
        session['to_build'] = False
        session['build'] = True
    if session['to_build']:
        return 'Loading (GIF)'
    if request.method == 'POST':
        if 'path' in request.form:
            build()
        elif 'query' in request.form:
            query()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

def build():
    if os.path.exists(request.form['path']):
        session['to_build'] = True
        session['path'] = request.form['path']
        flash('Path is valid, model is being constructed', 'message')
        result = {"action" : "build",
                "path" : session['path']}
        printjson(result)
    else:
        session['to_build'] = False
        flash('Path is Wrong, no new model for construction', 'Error')
    
    return redirect(url_for('index'))

def query():
    if session['query'] and session['build']:
        readjson()        
    elif session['build']:
        result = {"action" : "query",
                "query" : request.form['query'],
                "count": request.form['count']}
        session['query'] = True
        printjson(result)
    else:
        flash('No Model has been created')
    return redirect(url_for('index'))

def printjson(data):
    with io.open(os.path.pardir + '/json/out.ui.json', 'w', encoding='utf8') as outfile:
        data['time'] = time()
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

def readjson():
    try:
        with io.open(os.path.pardir + '/json/in.ui.json', 'r', encoding='utf8') as infile:
            data = json.load(infile)
            if not data['time'] == session['in_ts']:
                session['in_ts'] = data['time']
                return data
    except IOError as error:
        flash(error)
    return 0