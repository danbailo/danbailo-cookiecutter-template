import logging

from common.env_var import get_env_var

logger_level = get_env_var('LOGGER_LEVEL')
logger_level = logger_level.upper() if logger_level else 'DEBUG'

MAPPED_LOGGER_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'WARN': logging.WARN,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}

logging.basicConfig(
    format=(
        '%(asctime)s - %(threadName)s - %(levelname)s - '
        '%(filename)s:%(funcName)s:%(lineno)d - %(message)s'
    )
)

logger = logging.getLogger(__name__)
logger.setLevel(MAPPED_LOGGER_LEVEL.get(logger_level))
