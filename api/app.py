import base64 
import os

import cv2
import string
import random

from flask import Flask, jsonify, request, render_template, send_file
import numpy as np
from werkzeug.middleware.proxy_fix import ProxyFix

from api.TextDemo import MTS


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
    MTS()

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

        
        try:

            result_polygons, result_words = MTS.get().run_on_opencv_image(img)
            MTS.get().visualization(img, result_polygons, result_words)

            filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.png'


            path = os.path.join(app.instance_path, filename)

            cv2.imwrite(path, img)

            def generate():
                with open(path) as f:
                    yield from f
                os.remove(path)


            import pdb
            pdb.set_trace()

            return 

        except TypeError:
            return jsonify("No predictions")

    @app.route("/api/download", methods["GET"])
    def download():


    return app
