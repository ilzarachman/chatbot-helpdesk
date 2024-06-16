import logging
import logging.config
from logging.handlers import RotatingFileHandler
import sys
import os
import json


class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter that allows different colors for different log levels.
    """

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

    def __init__(self, fmt=None, datefmt=None, style="%"):
        """
        Initialize the formatter.
        """
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        """
        Format the record as a string.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
        """
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

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
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


class InfoAndErrorFilter(logging.Filter):
    """
    Filter for log records at the INFO and ERROR levels.
    """

    def filter(self, record):
        """
        Filter the log record if its level is not INFO or ERROR.

        Args:
            record (logging.LogRecord): The log record to filter.

        Returns:
            bool: True if the record should be logged; False otherwise.
        """
        return record.levelno in [logging.INFO, logging.ERROR]


def configure_logging():
    """
    Configures the logging settings for the application.

    This function sets up the logging configuration for the application. It creates a log folder named "logs" if it does not exist. The function then configures the logging settings using the `logging.config.dictConfig` method. The configuration includes the following components:

    - Formatters: Defines different log formatters for different logging levels.
    - Filters: Defines a filter to only log records at the INFO and ERROR levels.
    - Handlers: Defines different log handlers for different logging levels and destinations.
    - Loggers: Configures the loggers for different parts of the application.

    The loggers are configured as follows:

    - The root logger is configured to log records to the "root_file" handler and the "error_file" handler.
    - The "app" logger is configured to log records to the "app_file" handler, the "app_stream" handler, and the "error_file" handler.

    This function does not take any parameters.

    This function does not return any values.
    """
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
                "only_info_and_error": {"()": InfoAndErrorFilter},
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


logger: logging.Logger = logging.getLogger("app")
"""
The logger object for the application.

Use this object to log messages to the console and files.

Example usage:
```python
logger.info("Starting the application")
logger.error("An error occurred while processing the request")
```
"""
