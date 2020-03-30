# LOCAL DEVELOPMENT CONFIG FILE
# More config options: https://flask.palletsprojects.com/en/1.1.x/config/

# Flask specific values
ENV = "development"
DEBUG = True
TESTING = True
APPLICATION_ROOT = "/"
PREFERRED_URL_SCHEME = "http"

# Custom values
# Possible logging levels:
# CRITICAL - FATAL - ERROR - WARNING - INFO - DEBUG - NOTSET
LOGGER_LEVEL = "DEBUG"
LOG_FILE_NAME = "pi-car.log"
