"""Centralized logging configuration for SRM backend."""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(verbose: bool = False):
    """
    Setup logging configuration for the application.
    
    Args:
        verbose: If True, enables DEBUG level logging. Otherwise uses INFO level.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Log file path
    log_file = logs_dir / "srm_debug.log"
    
    # Set root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation (max 10MB, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Log initialization message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Verbose mode: {verbose}")
    logger.info(f"Log file: {log_file.absolute()}")
    
    return logger

