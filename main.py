from langgraph.graph import StateGraph, START
from graph_nodes import productivity_node, sentiment_node, compliance_node, interaction_node, correlation_node
from state_schema import AgentState
import pandas as pd

if __name__ == "__main__":
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("productivity", productivity_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("interaction", interaction_node)
    graph.add_node("correlation", correlation_node)

    # ✅ Define entrypoint
    graph.add_edge(START, "productivity")
    graph.add_edge(START, "sentiment")
    graph.add_edge(START, "compliance")
    graph.add_edge(START, "interaction")

    # Connect agents to correlation
    graph.add_edge("productivity", "correlation")
    graph.add_edge("sentiment", "correlation")
    graph.add_edge("compliance", "correlation")
    graph.add_edge("interaction", "correlation")

    # Compile and run
    app = graph.compile()
    final_state = app.invoke(AgentState())

    print("\n=== Detailed Multi-AI Agent Results ===")

    # Load merged dataset
    df = pd.read_csv("results/merged_metrics.csv")

    # Show first few rows of per-agent data
    print("\n📊 Sample of merged per-entity metrics:")
    print(df.head())

    # Compute and display averages
    avg_TCR = df["TCR"].mean()
    avg_SPI = df["SPI"].mean()
    avg_DCR = df["DCR"].mean()
    avg_CI = df["CI"].mean()

    print("\n📈 Aggregated Metrics:")
    print(f"Average Task Completion Ratio (TCR): {avg_TCR:.2f}%")
    print(f"Average Sentiment Polarity Index (SPI): {avg_SPI:.2f}")
    print(f"Average Disclosure Compliance Rate (DCR): {avg_DCR:.2f}%")
    print(f"Average Collaboration Index (CI): {avg_CI:.2f}")

    # Show final correlation score
    ocs = final_state.get("OCS", None)
    print(f"\n🔗 Outcome Correlation Score (OCS): {ocs}")