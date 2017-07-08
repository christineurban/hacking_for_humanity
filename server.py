from flask import (Flask, render_template, redirect, request, 
                   flash, session, jsonify, g)

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

import os           # Access OS environment variables

# raise an error if variable is undefined
app.jinja_env.undefined = StrictUndefined

################################################################################
# Pages

@app.route("/")
def splash():
    """Splash page."""

    return render_template("index.html")