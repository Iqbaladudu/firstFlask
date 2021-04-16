from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask.globals import request, session
from flask.helpers import make_response
from flask.signals import template_rendered
from werkzeug.exceptions import abort
from werkzeug.utils import unescape, secure_filename
import os

app = Flask(__name__)
app.secret_key = 'iqbal'
ALLOWED_EXTENSION = set(['png', 'jpg', '3gp', 'mp4', 'jpeg'])


@app.route('/')
def index():
    search = request.args.get('search')
    return render_template('index.html', search=search)

@app.route('/profil/<username>')
def profil(username):
    return render_template('profile.html', username=username)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == '':
            abort(401)
        resp = make_response(render_template('data.html', email=request.form['email'], password=request.form['password']))
        resp.set_cookie('user_pw', request.form['password'], 'email_user', request.form['email'])
        session['email'] = request.form['email']
        flash("Kamu berhasil login", 'Succes!')
        return resp
    if 'email' in session:
        email = session['email']
        return redirect(url_for('profil', username=email))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/cookie')
def getCookie():
    email = request.cookies.get('email_user')
    password = request.cookies.get('user_pw')
    return render_template('cookies.html', email=email, password=password)

@app.errorhandler(401)
def notFound(e):
    return render_template('401.html'), 401

# upload
app.config['UPLOAD_FOLDER'] = 'uploads'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files:
            return redirect(request.url)
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename =   secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File berhasil disimpan di ' + filename
    return render_template('upload.html')