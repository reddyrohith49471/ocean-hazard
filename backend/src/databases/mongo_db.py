import pymongo
import sys
from exception.exception import CustomException
from logging.logging import logger


class MongoDB:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(
                "mongodb+srv://reddyrohith20061902_db_user:ocean-hazard@cluster0.h7s3hox.mongodb.net/"
            )
            self.client.admin.command("ping")
            logger.info("MongoDB connected.")
        except Exception as e:
            raise CustomException(e, sys)

        self.db = self.client["Ocean_Hazard_DB"]
        self.collection = self.db["Hazard_posts"]
