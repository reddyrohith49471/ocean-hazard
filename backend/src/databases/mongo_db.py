import pymongo
import sys
from src.exception.exception import CustomException
from src.logging.logging import logger
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = pymongo.MongoClient(self.mongo_uri)
        try:
            self.client.admin.command("ping")
            logger.info("MongoDB connected.")
        except Exception as e:
            raise CustomException(e, sys)

        self.db = self.client["Ocean_Hazard_DB"]
        self.collection = self.db["Hazard_posts"]

