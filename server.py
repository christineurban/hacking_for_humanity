from flask import (Flask, render_template, redirect, request, 
                   flash, session, jsonify, g)

from jinja2 import StrictUndefined

import line to: from /usr/local/lib/python2.7/dist-packages/watson_developer_cloud 
import VisualRecognitionV3 as VisualRecognition

watson_key = os.environ["WATSON_SECRET_KEY"]

visual_recognition = VisualRecognition(api_key=watson_key)

import os           # Access OS environment variables

app = Flask(__name__)

# raise an error if variable is undefined
app.jinja_env.undefined = StrictUndefined

################################################################################
# Pages

@app.route("/")
def index():
    """Home page."""

    # return render_template("index.html")
    return "hi"


@app.route("/check_tattoo")
def check():
    """Checks tattoo against known tattoos."""

    return render_template("check_tattoo.html")


@app.route("/known_tattoo")
def known():
    """Uploads known tattoo and keywords to DB."""

    return render_template("known_tattoo.html")



################################################################################

if __name__ == "__main__":
    
    # app.debug = True # for DebugToolbarExtension
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    app.run(port=5000, host='0.0.0.0')