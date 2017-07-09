from flask import (Flask, render_template, redirect, request, 
                   flash, session, jsonify, g, url_for)

from jinja2 import StrictUndefined

import os           # Access OS environment variables
from werkzeug.utils import secure_filename
import json
from os.path import join, dirname
# watson_key = os.environ["WATSON_SECRET_KEY"]

# from watson_developer_cloud import VisualRecognitionV3
# visual_recognition = VisualRecognitionV3('2016-05-20', api_key=watson_key)

app = Flask(__name__)

# raise an error if variable is undefined
app.jinja_env.undefined = StrictUndefined

# For uploading images
UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

################################################################################
# Pages

@app.route("/")
def index():
    """Home page."""

    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/check-tattoo', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            check_tattoo(filename)

    return filename



################################################################################

if __name__ == "__main__":
    
    # app.debug = True # for DebugToolbarExtension
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    app.run(port=5000, host='0.0.0.0')