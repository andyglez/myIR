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
        return get_index()
    elif request.method == 'POST':
        session['results'] = []
        if 'update' in request.form:
            flash('Model is being constructed, please wait and try again') 
        elif 'another' in request.form:
            session['build'] = False
        elif 'path' in request.form:
            build(request.form['path'])
        elif 'query' in request.form:
            query()
        elif 'other' in request.form:
            session['query'] = False
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
        session['query_msg'] = request.form['query']
        printjson(result)
    else:
        flash('No Model has been created')
    return 'query'#redirect(url_for('index'))

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
    if valid_time(in_data) and has_fields(in_data):
        if in_data['type'] == 'build':
            if in_data['success']:
                session['build'] = True
                session['in_ts'] = in_data['time']
                session['to_build'] = False
                flash('Model successfully built in ' + str(in_data['time'] - session['out_ts']) + ' seconds')
            else:
                flash('Task incomplete')
        elif in_data['type'] == 'query':
            if in_data['success']:
                session['query'] = True
                session['query_sent'] = False
                session['in_ts'] = in_data['time']
                flash('Completed query '+ session['query_msg'] + ' in ' + str(in_data['time'] - session['out_ts']) + ' seconds')
                if 'results' in in_data:
                    session['results'] = in_data['results']
            else:
                session['query_sent'] = False
                session['query'] = False
                # session['results'] = []
                # session['in_ts'] = in_data['time']
                flash('Sorry, no items match your query')
    return render_template('index.html')


def build_completion(data):
    return valid_time(data) and has_fields(data) and data['type'] == 'build' and data['success']

def query_completion(data):
    return valid_time(data) and has_fields(data) and data['type'] == 'query' and data['success']

def valid_time(data):
    return 'time' in data and data['time'] > session['in_ts']

def has_fields(data):
    return 'type' in data and 'success' in data

@app.route('/eval')
def eval():
    querys = [
        {'query': 'leon', 'measures': {'precision': 1, 'rec': 1, 'F': 1, 'E': 1, 'R' : 1}},
        {'query': 'duck', 'measures': {'precision': 1, 'rec': 1, 'F': 1, 'E': 1, 'R' : 1}},
        {'query': 'fox', 'measures': {'precision': 1, 'rec': 1, 'F': 1, 'E': 1, 'R' : 1}},
        {'query': 'leon fox duck', 'measures': {'precision': 1, 'rec': 1, 'F': 1, 'E': 1, 'R' : 1}},
        {'query': 'leon duck', 'measures': {'precision': 1, 'rec': 1, 'F': 1, 'E': 1, 'R' : 1}},
        {'query': 'leon andy', 'measures': {'precision': 0, 'rec': 0, 'F': 0, 'E': 0, 'R' : 0}}]
    session['eval'] = querys
    return render_template('eval.html')