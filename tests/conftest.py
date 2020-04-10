import pytest

from Pi_Car.app import create_app


@pytest.fixture(scope="session", autouse=True)
def test_app():
    """
    Builds a Flask app and configures it for unit tests
    :return: Configured Flask app
    """
    test_app = create_app()
    test_app.app_context().push()

    yield test_app
