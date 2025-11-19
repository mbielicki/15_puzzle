"""Logging configuration utilities."""

import os
import sys
import logging
from datetime import datetime


def setup_logging(algorithm_name):
    """Configure logging with algorithm-specific log file.
    
    Args:
        algorithm_name: Name of the algorithm being used
        
    Returns:
        tuple: (logger instance, log filename)
    """
    os.makedirs('logs', exist_ok=True)
    
    # Create timestamp for unique log files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/{algorithm_name}_{timestamp}.log'
    
    # Force flush after each log
    class FlushFileHandler(logging.FileHandler):
        def emit(self, record):
            super().emit(record)
            self.flush()
    
    # Create file handler with unbuffered writing
    file_handler = FlushFileHandler(log_filename, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    # Create console handler - output to stdout for real-time visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, console_handler],
        force=True
    )
    
    return logging.getLogger(__name__), log_filename
