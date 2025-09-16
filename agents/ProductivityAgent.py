import pandas as pd
from sklearn.linear_model import LinearRegression

class ProductivityAgent:
    def __init__(self, file_path, mode="baseline"):
        self.data = pd.read_csv(file_path)
        self.mode = mode
        if mode == "ai":
            self.model = LinearRegression()

    def calculate_tcr(self):
        """Baseline metric"""
        completed = len(self.data[self.data["Status"] == "Completed"])
        assigned = len(self.data)
        return (completed / assigned) * 100 if assigned > 0 else 0

    def train(self):
        if self.mode == "ai":
            X = self.data[["EstimatedHours"]]
            y = self.data["ActualHours"]
            self.model.fit(X, y)

    def predict_completion(self, est_hours):
        if self.mode == "ai":
            return self.model.predict([[est_hours]])[0]
        else:
            return self.calculate_tcr()