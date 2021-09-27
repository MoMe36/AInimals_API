import os
import requests
import json
import numpy as np
from matplotlib import pyplot as plt
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from model import AInimalsModel
from PIL import Image

#Dossier d'upload des fichiers sons (les fichiers sont normalement supprimés après analyse)
UPLOAD_FOLDER = './uploads'
#Liste des extensions autorisées à l'upload
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
#Configuration
#Nécessaire pour le fonctionnement des alertes "flash"
app.config['SESSION_TYPE'] = 'filesystem'
app.config.update(SECRET_KEY=os.urandom(24))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Création du dossier upload si celui-ci n'existe pas
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print("Le dossier uploads n'existait pas et a été créé")

#Fonction prennant un nom d'oiseau en entrée et renvoyant un lien vers une image de cette oiseau
#Utilise google image search et nécessite une clé d'API Google et un numéro de CX (custom search engine)
#Entrer la clé d'API et le numéro CX dans le fichier request.json
def bird_finder(birdname):
    #Render du fichier de requète JSON en remplaçant la variable contenant le nom d'oiseau
    request_json=render_template('request.json', birdname=birdname)
    #Chargement du JSON
    json_params=json.loads(request_json)
    #Envoi de la requête GET avec les paramètres obtenus à partir du JSON
    response=requests.get("https://www.googleapis.com/customsearch/v1", params=json_params)
    #Chargement du JSON de réponse
    bird_found_json=response.json()
    #Chemin vers la variable "link" en réponse
    birdlink=bird_found_json['items'][0]['link']
    return(birdlink)

#Fonction de vérification de l'extension d'un fichier
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Racine
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #Uniquement executé si requête POST
    if request.method == 'POST':
        #Lecture des variables de configuration du formulaire HTML
        winSize=request.form['winSizeInput']
        winStart=request.form['StartPos']
        #Erreur si le fichier n'est pas upload correctement
        if 'file' not in request.files:
            flash('Erreur: Fichier absent dans la requête POST')
            return redirect(request.url)
        file = request.files['file']
        #Si l'utilisateur ne séléctionne pas un fichier, le navigateur envoie un fichier vide sans nom
        if file.filename == '':
            flash('Erreur: Pas de fichier sélectionné')
            return redirect(request.url)
        #Si l'extension est autorisée
        if file and allowed_file(file.filename):
            #Nettoyage du nom de fichier
            filename = secure_filename(file.filename)
            #Ecriture du fichier dans le dossier d'upload
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Renvoi une URL vers la fonction analyse_file() avec les paramètres de configuration
            return redirect(url_for('analyse_file', songfile=filename, windowSize=winSize, windowStart=winStart))
        else:
            #Erreur si l'extension du fichier est incorrecte
            flash('Erreur: Type de fichier incorrect')
            #Retour à la racine
            return redirect(request.url)
    #Retourne la page home.html si requête GET
    return render_template('home.html')
    
#Page de résultats
@app.route('/uploads/<songfile>/<windowSize>/<windowStart>')
def analyse_file(songfile,windowSize,windowStart):
    #Chargement du modèle
    m = AInimalsModel()
    #Stockage des résultats de prédictions
    results=m.get_preds('./uploads/'+songfile, int(float(windowStart)), windowSize)
    #Suppression du fichier après analyse et stockage des résultats
    os.remove('./uploads/'+songfile)
    #Transformation de l'array de pixels en image
    spectrogramme=Image.fromarray(results[2])
    #Sauvegarde de l'image
    spectrogramme.save('./static/'+songfile+'.png')
    #Rotation du spectrogramme:
    im=Image.open('./static/'+songfile+'.png')
    im=im.rotate(90, expand=True)
    #Sauvegarde du fichier après rotation
    im.save('./static/'+songfile+'.png')
    #Construction d'un histogramme de la distribution
    histogramme=plt.hist(results[0])
    histogramme=plt.title("Histogramme")
    #Sauvegarde de l'image de l'histogramme
    plt.savefig('./static/histo'+songfile+'.png')
    #Construction de la page à partir du template results.html
    return render_template('results.html', songfile=songfile, windowSize=windowSize, windowStart=windowStart, pred_num=str(results[1]), preds=str(results[0]), histo='/static/histo'+songfile+'.png', spectro='/static/'+songfile+'.png', birdlink=bird_finder('meme'))


if __name__ == '__main__':
    
    app.run()