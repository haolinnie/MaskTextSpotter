from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from api.TextDemo import MTS


def create_app():

    # Instantiate
    app = Flask("MaskTextSpotterAPI", instance_relative_config=True)

    # Add cors
    CORS(app)

    # proxy support
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Instantiate MaskTextSpotter
    MTS()

    @app.route("/")
    def index():
        return jsonify("hello world from Mask Textspotter")

    @app.route("/api")
    def index_api():
        return jsonify("MaskTextSpotter API")

    @app.route("/api/upload", methods=["POST"])
    def upload():
        imagefile = request.files.get('imagefile', '')
        breakpoint()

        return "/api/upload POST request received"

    return app
