from sklearn.ensemble import RandomForestRegressor

class CorrelationEngine:
    def __init__(self, mode="baseline"):
        self.mode = mode
        if mode == "ai":
            self.model = RandomForestRegressor()

    def run_regression(self, X, y):
        if self.mode == "ai":
            self.model.fit(X, y)
            return self.model.score(X, y)
        else:
            # Simple correlation (baseline)
            import numpy as np
            return np.corrcoef(X.flatten(), y.flatten())[0, 1]