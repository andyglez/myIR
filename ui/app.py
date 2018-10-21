from flask import Flask, render_template, url_for, request, session, flash, redirect
import os
import json
import io

app = Flask(__name__)
app.secret_key = str(os.urandom(24))
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')


@app.route('/', methods=['GET','POST'])
def layout():
    session['path'] = ''
    session['build'] = False
    session['query'] = False
    session['results'] = []
    session['user'] = 'andy'    
    return redirect(url_for('index'))

@app.route('/index', methods=['GET','POST'])
def index():
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
        session['build'] = True
        session['path'] = request.form['path']
        flash('Path is valid, model is being constructed', 'message')
        result = {"action" : "build",
                "path" : session['path']}
        printjson(result)
    else:
        session['build'] = False
        flash('Path is Wrong, no new model for construction', 'Error')
    
    return redirect(url_for('static', filename='json/action.json'))

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
    with io.open(os.path.curdir + url_for('static', filename='json/action.json'), 'w', encoding='utf8') as outfile:
        text = json.dumps(data,
                    indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)

def readjson():
    with io.open(os.path.curdir + url_for('static', filename='json/action.json'), 'r', encoding='utf8') as infile:
        data = json.load(infile)
        if data['action'] == 'report' and data['success']:
            session['results'] = data['results']
            session['query'] = False