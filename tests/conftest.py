import pytest
from Pi_Car.app import create_app


@pytest.fixture(scope="session", autouse=True)
def build_testing_app():
    """
    Builds a testing app with basic application context
    """
    app = create_app(config_file="config/test_config.py")
    app.app_context().push()

    yield app
