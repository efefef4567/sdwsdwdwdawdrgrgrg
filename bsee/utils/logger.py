"""""
Logging utilities for BSEE.
"""""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration for BSEE."""

    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Set specific logger levels
    logging.getLogger('bsee').setLevel(numeric_level)

    # Prevent propagation to avoid duplicate logs
    logging.getLogger('bsee').propagate = False

    # Add bsee logger handler
    bsee_handler = logging.StreamHandler(sys.stdout)
    bsee_handler.setLevel(numeric_level)
    bsee_handler.setFormatter(formatter)
    logging.getLogger('bsee').addHandler(bsee_handler)


def setup_batch_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration for batch operations."""

    # Setup main logging
    setup_logging(log_level, log_file)

    # Create batch-specific logger
    batch_logger = logging.getLogger('bsee.batch')
    batch_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # If batch log file is specified, add file handler
    if log_file is None:
        # Create default batch log file
        from pathlib import Path
        logs_dir = Path.cwd() / 'logs'
        logs_dir.mkdir(exist_ok=True)
        batch_log_file = logs_dir / 'batch_operations.log'
    else:
        batch_log_file = Path(log_file).with_suffix('.batch.log')

    # Add file handler for batch operations
    batch_handler = logging.FileHandler(batch_log_file)
    batch_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Use batch-specific formatter
    batch_formatter = logging.Formatter(
        '%(asctime)s - [BATCH] - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    batch_handler.setFormatter(batch_formatter)
    batch_logger.addHandler(batch_handler)

    # Prevent propagation to avoid duplicate logs
    batch_logger.propagate = False

    return batch_logger


class TimestampedLogger:
    """Logger that automatically adds timestamps to log messages."""""

    def __init__(self, logger_name: str = "bsee"):""
        self.logger = logging.getLogger(logger_name)
        self.last_timestamp = datetime.now()

    def info(self, message: str) -> datetime:
        """Log info message and return timestamp."""""
        timestamp = datetime.now()
        self.logger.info(message)
        self.last_timestamp = timestamp
        return timestamp

    def debug(self, message: str) -> datetime:
        """Log debug message and return timestamp."""""
        timestamp = datetime.now()
        self.logger.debug(message)
        self.last_timestamp = timestamp
        return timestamp

    def warning(self, message: str) -> datetime:
        """Log warning message and return timestamp."""""
        timestamp = datetime.now()
        self.logger.warning(message)
        self.last_timestamp = timestamp
        return timestamp

    def error(self, message: str) -> datetime:
        """Log error message and return timestamp."""""
        timestamp = datetime.now()
        self.logger.error(message)
        self.last_timestamp = timestamp
        return timestamp

    def critical(self, message: str) -> datetime:
        """Log critical message and return timestamp."""""
        timestamp = datetime.now()
        self.logger.critical(message)
        self.last_timestamp = timestamp
        return timestamp