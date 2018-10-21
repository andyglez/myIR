from flask import Flask, render_template, url_for, request, session, flash, redirect
import os

app = Flask(__name__)
app.secret_key = str(os.urandom(24))
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')


@app.route('/', methods=['GET','POST'])
def layout():
    if 'user' in session:
        return redirect(url_for('index'))
    session['user'] = 'andy'    
    return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if 'path' in session:
            if request.form['path'] == session['path']:
                if 'build' in session and session['build'] == True:
                    flash('Model is already constructed', 'warning')
                else:
                    session['build'] = False
            else:
                session['build'] = True
                session['path'] = request.form['path']
                if os.path.exists(session['path']):
                    flash('Ok it does exist', 'message')
                else:
                    flash('Path is wrong', 'error')
        else:
            session['path'] = request.form['path']
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')