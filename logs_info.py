import logging
import os

FORMAT = "%(asctime)s - %(levelname)s - %(filename)s: %(lineno)d - %(message)s"

if not os.path.exists('./logs'):
    os.makedirs('./logs')

logger = logging.getLogger('python-logger')
formatter = logging.Formatter(FORMAT)
logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.TimedRotatingFileHandler("./logs/logs.log", when="midnight")
file_handler.suffix = "%Y-%m-%d_%H-%M-%S"
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

