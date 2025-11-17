import pickle
import os
import sys
from src.exception.exception import CustomException
from src.logging.logging import logger


class HazardClassifier:
    def __init__(self):
        try:
            model_path = os.path.join("src", "model", "ocean_hazard_model1.pkl")
            with open(model_path, "rb") as f:
                self.vectorizer, self.model = pickle.load(f)

            logger.info("ML model loaded.")
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, text):
        try:
            vec = self.vectorizer.transform([text])
            return int(self.model.predict(vec)[0])
        except Exception as e:
            raise CustomException(e, sys)


classifier = HazardClassifier()
