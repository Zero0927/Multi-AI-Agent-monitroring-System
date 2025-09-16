import pandas as pd

class InteractionAgent:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Collaboration Index (CI) per sender
        Returns DataFrame: Sender, CI
        """
        grouped = self.data.groupby("sender").apply(
            lambda df: df["is_reply"].sum() / len(df)
        ).reset_index(name="CI")
        return grouped