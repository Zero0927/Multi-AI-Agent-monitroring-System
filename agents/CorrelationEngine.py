import numpy as np
from sklearn.linear_model import LinearRegression

class CorrelationEngine:
    def __init__(self):
        self.model = LinearRegression()

    def run_regression(self, X, y):
        if len(X) < 2:
            print("⚠️ Not enough samples for correlation. Provide N ≥ 2.")
            return np.nan  
        self.model.fit(X, y)
        return self.model.score(X, y)  # R² score