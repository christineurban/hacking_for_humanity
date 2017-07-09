from flask import (Flask, render_template, redirect, request, 
                   flash, session, jsonify, g, url_for)

from jinja2 import StrictUndefined

import os           # Access OS environment variables
from werkzeug.utils import secure_filename
import json
from os.path import join, dirname

from twilio.rest import Client

#Needed for Watson
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

watson_key = os.environ["WATSON_SECRET_KEY"]

# from watson_developer_cloud import VisualRecognitionV3
# visual_recognition = VisualRecognitionV3('2016-05-20', api_key=watson_key)

app = Flask(__name__)

# For uploading images
UNKNOWN_TATTOOS = 'static/images/unknown_tattoos'
USER_KNOWN_TATTOOS = 'static/images/user_known_tattoos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UNKNOWN_TATTOOS'] = UNKNOWN_TATTOOS
app.config['USER_KNOWN_TATTOOS'] = USER_KNOWN_TATTOOS

# raise an error if variable is undefined
app.jinja_env.undefined = StrictUndefined

################################################################################
# Pages

@app.route("/")
def index():
    """Home page."""

    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process-form', methods=['POST'])
def upload_file():
    # Get tattoo status (known or unknown)
    tattoo_status = request.form.get("known-unknown")
    if tattoo_status == 'known':
        # Update tattoo database with image
        if request.method == 'POST':
            # check if the post request has the file part
            if 'image' not in request.files:
                print request.files
                print "doesn't have file"
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                print "no selected file"
            if file and allowed_file(file.filename):
                print "file type allowed"
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['USER_KNOWN_TATTOOS'], filename))
            return render_template("known.html")

    # Unknown tattoo status
    else:
        # Check tattoo for similarity
        if request.method == 'POST':
            # check if the post request has the file part
            if 'image' not in request.files:
                print request.files
                print "doesn't have file"
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                print "no selected file"
            if file and allowed_file(file.filename):
                print "file type allowed"
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UNKNOWN_TATTOOS'], filename))

            similarity = check_tattoo(filename)
            return render_template("unknown.html", 
                                    similarity=similarity)


@app.route("/send-text", methods=["POST"])
def send_text_message():
    """Send a text message using the Twilio API to number provided by user."""
    
    phone_number = request.form.get("phone-number")    
    account_sid = os.environ["ACCOUNT_SID"]
    auth_token = os.environ["AUTH_TOKEN"]    

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phone_number,
        from_="+19073121980",
        body="""If you need help, call 1-888-373-7888.""")

    print(message.sid)

    return "Your message has been sent."


def train_classifier():

    visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key=watson_key)

    with open(join(dirname(__file__), 'barcode_trainers.zip'), 'rb') as barcodes, \
        open(join(dirname(__file__), 'crown_trainers.zip'), 'rb') as crowns :
        print "Uploading files..."
        print(json.dumps(visual_recognition.create_classifier('Tattoos', \
            barcode_positive_examples=barcodes, \
            crowns_positive_examples=crowns), indent=2))

def get_trainer_status():
    visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key=watson_key)

    print(json.dumps(visual_recognition.get_classifier('Tattoos_502109298'), indent=2))
# train_classifier()

def check_tattoo(filename):
    """Checks image for similarity and renders appropriate advice."""
    # Mocked out due to time constraint

    # # Match for known trafficking tattoo
    # if filename == 'barcode6.jpeg':
    #     similarity = .70
    #     return {"similarity": similarity, "strength": "strong"}
    # # TODO find image for non-match
    # if filename == '':
    #     similarity = .06
    #     return {"similarity": similarity, "strength": "low"}

    # # TODO find image for kinda similar
    # if filename == '':
    #     similarity = .40
    #     return {"similarity": similarity, "strength": "medium"}

    visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key=watson_key)

    with open(join(dirname(__file__), filename), 'rb') as image_file:
        response = json.dumps(visual_recognition.classify(images_file=image_file, threshold=0, classifier_ids=['Tattoos_502109298']), indent=2)

        similarity = json.loads(response)

        print "********************************", similarity, "*************************"

        barcode_score = similarity['images'][0]['classifiers'][0]["classes"][0]['score']
        print barcode_score
        crown_score = similarity['images'][0]['classifiers'][0]["classes"][1]['score']
        print crown_score

        if barcode_score or crown_score >= .7:
            return {"score": barcode_score, "strength": "strong"}
        elif barcode_score or crown_score >= .3:
            return {"score": barcode_score, "strength": "medium"}
        elif barcode_score or crown_score >= .0:
            return {"score": barcode_score, "strength": "low"}





################################################################################

if __name__ == "__main__":
    
    app.debug = True # for DebugToolbarExtension
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    app.run(port=5000, host='0.0.0.0')