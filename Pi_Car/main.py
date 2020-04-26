from flask import Blueprint, render_template
from .sensors import Sensors
from flask import current_app as app
from datetime import datetime

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def show():
    app.logger.info("Starting to retrieve core data")
    sensors = Sensors()

    temperature = sensors.get_external_temp()
    boot_status = sensors.get_boot_status()
    light_status = sensors.get_light_status()
    reverse_light = sensors.get_reverse_status()
    fog_light = sensors.get_fog_light_status()

    today = datetime.now()
    time = today.strftime("%H:%M")
    date = today.strftime("%A %d %B %Y")

    result = {
        "temperature": temperature,
        "boot": boot_status,
        "light": light_status,
        "reverse": reverse_light,
        "fog": fog_light,
        "time": time,
        "date": date,
    }

    app.logger.info("Finished retrieving core data")
    app.logger.debug(f"Core data: {result}")
    return render_template("main.html", data=result)
