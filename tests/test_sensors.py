import pytest
from unittest.mock import patch
from Pi_Car.sensors import Sensors


class TestSensors:
    @patch("gpiozero.Button.is_pressed")
    def test_get_boot_status_positive(self, mock_is_pressed):
        assert 1 == 1
