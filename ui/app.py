from flask import Flask, render_template, url_for, request, session
import os

app = Flask(__name__)
app.secret_key = str(os.urandom(24))
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')


@app.route('/', methods=['GET','POST'])
def layout():
    session['username'] = 'andy'
    if request.method == 'POST':
        if 'path' in session:
            if not request.form['path'] == session['path']:
                return render_template('about.html')
        else:
            session['path'] = request.form['path']
    return render_template('layout.html')

@app.route('/about')
def about():
    return render_template('about.html')