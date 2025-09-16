import os
import pandas as pd
from agents.ProductivityAgent import ProductivityAgent
from agents.SentimentAgent import SentimentAgent
from agents.ComplianceAgent import ComplianceAgent
from agents.InteractionAgent import InteractionAgent
from agents.CorrelationEngine import CorrelationEngine
from state_schema import AgentState   # type schema

# global merged metrics
metrics_df = pd.DataFrame(columns=["EntityID"])

def safe_merge(df_main, df_new):
    """Ensure safe merging even if df_main is empty."""
    if df_main.empty:
        return df_new
    return df_main.merge(df_new, on="EntityID", how="outer")

def productivity_node(state: AgentState) -> AgentState:
    global metrics_df
    df = ProductivityAgent("demo_data/tasks.csv").get_metrics()
    df = df.rename(columns={"AssignedTo": "EntityID"})
    metrics_df = safe_merge(metrics_df, df)
    return state

def sentiment_node(state: AgentState) -> AgentState:
    global metrics_df
    df = SentimentAgent("demo_data/emails.csv").get_metrics()
    df = df.rename(columns={"Sender": "EntityID"})
    metrics_df = safe_merge(metrics_df, df)
    return state

def compliance_node(state: AgentState) -> AgentState:
    global metrics_df
    df = ComplianceAgent("demo_data/compliance.csv").get_metrics()
    df = df.rename(columns={"User": "EntityID"})
    metrics_df = safe_merge(metrics_df, df)
    return state

def interaction_node(state: AgentState) -> AgentState:
    global metrics_df
    df = InteractionAgent("demo_data/messages.csv").get_metrics()
    df = df.rename(columns={"sender": "EntityID"})
    metrics_df = safe_merge(metrics_df, df)
    return state

def correlation_node(state: AgentState) -> AgentState:
    global metrics_df
    engine = CorrelationEngine()
    df = metrics_df.dropna(subset=["TCR", "SPI", "DCR", "CI"])

    if len(df) >= 2:
        X = df[["TCR", "SPI", "DCR", "CI"]].values
        y = [1 if x > 70 else 0 for x in df["TCR"]]  # synthetic binary outcome
        state.OCS = engine.run_regression(X, y)

        os.makedirs("results", exist_ok=True)
        df.to_csv("results/merged_metrics.csv", index=False)
        print("📂 merged_metrics.csv saved")
    else:
        state.OCS = None
        print("⚠️ Not enough valid rows for correlation")

    return state