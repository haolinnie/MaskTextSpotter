from flask import Flask, jsonify, request, render_template, send_file
from werkzeug.middleware.proxy_fix import ProxyFix

from api.img_endpoints import img_blueprint
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

    # Instantiate MaskTextSpotter model
    MTS()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api")
    def index_api():
        return jsonify("MaskTextSpotter API")

    app.register_blueprint(img_blueprint)

    return app
