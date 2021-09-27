import os
import requests
import json
import numpy as np
from matplotlib import pyplot as plt
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from model import AInimalsModel
from PIL import Image

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config.update(SECRET_KEY=os.urandom(24))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print("Le dossier uploads n'existait pas et a été créé")

def bird_finder(birdname):
    request_json=render_template('request.json', birdname=birdname)
    json_params=json.loads(request_json)
    response=requests.get("https://www.googleapis.com/customsearch/v1", params=json_params)
    bird_found_json=response.json()
    birdlink=bird_found_json['items'][0]['link']
    return(birdlink)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #Set vars from form
        winSize=request.form['winSizeInput']
        winStart=request.form['StartPos']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Erreur: Fichier absent dans la requête POST')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Erreur: Pas de fichier sélectionné')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('analyse_file', songfile=filename, windowSize=winSize, windowStart=winStart))
        else:
            flash('Erreur: Type de fichier incorrect')
            return redirect(request.url)
    return render_template('home.html')
    

@app.route('/uploads/<songfile>/<windowSize>/<windowStart>')
def analyse_file(songfile,windowSize,windowStart):
    m = AInimalsModel()
    results=m.get_preds('./uploads/'+songfile, int(float(windowStart)), windowSize)
    os.remove('./uploads/'+songfile)
    spectrogramme=Image.fromarray(results[2])
    spectrogramme.save('./static/'+songfile+'.png')
    #Rotation du spectrogramme:
    im=Image.open('./static/'+songfile+'.png')
    im=im.rotate(90, expand=True)
    im.save('./static/'+songfile+'.png')
    histogramme=plt.hist(results[0])
    histogramme=plt.title("Histogramme")
    plt.savefig('./static/histo'+songfile+'.png')
    return render_template('results.html', songfile=songfile, windowSize=windowSize, windowStart=windowStart, pred_num=str(results[1]), preds=str(results[0]), histo='/static/histo'+songfile+'.png', spectro='/static/'+songfile+'.png', birdlink=bird_finder('meme'))


if __name__ == '__main__':
    
    app.run()