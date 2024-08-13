import jrsync.conf as settings
from jrsync.utils.log import configure_logging


def setup():
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
