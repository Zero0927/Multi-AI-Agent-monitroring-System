import numpy as np
from agents.ProductivityAgent import ProductivityAgent
from agents.SentimentAgent import SentimentAgent
from agents.ComplianceAgent import ComplianceAgent
from agents.InteractionAgent import InteractionAgent
from agents.CorrelationEngine import CorrelationEngine

if __name__ == "__main__":
    # Paths to demo datasets
    TASKS_PATH = "demo_data/tasks.csv"
    EMAILS_PATH = "demo_data/emails.csv"
    COMPLIANCE_PATH = "demo_data/compliance.csv"
    MESSAGES_PATH = "demo_data/messages.csv"

    # Initialize agents (AI mode for demo)
    prod_agent = ProductivityAgent(TASKS_PATH, mode="ai")
    sent_agent = SentimentAgent(EMAILS_PATH, mode="baseline")   # use baseline first (AI slower)
    comp_agent = ComplianceAgent(COMPLIANCE_PATH, mode="ai")
    inter_agent = InteractionAgent(MESSAGES_PATH, mode="baseline")
    engine = CorrelationEngine(mode="baseline")

    # Train AI models where required
    prod_agent.train()
    comp_agent.train()

    # Collect metrics
    TCR = prod_agent.calculate_tcr()  # task completion rate
    SPI = sent_agent.calculate_spi()  # sentiment polarity index
    DCR = comp_agent.calculate_dcr()  # disclosure compliance
    CI = inter_agent.calculate_ci()   # collaboration index

    print("=== Demo Results ===")
    print("Task Completion Ratio (TCR):", round(TCR, 2))
    print("Sentiment Polarity Index (SPI):", round(SPI, 2))
    print("Disclosure Compliance Rate (DCR):", round(DCR, 2))
    print("Collaboration Index (CI):", round(CI, 2))

    # Correlation Engine demo
    X = np.array([[TCR, SPI, DCR, CI]])
    y = np.array([0.8])  # synthetic outcome for demo
    score = engine.run_regression(X, y)
    print("Outcome Correlation Score (OCS):", round(score, 2))