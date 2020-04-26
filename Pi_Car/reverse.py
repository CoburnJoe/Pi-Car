from flask import Blueprint, render_template
from flask import current_app as app
from .sensors import Sensors

reverse_blueprint = Blueprint("reverse", __name__)


@reverse_blueprint.route("/reverse/")
def reverse():
    app.logger.info("Starting to load reverse route")
    stream_port = app.config.get("STREAM_PORT", 8081)
    host = "pi-car"
    stream_url = f"http://{host}:{stream_port}"
    app.logger.debug(f"Camera streaming url: {stream_url}")
    app.logger.info("Finished loading reverse route")
    return render_template(template_name_or_list="reverse.html", base_url=stream_url)


@reverse_blueprint.route("/reverse/beep/")
def reverse_beep():
    app.logger.info("Starting to load reverse rear detection")
    sensors = Sensors()
    reverse_light = sensors.get_reverse_status()
    if reverse_light:
        return "Exit"

    rear_distance_item = sensors.get_rear_distance_sensor()
    if rear_distance_item:
        sensors.beep()
    app.logger.info("Finished loading reverse rear detection")

    return "Success"
