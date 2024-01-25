"""
This module sets up a logging system for the application. It includes configuration for logging to a file
and the console with different formats. The console output is colored based on the log level to enhance visibility.
"""

import logging
import os

COLORS = {
    "WARNING": "\033[93m",
    "INFO": "\033[94m",
    "DEBUG": "\033[92m",
    "CRITICAL": "\033[91m",
    "ERROR": "\033[91m",
    "ENDC": "\033[0m",
}


class ColoredFormatter(logging.Formatter):
    """
    This custom formatter colors the log messages based on their severity level.
    It extends the logging.Formatter class and overrides the format method to add color codes.
    """

    def format(self, record):
        log_message = super().format(record)
        return f"{COLORS.get(record.levelname, COLORS['ENDC'])}{log_message}{COLORS['ENDC']}"


LOG_FILE_PATH = "logs/philipsLightsLogs.log"

if not os.path.exists("logs"):
    os.mkdir("logs")

if not os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, "w", encoding="utf-8"):
        print(f"Log file created at {LOG_FILE_PATH}")

file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

console_handler = logging.StreamHandler()
console_formatter = ColoredFormatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
