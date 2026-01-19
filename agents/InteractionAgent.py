import pandas as pd
import os

class InteractionAgent:
    def __init__(self, file_path=None):
        # Default to remote_worker_productivity_1000.csv if no file path provided
        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "data",
                "remote_worker_productivity_1000.csv"
            )
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Collaboration Index (CI) using Social Graph Analysis.
        Analyzes response time and message density from worker interactions.
        Formula: Response time, message density.
        Returns DataFrame: Worker, CI
        """
        # Message density: derived from break frequency (higher breaks = more interactions)
        self.data["message_density"] = (
            (self.data["break_frequency_per_day"] / 5) * 100
        ).clip(0, 100)
        
        # Response time (inverse): measured via real-time feedback score
        # Higher feedback score = better responsiveness
        self.data["response_time"] = (
            (self.data["real_time_feedback_score"] / 100) * 100
        ).clip(0, 100)
        
        # Collaboration Index = average of message density and response time
        self.data["CI"] = (
            (self.data["message_density"] + self.data["response_time"]) / 200
        ).clip(0, 1)
        
        grouped = self.data.groupby("worker_id").agg({"CI": "mean"}).reset_index()
        return grouped