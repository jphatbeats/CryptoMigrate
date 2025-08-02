import logging
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except:
            # If we can't create logs directory, just log to console
            log_dir = None
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Set log level from environment variable
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, log_level, logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(log_format, date_format)
    console_handler.setFormatter(console_formatter)
    
    # Create file handler if logs directory exists
    file_handler = None
    if log_dir:
        try:
            log_filename = f"{log_dir}/trading_server_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(log_format, date_format)
            file_handler.setFormatter(file_formatter)
        except Exception as e:
            print(f"Warning: Could not create file handler: {e}")
    
    # Get root logger and configure handlers
    root_logger = logging.getLogger()
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(console_handler)
    if file_handler:
        root_logger.addHandler(file_handler)
    
    # Configure specific loggers
    loggers = [
        'main_server',
        'exchange_manager', 
        'trading_functions',
        'error_handler'
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        # Don't add handlers here as they inherit from root logger
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("Logging configuration completed")
    logger.info(f"Log level set to: {log_level}")
    if log_dir:
        logger.info(f"Logs will be written to: {log_dir}")
    else:
        logger.info("File logging disabled - console only")
