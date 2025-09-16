import pandas as pd

class ProductivityAgent:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Task Completion Ratio (TCR) per user
        Returns DataFrame: User, TCR
        """
        grouped = self.data.groupby("AssignedTo").apply(
            lambda df: (df["Status"].eq("Completed").sum() / len(df)) * 100
        ).reset_index(name="TCR")
        return grouped