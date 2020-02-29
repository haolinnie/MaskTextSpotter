from flask import Flask, jsonify, request, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

import numpy as np
import cv2

# from api.TextDemo import MTS


def create_app():

    # Instantiate
    app = Flask(
        "MaskTextSpotterAPI",
        instance_relative_config=True,
        static_folder="api/frontend/static",
        template_folder="api/frontend",
    )

    # proxy support
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Instantiate MaskTextSpotter
    # MTS()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api")
    def index_api():
        return jsonify("MaskTextSpotter API")

    @app.route("/api/upload", methods=["POST"])
    def upload():
        image_blob = request.files.get("picture", "").read()
        npimg = np.fromstring(image_blob, np.uint8)

        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        import pdb

        pdb.set_trace()

        return "/api/upload POST request received"

    return app
