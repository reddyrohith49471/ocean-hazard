from deep_translator import GoogleTranslator
import sys
from exception.exception import CustomException


class Translator:
    def translate(self, text):
        try:
            return GoogleTranslator(source="auto", target="en").translate(text)
        except Exception as e:
            raise CustomException(e, sys)


translator = Translator()
