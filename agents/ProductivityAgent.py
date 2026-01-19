# https://www.kaggle.com/datasets/digrok/agile-project-dataset-2024
import pandas as pd


class ProductivityAgent:
    def __init__(self, file_path: str):
        # Support both CSV (legacy) and Excel (Agile_Projects_Dataset.xlsx)
        if file_path.lower().endswith((".xlsx", ".xls")):
            self.data = pd.read_excel(file_path)
        else:
            self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Task Completion Rate (TCR) using Task Mining + Time Series analysis.
        Formula: TCR = (Tasks Completed / Tasks Assigned) * 100
        Returns DataFrame: EntityID, TCR (0-100).
        """
        df = self.data.copy()

        # Use actual task completion if available, else use Agile Effectiveness as proxy
        if "Completed Tasks" in df.columns and "Scheduled Tasks" in df.columns:
            df["TCR"] = (df["Completed Tasks"] / df["Scheduled Tasks"] * 100).clip(0, 100)
        else:
            # Fallback: Agile Effectiveness is proxy for task completion rate
            df["TCR"] = df["Agile Effectiveness"].astype(float) / 5 * 100

        df["EntityID"] = [f"Project_{i+1}" for i in range(len(df))]
        return df[["EntityID", "TCR"]]