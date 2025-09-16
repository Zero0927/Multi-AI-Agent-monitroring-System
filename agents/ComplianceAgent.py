import pandas as pd

class ComplianceAgent:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Disclosure Compliance Rate (DCR) per user
        Returns DataFrame: User, DCR
        """
        grouped = self.data.groupby("User").apply(
            lambda df: (df["Acknowledged"].sum() / len(df)) * 100
        ).reset_index(name="DCR")
        return grouped