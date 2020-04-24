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
    reverse_light = Sensors.get_reverse_status()
    fog_light = Sensors.get_fog_light_status()
    rear_distance = Sensors.get_rear_distance_sensor()

    result = {
        "temperature": temperature,
        "boot": boot_status,
        "light": light_status,
        "reverse": reverse_light,
        "rear_distance": rear_distance,
        "fog": fog_light,
    }

    Sensors.beep()
    app.logger.info("Finished retrieving core data")
    app.logger.debug(f"Core data: {result}")
    return jsonify(result)
