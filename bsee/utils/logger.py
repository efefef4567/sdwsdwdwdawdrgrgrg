"""""
# DISABLED: Logging utilities for BSEE.
"""""

# DISABLED: import logging
# DISABLED: import sys
# DISABLED: from datetime import datetime
# DISABLED: from pathlib import Path
# DISABLED: from typing import Optional


# DISABLED: def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration for BSEE."""

    # Convert string level to logging constant
# DISABLED:     numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatter
# DISABLED:     formatter = logging.Formatter(
# DISABLED:         '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# DISABLED:         datefmt='%Y-%m-%d %H:%M:%S'
# DISABLED:     )

    # Setup root logger
# DISABLED:     root_logger = logging.getLogger()
# DISABLED:     root_logger.setLevel(numeric_level)

    # Clear existing handlers
# DISABLED:     root_logger.handlers.clear()

    # Console handler
# DISABLED:     console_handler = logging.StreamHandler(sys.stdout)
# DISABLED:     console_handler.setLevel(numeric_level)
# DISABLED:     console_handler.setFormatter(formatter)
# DISABLED:     root_logger.addHandler(console_handler)

    # File handler (optional)
# DISABLED:     if log_file:
# DISABLED:         log_path = Path(log_file)
# DISABLED:         log_path.parent.mkdir(parents=True, exist_ok=True)

# DISABLED:         file_handler = logging.FileHandler(log_path)
# DISABLED:         file_handler.setLevel(numeric_level)
# DISABLED:         file_handler.setFormatter(formatter)
# DISABLED:         root_logger.addHandler(file_handler)

    # Set specific logger levels
# DISABLED:     logging.getLogger('bsee').setLevel(numeric_level)

    # Prevent propagation to avoid duplicate logs
# DISABLED:     logging.getLogger('bsee').propagate = False

    # Add bsee logger handler
# DISABLED:     bsee_handler = logging.StreamHandler(sys.stdout)
# DISABLED:     bsee_handler.setLevel(numeric_level)
# DISABLED:     bsee_handler.setFormatter(formatter)
# DISABLED:     logging.getLogger('bsee').addHandler(bsee_handler)


# DISABLED: def setup_batch_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration for batch operations."""

    # Setup main logging
# DISABLED:     setup_logging(log_level, log_file)

    # Create batch-specific logger
# DISABLED:     batch_logger = logging.getLogger('bsee.batch')
# DISABLED:     batch_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # If batch log file is specified, add file handler
# DISABLED:     if log_file is None:
        # Create default batch log file
# DISABLED:         from pathlib import Path
# DISABLED:         logs_dir = Path.cwd() / 'logs'
# DISABLED:         logs_dir.mkdir(exist_ok=True)
# DISABLED:         batch_log_file = logs_dir / 'batch_operations.log'
# DISABLED:     else:
# DISABLED:         batch_log_file = Path(log_file).with_suffix('.batch.log')

    # Add file handler for batch operations
# DISABLED:     batch_handler = logging.FileHandler(batch_log_file)
# DISABLED:     batch_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Use batch-specific formatter
# DISABLED:     batch_formatter = logging.Formatter(
# DISABLED:         '%(asctime)s - [BATCH] - %(name)s - %(levelname)s - %(message)s',
# DISABLED:         datefmt='%Y-%m-%d %H:%M:%S'
# DISABLED:     )
# DISABLED:     batch_handler.setFormatter(batch_formatter)
# DISABLED:     batch_logger.addHandler(batch_handler)

    # Prevent propagation to avoid duplicate logs
# DISABLED:     batch_logger.propagate = False

# DISABLED:     return batch_logger


# DISABLED: class TimestampedLogger:
    """Logger that automatically adds timestamps to log messages."""

# DISABLED:     def __init__(self, logger_name: str = "bsee"):
# DISABLED:         self.logger = logging.getLogger(logger_name)
# DISABLED:         self.last_timestamp = datetime.now()

# DISABLED:     def info(self, message: str) -> datetime:
        """Log info message and return timestamp."""
# DISABLED:         timestamp = datetime.now()
# DISABLED:         self.logger.info(message)
# DISABLED:         self.last_timestamp = timestamp
# DISABLED:         return timestamp

# DISABLED:     def debug(self, message: str) -> datetime:
        """Log debug message and return timestamp."""
# DISABLED:         timestamp = datetime.now()
# DISABLED:         self.logger.debug(message)
# DISABLED:         self.last_timestamp = timestamp
# DISABLED:         return timestamp

# DISABLED:     def warning(self, message: str) -> datetime:
        """Log warning message and return timestamp."""
# DISABLED:         timestamp = datetime.now()
# DISABLED:         self.logger.warning(message)
# DISABLED:         self.last_timestamp = timestamp
# DISABLED:         return timestamp

# DISABLED:     def error(self, message: str) -> datetime:
        """Log error message and return timestamp."""
# DISABLED:         timestamp = datetime.now()
# DISABLED:         self.logger.error(message)
# DISABLED:         self.last_timestamp = timestamp
# DISABLED:         return timestamp

# DISABLED:     def critical(self, message: str) -> datetime:
        """Log critical message and return timestamp."""
# DISABLED:         timestamp = datetime.now()
# DISABLED:         self.logger.critical(message)
# DISABLED:         self.last_timestamp = timestamp
# DISABLED:         return timestamp


# DISABLED: def get_logger(name: str):
    """Get a logger instance with the specified name."""
# DISABLED:     return logging.getLogger(name)