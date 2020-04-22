import logging

from flask import Flask, render_template, Response
from logging.handlers import RotatingFileHandler
from .data import data_blueprint

try:
    from picamera import PiCamera
except ImportError:
    PiCamera = None


import socket
import io


def create_app(config_file="config/local_config.py"):
    app = Flask(__name__)  # Initialize app
    app.config.from_pyfile(config_file, silent=False)  # Read in config from file

    if app.config.get("FILE_LOGGING"):
        # Configure file based log handler
        log_file_handler = RotatingFileHandler(
            filename=app.config.get("LOG_FILE_NAME", "config/pi-car.log"),
            maxBytes=10000000,
            backupCount=4,
        )
        log_file_handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(log_file_handler)

    app.logger.setLevel(app.config.get("LOGGER_LEVEL", "ERROR"))

    app.logger.info("----- STARTING APP ------")
    app.register_blueprint(data_blueprint)
    app.logger.info("----- FINISHED STARTING APP -----")

    if PiCamera:
        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
    else:
        camera = None

    @app.route("/camera/")
    def index():
        """Video streaming ."""
        return render_template("camera.html")

    def gen():
        """Video streaming generator function."""
        while True:
            camera.capture("pic.jpg")
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + open("pic.jpg", "rb").read()
                + b"\r\n"
            )

    @app.route("/video_feed")
    def video_feed():
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

    return app
