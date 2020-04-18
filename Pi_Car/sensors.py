from flask import current_app as app
from gpiozero import Button, exc, LightSensor

try:
    from w1thermsensor import W1ThermSensor
except Exception:
    W1ThermSensor = None


class Sensors:
    @staticmethod
    def get_external_temp():
        """
        Safely read the external temperature
        :return: Integer of current temperature
        """
        app.logger.info("Starting to read temperature sensor")

        try:
            sensor = W1ThermSensor()
            temperature = sensor.get_temperature()
        except TypeError as e:
            app.logger.warning(
                f"Unable to use primary temperature sensor in this environment: {e}"
            )
            temperature = 0
        except Exception as e:
            app.logger.error(
                f"Unknown problem with primary external temperature sensor: {e}"
            )
            temperature = 0

        app.logger.info("Finished reading temperature sensor")
        app.logger.debug(f"Temperature: {temperature}")
        return int(temperature)

    @staticmethod
    def get_boot_status():
        """
        Safely read the boot sensor and calculate the state - open/closed/unavailable/unknown
        :return: String - boot status
        """
        app.logger.info("Starting to read boot sensor")
        result = None
        status = None

        try:
            button = Button(pin=14)
            status = button.is_pressed
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use boot sensor in this environment: {e}")
            result = "Unknown"
        except Exception as e:
            app.logger.error(f"Unknown problem with boot sensor: {e}")
            result = "Unknown"

        if not result:
            if status:
                result = "Closed"
            else:
                result = "Open"

        app.logger.debug(f"Boot: {result}")
        app.logger.info("Finished reading boot sensor")
        return result

    @staticmethod
    def get_light_status():
        """
        Safely read the available light and calculate a status - daytime/dusk/nighttime/unknown
        :return: String - light status
        """
        app.logger.info("Starting to read available light")
        status = -1

        try:
            sensor = LightSensor(pin=15)
            status = float(sensor.value)
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use light sensor in this environment: {e}")
        except Exception as e:
            app.logger.error(f"Unknown problem with light sensor: {e}")

        if status == -1:
            result = "Unknown"
        elif status >= 0.6:
            result = "Daytime"
        elif 0.6 > status > 0.2:
            result = "Dusk"
        else:
            result = "Nighttime"

        app.logger.debug(f"Light: {status}")
        app.logger.info("Finished reading available light")

        return result
