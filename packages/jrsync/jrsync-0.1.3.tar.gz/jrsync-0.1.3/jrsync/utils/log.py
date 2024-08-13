import logging.config

import jrsync.conf as settings
from jrsync.utils.module_loading import import_string

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "jrsync.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "jrsync.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "my_fmt": {
            "format": "[%(asctime)s] - %(levelname)s: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
            "formatter": "my_fmt",
        },
        "console_with_debug": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "my_fmt",
        },
    },
    "loggers": {
        "jrsync": {
            "handlers": ["console", "console_with_debug"],
            "level": "DEBUG",
        },
    },
}


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG


def configure_logging(logging_config, logging_settings):
    if logging_config:
        # First find the logging configuration function ...
        logging_config_func = import_string(logging_config)

        logging.config.dictConfig(DEFAULT_LOGGING)

        # ... then invoke it with the logging settings
        if logging_settings:
            logging_config_func(logging_settings)
