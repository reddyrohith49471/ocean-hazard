from transformers import pipeline
import sys
from exception.exception import CustomException

class Summarizer:
    def __init__(self):
        self.pipe = pipeline(
                "summarization",
                model="t5-small",
                tokenizer="t5-small",
                framework="pt" 
            )

    def summarize(self, text, words):
        try:
            min_len = max(5, int(words * 0.3))
            max_len = max(10, int(words * 0.7))

            out = self.pipe(text, min_length=min_len, max_length=max_len)
            return out[0]["summary_text"]

        except Exception as e:
            raise CustomException(e, sys)

summarizer = Summarizer()
