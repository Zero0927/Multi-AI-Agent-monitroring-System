import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class CorrelationEngine:
    def __init__(self):
        self.model = LinearRegression()

    def compute_correlation(self, metrics_df, target_df):
        self.model.fit(metrics_df, target_df)
        predictions = self.model.predict(metrics_df)
        return r2_score(target_df, predictions)