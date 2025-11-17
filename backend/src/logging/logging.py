import logging
import os
from datetime import datetime

LOGS_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(levelname)s %(name)s:%(lineno)d - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("ocean_hazard")
logger.setLevel(logging.INFO)
