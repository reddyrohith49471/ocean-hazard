import sys
from utils.translator import translator
from utils.text_processor import processor
from ml_models.classifier import classifier
from utils.summarizer import summarizer
from exception.exception import CustomException


class HazardPipeline:
    def process(self, text):
        try:
            translated = translator.translate(text)
            cleaned = processor.preprocess(translated)
            prediction = classifier.predict(cleaned)

            summary = None
            if prediction == 1:
                summary = summarizer.summarize(cleaned, len(cleaned.split()))

            return translated, cleaned, prediction, summary

        except Exception as e:
            raise CustomException(e, sys)


hazard_pipeline = HazardPipeline()
