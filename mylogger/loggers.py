import logging
from loguru import logger as loguru_logger

# may add to this later, as of now only accounting for local
def local_logger_catcher():
    return loguru_logger, loguru_logger.catch
