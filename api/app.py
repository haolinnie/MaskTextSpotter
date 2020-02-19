from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():

    # Instantiate
    app = Flask("MaskTextSpotterAPI", instance_relative_config=True)

    # Add cors
    CORS(app)

    # proxy support
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.route("/")
    def index():
        return jsonify("hello world!")

    return app
