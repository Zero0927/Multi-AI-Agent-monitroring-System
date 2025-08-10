class ComplianceAgent:
    def __init__(self, logs):
        self.logs = logs

    def calculate_dcr(self):
        acknowledgements = sum(1 for log in self.logs if log['acknowledged'])
        total_sessions = len(self.logs)
        return (acknowledgements / total_sessions) * 100 if total_sessions > 0 else 0