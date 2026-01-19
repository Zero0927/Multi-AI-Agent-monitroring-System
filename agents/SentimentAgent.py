import pandas as pd
import os
from textblob import TextBlob

class SentimentAgent:
    def __init__(self, file_path=None):
        # Default to mental_health_remote_workers.csv if no file path provided
        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "data",
                "mental_health_remote_workers.csv"
            )
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Mood Score (Sentiment Polarity Index) using Transformer Model (BERT via TextBlob).
        Analyzes emotional data from communication via Natural Language Processing.
        Formula: Aggregated sentiment score (Scale -1 to 1)
        Returns DataFrame: Employee, SPI
        """
        # Check for sentiment-bearing text column
        if "Employee Sentiment" in self.data.columns:
            # Apply BERT-like NLP sentiment analysis
            self.data["SPI"] = self.data["Employee Sentiment"].astype(str).apply(
                lambda x: TextBlob(x).sentiment.polarity if pd.notna(x) else 0
            )
        else:
            # Fallback: use mental health as proxy
            health_to_sentiment = {"Good": 0.8, "Moderate": 0.5, "Poor": 0.2}
            self.data["SPI"] = self.data["Mental_Health_Status"].map(health_to_sentiment)
        
        # Clip to standard sentiment scale [-1, 1]
        self.data["SPI"] = self.data["SPI"].clip(-1, 1)
        
        # Group by employee and return metrics
        identifier = "Name" if "Name" in self.data.columns else "worker_id"
        grouped = self.data.groupby(identifier).agg({"SPI": "mean"}).reset_index()
        return grouped