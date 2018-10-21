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
    if 'user' in session:
        return redirect(url_for('index'))
    session['user'] = 'andy'    
    return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if os.path.exists(request.form['path']):
            if session['build'] == True:
                flash('Model is already constructed, touch again for rebuilding in a diferent path', 'message')
                session['build'] = False
            else:
                session['build'] = True
                session['path'] = request.form['path']
                flash('Path is valid, model is being constructed', 'message')
                build()
        else:
            flash('Path is Wrong, no new model for construction', 'Error')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/json/build')
def build():
    result = {"action" : "build",
                "path" : session['path']}
    with io.open(os.path.curdir + url_for('static', filename='json/build.json'), 'w', encoding='utf8') as outfile:
        text = json.dumps(result,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
        outfile.write(text)
    return redirect(url_for('static', filename='json/build.json'))