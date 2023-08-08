import logging
from datetime import datetime
import os
def setup_logger():
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Set the level to INFO. This means that logger will handle all messages of level INFO and above
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()

    today = datetime.today().strftime('%d_%m_%Y')
    if not os.path.exists('logs'):
        os.mkdir('logs')
    f_handler = logging.FileHandler(f"./logs/logs_{today}.log")
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    format = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(format)
    f_handler.setFormatter(format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


aeya_logger = setup_logger()
