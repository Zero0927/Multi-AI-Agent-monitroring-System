import pandas as pd
import os

class ComplianceAgent:
    def __init__(self, file_path=None):
        # Default to Enterprise_GenAI_Adoption_Impact.csv if no file path provided
        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "data",
                "Enterprise_GenAI_Adoption_Impact.csv"
            )
        self.data = pd.read_csv(file_path)

    def get_metrics(self):
        """
        Compute Disclosure Compliance Rate (DCR) based on training completion.
        Analyzes whether companies provided adequate training for GenAI adoption.
        Formula: (Training Hours Provided / Number of Employees) normalized to compliance score
        Returns DataFrame with company compliance metrics
        """
        # Calculate training hours per employee as a compliance indicator
        # More training = better compliance with responsible AI adoption practices
        self.data["training_per_employee"] = (
            self.data["Training Hours Provided"] / self.data["Number of Employees Impacted"]
        )
        
        # Group by company
        metrics = self.data.groupby("Company Name").agg({
            "Number of Employees Impacted": "first",
            "training_per_employee": "mean"
        }).reset_index()
        
        # DCR based on training compliance (assuming 20 hours is full compliance = 100%)
        # Companies providing adequate training show better compliance with AI governance
        metrics["DCR"] = (
            (metrics["training_per_employee"] / 20.0).clip(0, 1) * 100
        )
        
        # Alternative: Also check for positive sentiment indicators related to training/governance
        def has_training_mention(text):
            if pd.isna(text):
                return 0
            text_lower = str(text).lower()
            training_keywords = ["training", "learn", "transition", "documentation", "guidance"]
            return 1 if any(keyword in text_lower for keyword in training_keywords) else 0
        
        self.data["training_mentioned"] = self.data["Employee Sentiment"].apply(has_training_mention)
        
        # Add sentiment-based compliance boost (up to 20% bonus)
        sentiment_compliance = self.data.groupby("Company Name")["training_mentioned"].mean() * 20
        
        # Merge sentiment bonus
        metrics = metrics.merge(
            sentiment_compliance.reset_index().rename(columns={"training_mentioned": "sentiment_bonus"}),
            on="Company Name",
            how="left"
        )
        
        # Final DCR = training compliance + sentiment bonus
        metrics["DCR"] = (metrics["DCR"] + metrics["sentiment_bonus"]).clip(0, 100)
        
        return metrics[["Company Name", "Number of Employees Impacted", "DCR"]]