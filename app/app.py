"""
app.py

Main program for BLEU score calculator

TODO: Checkbox to select whitespace/non-whitespace language
TODO: Clear files on future visits
"""

import os

import pandas as pd
import redis
from flask import (Flask, json, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_dropzone import Dropzone
from flask_session import Session

from bleu.bleu_score import (get_corpus_bleu_scores, get_min_max_sents,
                             get_refs_and_hyps)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure redis and secret key
is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')
    redis_password = os.environ.get('REDIS_PASSWORD')
    session_redis = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
    secret_key = os.environ.get('SECRET_KEY')
else:
    # Local environment
    redis_url = 'redis://localhost:6379'
    session_redis = redis.from_url(redis_url)
    secret_key = 'bananas'

# Configure app
app = Flask(__name__)
app.config.update(
    SECRET_KEY=secret_key,
    UPLOAD_FOLDER=os.path.join(basedir, 'uploads'),
    SESSION_TYPE='redis',
    SESSION_PERMANENT=False,
    SESSION_USE_SIGNER=True,
    SESSION_REDIS=session_redis
)
server_session = Session(app)

dropzone = Dropzone(app)


# ====================
@app.route('/')
def index():
    # render upload page
    return render_template('index.html')


# ====================
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            print('uploading')
            session['fname'] = f.filename
            fpath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            session['fpath'] = fpath
            f.save(fpath)
    return redirect(url_for('result'))


# ====================
@app.route('/result')
def result():
    fpath = session['fpath']
    _, fname_ext = os.path.splitext(session['fname'])
    if fname_ext == '.xlsx':
        df = pd.read_excel(fpath)
        refs_and_hyps = get_refs_and_hyps(df)
        scores = get_corpus_bleu_scores(refs_and_hyps)
        min_max = get_min_max_sents(refs_and_hyps)
    return render_template('result.html', scores=scores, min_max=min_max)


# ====================
if __name__ == "__main__":

    app.run(debug=True)
