import base64
import os
import string
import random

import cv2
import numpy as np
from flask import current_app, request, Blueprint, abort

from api.TextDemo import MTS

img_blueprint = Blueprint("img_blueprint", __name__)

@img_blueprint.route("/api/upload", methods=["POST"])
def upload():
    image_blob = request.files.get("picture", "").read()
    npimg = np.fromstring(image_blob, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    try:
        result_polygons, result_words = MTS.get().run_on_opencv_image(img)
        MTS.get().visualization(img, result_polygons, result_words)

        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.png'

        path = os.path.join(current_app.instance_path, filename)
        cv2.imwrite(path, img)
        res = {"status": 200, "words": result_words, "img": filename}
        return res
    except TypeError:
        return {"status": 400, "error": "No predictions"}

@img_blueprint.route("/api/download/<filename>", methods=["GET"])
def download(filename):

    path = os.path.join(current_app.instance_path, filename)

    def generate():
        with open(path, 'rb') as f:
            yield from f
        os.remove(path)

    try:
        r = current_app.response_class(generate(), mimetype='image/png')
        r.headers.set('Content-Disposition', 'attachment', filename='result.png')
    except FileNotFoundError:
        abort(404)
    return r
