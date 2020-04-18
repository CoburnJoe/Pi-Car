from flask import Blueprint, jsonify
from .sensors import Sensors
from flask import current_app as app

data_blueprint = Blueprint("data", __name__)


@data_blueprint.route("/")
def show():
    app.logger.info("Starting to retrieve core data")
    temperature = Sensors.get_external_temp()
    boot_status = Sensors.get_boot_status()
    light_status = Sensors.get_light_status()

    result = {"temperature": temperature, "boot": boot_status, "light": light_status}

    app.logger.info("Finished retrieving core data")
    app.logger.debug(f"Core data: {result}")
    return jsonify(result)
