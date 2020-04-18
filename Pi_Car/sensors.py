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
    def get_bool_pin(pin):
        """
        Defensively read boolean pin as a button
        :param pin: GPIO pin (in BCM layout) to read
        :return: Boolean result -- pressed on not, or none
        """
        app.logger.info(f"Starting to read boolean value from pin: {pin}")

        try:
            button = Button(pin=pin)
            result = button.is_pressed
        except exc.BadPinFactory as e:
            app.logger.warning(f"Unable to use boot sensor in this environment: {e}")
            result = None
        except Exception as e:
            app.logger.error(f"Unknown problem with boot sensor: {e}")
            result = None

        app.logger.info(f"Finished reading boolean value from pin: {pin}")
        return result

    @classmethod
    def get_reverse_status(cls):
        """
        Safely read the reversing sensor
        :return: Boolean - reversing or not, or None
        """
        app.logger.info("Starting to read reverse sensor")
        result = cls.get_bool_pin(pin=22)
        app.logger.debug(f"Boot: {result}")
        app.logger.info("Finished reading reverse sensor")
        return result

    @classmethod
    def get_fog_light_status(cls):
        """
        Safely read the fog light sensor
        :return: Boolean - fog lights on or not, or None
        """
        app.logger.info("Starting to read fog light sensor")
        result = cls.get_bool_pin(pin=23)
        app.logger.debug(f"Boot: {result}")
        app.logger.info("Finished reading fog light sensor")
        return result

    @classmethod
    def get_boot_status(cls):
        """
        Safely read the boot sensor and calculate the state - open/closed/unavailable/unknown
        :return: String - boot status
        """
        app.logger.info("Starting to read boot sensor")
        button_status = cls.get_bool_pin(pin=14)

        if button_status is None:
            result = "Unknown"
        else:
            if button_status:
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
        elif status >= 0.5:
            result = "Daytime"
        else:
            result = "Nighttime"

        app.logger.debug(f"Light: {status} - {result}")
        app.logger.info("Finished reading available light")

        return result
