import logging
import os
from datetime import datetime
from typing import Optional


class TestLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initialize the logger with both file and console handlers"""
        self.logger = logging.getLogger('TestAutomation')
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory if it doesn't exist
        log_dir = 'reports'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create handlers
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_handler = logging.FileHandler(
            f'{log_dir}/test_execution_{timestamp}.log',
            encoding='utf-8'
        )
        console_handler = logging.StreamHandler()

        # Set levels
        file_handler.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s'
        )
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s'
        )

        file_handler.setFormatter(file_format)
        console_handler.setFormatter(console_format)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """Log info level message"""
        self.logger.info(message)

    def debug(self, message: str):
        """Log debug level message"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log warning level message"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: Optional[Exception] = None):
        """Log error level message with optional exception info"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: Optional[Exception] = None):
        """Log critical level message with optional exception info"""
        self.logger.critical(message, exc_info=exc_info)


# Create a singleton instance
logger = TestLogger()