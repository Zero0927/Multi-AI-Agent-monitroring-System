import pandas as pd
from textblob import TextBlob

class SentimentAgent:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Sentiment Polarity Index (SPI) per sender
        Returns DataFrame: Sender, SPI
        """
        grouped = self.data.groupby("Sender")["message"].apply(
            lambda msgs: sum([TextBlob(str(m)).sentiment.polarity for m in msgs]) / len(msgs)
        ).reset_index(name="SPI")
        return grouped