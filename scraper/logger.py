"""
Logger
    It configures the logging level and provides a logger instance that can 
    be used throughout the project to log messages, errors, and other info.
"""

# scraper/logger.py
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

log = logging.getLogger(__name__)
