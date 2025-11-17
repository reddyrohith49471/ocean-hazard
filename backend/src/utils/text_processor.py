import re
import emoji
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sys
from src.exception.exception import CustomException

class TextProcessor:
    def __init__(self):
        self.lem = WordNetLemmatizer()
        ENGLISH_STOPWORDS = {
            "a", "an", "the", "and", "or", "is", "are", "was", "were",
            "in", "on", "at", "to", "from", "for", "by", "with", "of",
            "that", "this", "it", "as", "be", "but", "if", "not"
        }
        self.stop = ENGLISH_STOPWORDS

    def preprocess(self, text):
        try:
            text = emoji.replace_emoji(text, replace=" ")
            text = re.sub(r"[^a-zA-Z0-9]", " ", text)
            text = text.lower().split()
            text = [self.lem.lemmatize(w) for w in text if w not in self.stop]
            return " ".join(text)
        except Exception as e:
            raise CustomException(e, sys)

processor = TextProcessor()
