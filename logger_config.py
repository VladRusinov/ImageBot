import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
BOT_PATH = os.path.abspath(__file__)
CATALOG_NAME = os.path.dirname(BOT_PATH) + r'\logs.log'
file_handler = logging.FileHandler(filename=CATALOG_NAME)
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s - %(lineno)d - '
    '%(funcName)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
