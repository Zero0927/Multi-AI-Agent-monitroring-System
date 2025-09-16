import pandas as pd
from textblob import TextBlob
from transformers import pipeline

class SentimentAgent:
    def __init__(self, file_path, mode="baseline"):
        self.data = pd.read_csv(file_path)
        self.mode = mode
        if mode == "ai":
            self.model = pipeline("sentiment-analysis")

    def calculate_spi(self):
        """Baseline metric using TextBlob"""
        messages = self.data["message"].head(100)
        scores = [TextBlob(str(msg)).sentiment.polarity for msg in messages]
        return sum(scores) / len(scores) if scores else 0

    def calculate_spi_ai(self):
        """AI-powered transformer sentiment analysis"""
        messages = self.data["message"].head(20).tolist()
        results = self.model(messages)
        scores = [(1 if r["label"] == "POSITIVE" else -1) * r["score"] for r in results]
        return sum(scores) / len(scores)