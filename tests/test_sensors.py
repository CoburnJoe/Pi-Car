from unittest.mock import patch
from Pi_Car.sensors import Sensors
from gpiozero import exc


class TestSensors:
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
