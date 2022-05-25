"""
app.py

Main program for BLEU score calculator

TODO: Checkbox to select whitespace/non-whitespace language
TODO: Clear files on future visits
TODO: Link to

"""

from flask import Flask, render_template, request, redirect, url_for
from flask_dropzone import Dropzone
from bleu.bleu_score import (
    get_min_max_sents,
    get_corpus_bleu_scores,
    get_refs_and_hyps
)
import os

filename = ''

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

app = Flask(__name__)
app.config.update(
    UPLOADED_PATH= os.path.join(basedir,'uploads'))

dropzone = Dropzone(app)

import pandas as pd


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
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            global filename
            filename = f.filename
            print(filename)
    return redirect(url_for('result'))


# ====================
@app.route('/result')
def result():
    fname, fext = os.path.splitext(filename)
    if fext == '.xlsx':
        df = pd.read_excel(os.path.join(app.config['UPLOADED_PATH'], filename))
        refs_and_hyps = get_refs_and_hyps(df)
        scores = get_corpus_bleu_scores(refs_and_hyps)
        min_max_sents = get_min_max_sents(refs_and_hyps)
        best = min_max_sents['max']
        worst = min_max_sents['min']
    return render_template('result.html', scores=scores, best=best, worst=worst)


# ====================
if __name__ == "__main__":

    app.run(debug=True)
