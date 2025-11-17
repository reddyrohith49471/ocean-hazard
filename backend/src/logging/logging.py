# src/logging/logger.py
import logging
import os
from datetime import datetime

# Logs folder inside backend directory
LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)

# Configure root logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(levelname)s %(name)s:%(lineno)d - %(message)s",
    level=logging.INFO,
)

# Provide a module-level logger instance for import
logger = logging.getLogger("posts_recom")
logger.setLevel(logging.INFO)


# logging.basicConfig(
#     filename=LOG_FILE_PATH,
#     format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO,
# )
