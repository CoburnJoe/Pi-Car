import logging

from flask import Flask
from logging.handlers import RotatingFileHandler
from .data import data_blueprint


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

    return app
