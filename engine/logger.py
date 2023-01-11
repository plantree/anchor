import logging
import logging.handlers

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() %(lineno)s - %(message)s"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
log = logging.getLogger(__name__)