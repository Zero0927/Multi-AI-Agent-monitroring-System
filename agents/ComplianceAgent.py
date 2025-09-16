import pandas as pd
from sklearn.linear_model import LogisticRegression

class ComplianceAgent:
    def __init__(self, file_path, mode="baseline"):
        self.data = pd.read_csv(file_path)
        self.mode = mode
        if mode == "ai":
            self.model = LogisticRegression()

    def calculate_dcr(self):
        """Baseline metric"""
        ack = self.data["Acknowledged"].sum()
        sessions = len(self.data)
        return (ack / sessions) * 100 if sessions > 0 else 0

    def train(self):
        if self.mode == "ai":
            X = self.data[["SessionLength", "LoginFrequency"]]
            y = self.data["Acknowledged"]
            self.model.fit(X, y)

    def predict_acknowledgement(self, session_length, login_freq):
        if self.mode == "ai":
            return self.model.predict([[session_length, login_freq]])[0]
        else:
            return self.calculate_dcr()