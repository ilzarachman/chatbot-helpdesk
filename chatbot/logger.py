import logging
import logging.config
from logging.handlers import RotatingFileHandler
import sys

class CustomFormatter(logging.Formatter):
    grey = "\033[90m"
    yellow = "\033[93m"
    red = "\033[91m"
    bold_red = "\033[1;91m"
    reset = "\033[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def configure_logging():
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "custom": {
                "()": CustomFormatter
            },
            "default": {
                "()": logging.Formatter,
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
            }
        },
        "filters": {
            "only_info_and_error": {
                "(record)": lambda record: record.levelname == "INFO" or record.levelno >= 40,
            }
        },
        "handlers": {
            "root_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "root.log",
                "maxBytes": 1e6,
                "backupCount": 3,
                "formatter": "default",
                "encoding": "utf-8"
            },
            "app_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 1e6,
                "backupCount": 2,
                "formatter": "default",
                "encoding": "utf-8"
            },
            "app_stream": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "custom",
                "level": "INFO",
                "filters": ["only_info_and_error"]
            }
        },
        "loggers": {
            "": {
                "handlers": ["root_file"],
                "level": "NOTSET"
            },
            "app": {
                "handlers": ["app_file", "app_stream"],
                "level": "DEBUG"
            }
        }
    })

logger = logging.getLogger("app")