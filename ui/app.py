from flask import Flask, render_template, url_for, request, session, flash, redirect
import os
import json
import io
import threading
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
        session['query_sent'] = False
        session['query'] = False        
        session['results'] = []
        session['user'] = 'andy'
        session['in_ts'] = time()
        session['out_ts'] = time()
    return redirect(url_for('index'))

@app.route('/index', methods=['GET','POST'])
def index():
    if not 'new' in session:
        return layout()
    if request.method == 'GET':
        get_index()
    elif request.method == 'POST':
        if 'update' in request.form:
            flash('Model is being constructed, please wait and try again') 
        elif 'another' in request.form:
            session['build'] = False
        elif 'path' in request.form:
            build(request.form['path'])
        elif 'query' in request.form:
            query()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

def build(path):
    if os.path.exists(path):
        session['to_build'] = True
        session['path'] = path
        flash('Path is valid, model is being constructed', 'message')
        result = {"action" : "build",
                "path" : session['path']}
        printjson(result)
    else:
        session['to_build'] = False
        flash('Path is Wrong, no new model for construction', 'Error')
    
    return 'build'

def query():    
    if session['build']:
        result = {"action" : "query",
                "query" : request.form['query'],
                "count": request.form['count']}
        session['query_sent'] = True
        printjson(result)
    else:
        flash('No Model has been created')
    return redirect(url_for('index'))

def printjson(data):
    with io.open(os.path.pardir + '/json/out.ui.json', 'w', encoding='utf8') as outfile:
        data['time'] = time()
        session['out_ts'] = data['time']
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

def readjson():
    try:
        with io.open(os.path.pardir + '/json/in.ui.json', 'r', encoding='utf8') as infile:
            return json.load(infile)
    except IOError as error:
        flash(error)

def get_index():
    in_data = readjson()
    if session['to_build'] and build_completion(in_data):
        session['build'] = True
        session['to_build'] = False
        session['in_ts'] = in_data['time']
        flash('Model successfully built in ' + str(in_data['time'] - session['out_ts']) + ' seconds')
    elif session['query_sent'] and query_completion(in_data):
        session['query'] = True
        session['query_sent'] = False
        session['in_ts'] = in_data['time']
        flash('Completed query in ' + str(in_data['time'] - session['out_ts']) + ' seconds')

def build_completion(data):
    return valid_time(data) and has_fields(data) and data['type'] == 'build' and data['success']

def query_completion(data):
    return valid_time(data) and has_fields(data) and data['type'] == 'query' and data['success']

def valid_time(data):
    return 'time' in data and data['time'] > session['in_ts']

def has_fields(data):
    return 'type' in data and 'success' in data
            