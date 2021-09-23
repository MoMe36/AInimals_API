import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from model import AInimalsModel

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            return redirect(url_for('analyse_file', songfile=filename, windowSize=winSize, windowStart=winStart))
    return render_template('home.html')
    

@app.route('/uploads/<songfile>/<windowSize>/<windowStart>')
def analyse_file(songfile,windowSize,windowStart):
    m = AInimalsModel()
    results=m.get_preds('./uploads/'+songfile, int(float(windowStart)), windowSize)
    return render_template('results.html', songfile=songfile, windowSize=windowSize, windowStart=windowStart, pred_num=str(results[1]), preds=str(results[0]), spectro=str(results[2]))


if __name__ == '__main__':
    app.run()