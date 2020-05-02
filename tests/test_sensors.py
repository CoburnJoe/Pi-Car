import pytest

from unittest.mock import patch
from Pi_Car.sensors import Sensors
from gpiozero import exc


class TestSensors:
    @patch("Pi_Car.sensors.Buzzer")
    def test_beep_bad_pin_factory(self, mock_buzzer):
        mock_buzzer.side_effect = exc.BadPinFactory
        result = Sensors.beep()
        assert result is None

    @patch("Pi_Car.sensors.Buzzer")
    def test_beep_other_pin_error(self, mock_buzzer):
        mock_buzzer.side_effect = TypeError
        result = Sensors.beep()
        assert result is None

    @patch("Pi_Car.sensors.Button")
    def test_get_bool_pin_bad_pin_factory(self, mock_button):
        mock_button.side_effect = exc.BadPinFactory
        result = Sensors.get_bool_pin(pin=None)
        assert result is None

    @patch("Pi_Car.sensors.Button")
    def test_get_bool_pin_other_pin_error(self, mock_button):
        mock_button.side_effect = TypeError
        result = Sensors.get_bool_pin(pin=None)
        assert result is None

    @patch("Pi_Car.sensors.Button")
    def test_get_boot_status_bad_pin_factory(self, mock_button):
        mock_button.side_effect = exc.BadPinFactory
        result = Sensors.get_boot_status()
        assert result == "Unknown"

    @patch("Pi_Car.sensors.Button")
    def test_get_boot_status_other_pin_error(self, mock_button):
        mock_button.side_effect = TypeError
        result = Sensors.get_boot_status()
        assert result == "Unknown"

    @patch("Pi_Car.sensors.Button")
    def test_get_boot_status_closed(self, mock_button):
        mock_button.return_value = type("Button", (), {"is_pressed": True})
        result = Sensors.get_boot_status()
        assert result == "Closed"

    @patch("Pi_Car.sensors.Button")
    def test_get_boot_status_open(self, mock_button):
        mock_button.return_value = type("Button", (), {"is_pressed": False})
        result = Sensors.get_boot_status()
        assert result == "Open"

    @patch("Pi_Car.sensors.LightSensor")
    def test_get_light_status_bad_pin_factory(self, mock_light_sensor):
        mock_light_sensor.side_effect = exc.BadPinFactory
        result = Sensors.get_light_status()
        assert result == "Unknown"

    @patch("Pi_Car.sensors.LightSensor")
    def test_get_light_status_other_pin_error(self, mock_light_sensor):
        mock_light_sensor.side_effect = TypeError
        result = Sensors.get_light_status()
        assert result == "Unknown"

    @pytest.mark.parametrize(
        "sensor_value, expected_result",
        [
            (1, "Daytime"),
            (0.9, "Daytime"),
            (0.5, "Daytime"),
            (0.55, "Daytime"),
            (0.49, "Nighttime"),
            (0.4, "Nighttime"),
            (0, "Nighttime"),
            (None, "Unknown"),
        ],
    )
    @patch("Pi_Car.sensors.LightSensor")
    def test_get_light_status_values(
        self, mock_light_sensor, sensor_value, expected_result
    ):
        mock_light_sensor.return_value = type("Button", (), {"value": sensor_value})
        result = Sensors.get_light_status()
        assert result == expected_result
