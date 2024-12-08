import logging
import os
from datetime import datetime

def setup_logging(log_dir='logs', log_file=None):
    """
    Configures the logging settings.

    Parameters:
    - log_dir (str): Directory where log files will be stored.
    - log_file (str): Specific log file name. If None, a timestamped file is created.
    """
    # Create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    if not log_file:
        # Generate a unique log file name based on the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"simulation_{timestamp}.log"

    log_path = os.path.join(log_dir, log_file)

    # Configure the logging settings
    logging.basicConfig(
        level=logging.DEBUG,  # Set the minimum log level
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',  # Log message format
        handlers=[
            logging.FileHandler(log_path),  # Log to the specified file
            logging.StreamHandler()  # Also log to the console
        ]
    )
