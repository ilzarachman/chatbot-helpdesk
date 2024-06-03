import logging
import logging.config
from logging.handlers import RotatingFileHandler
import sys
import os
import json


class CustomFormatter(logging.Formatter):
    grey = "\033[90m"
    yellow = "\033[93m"
    red = "\033[91m"
    bold_red = "\033[1;91m"
    reset = "\033[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomJSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for logging.
    """

    def __init__(self, fmt=None, datefmt=None, style="%"):
        """
        Initialize the formatter.
        """
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        """
        Format the record as JSON.
        """
        # Create a dictionary with the log record attributes
        log_dict = {
            "ts": self.formatTime(record, self.datefmt),
            "lvl": record.levelname,
            "file": record.filename,
            "line": record.lineno,
            "msg": record.getMessage(),
            "func": record.funcName,
        }

        # Add any additional custom fields you need
        # log_dict["custom_field"] = "some_value"
        # Convert the dictionary to JSON
        return json.dumps(log_dict)


def configure_logging():

    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "custom": {"()": CustomFormatter},
                "default": {
                    "()": logging.Formatter,
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
                },
                "json": {
                    "()": CustomJSONFormatter,
                },
            },
            "filters": {
                "only_info_and_error": {
                    "(record)": lambda record: record.levelname == "INFO"
                    or record.levelno >= 40,
                },
            },
            "handlers": {
                "root_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(log_folder, "root.log.jsonl"),
                    "maxBytes": 1e6,
                    "backupCount": 3,
                    "formatter": "json",
                    "encoding": "utf-8",
                },
                "app_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(log_folder, "app.log.jsonl"),
                    "maxBytes": 1e6,
                    "backupCount": 2,
                    "formatter": "json",
                    "encoding": "utf-8",
                },
                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(log_folder, "error.log.jsonl"),
                    "maxBytes": 1e6,
                    "backupCount": 2,
                    "formatter": "json",
                    "encoding": "utf-8",
                    "level": "ERROR",
                },
                "app_stream": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "custom",
                    "level": "INFO",
                    "filters": ["only_info_and_error"],
                },
            },
            "loggers": {
                "": {"handlers": ["root_file", "error_file"], "level": "NOTSET"},
                "app": {
                    "handlers": ["app_file", "app_stream", "error_file"],
                    "level": "DEBUG",
                },
            },
        }
    )


"""
The logger object for the application.

Use this object to log messages to the console and files.

Example usage:
```python
logger.info("Starting the application")
logger.error("An error occurred while processing the request")
```
"""
logger: logging.Logger = logging.getLogger("app")
