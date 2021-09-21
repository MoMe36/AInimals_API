import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('analyse_file', name=filename))
    return '''
    <!doctype html>
    <title>Chant à analyser:</title>
    <h1>Envoyer un fichier son:</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload><br />
      <label for="winSizeInput">Taille de la fenêtre glissante (entre 1 and 10):</label>
      <input type="number" name="winSizeInput" min="1" max="10" value="5" oninput="this.form.winSizeRange.value=this.value" />
      <input type="range" name="winSizeRange" min="1" max="10" value="5" oninput="this.form.winSizeInput.value=this.value" /><br />
      <label for="StartPos">Position de départ de la fenêtre:</label>
      <input type="number" name="StartPos" min="0.0" max="300.0" value="0.0" step="0.1" />
    </form>
    '''

@app.route('/uploads/<name>')
def analyse_file(name):
    return 'Résultats: <name>'

if __name__ == '__main__':
    app.run()