import sys
import os

#Help it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from routes.api import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
