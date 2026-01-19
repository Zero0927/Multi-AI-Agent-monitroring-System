"""
Multi-AI Agent Monitoring System
Powered by LangChain Agent Framework with LangGraph
"""
from langgraph.graph import StateGraph, START, END
from graph_nodes import productivity_node, sentiment_node, compliance_node, interaction_node, correlation_node
from state_schema import AgentState
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def initialize_state() -> AgentState:
    """Initialize the agent state with default values"""
    return {
        "TCR": None,
        "SPI": None,
        "DCR": None,
        "CI": None,
        "OCS": None,
        "messages": [],
        "merged_data_path": None,
        "completed_agents": []
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 Multi-AI Agent Monitoring System")
    print("   Powered by LangChain + LangGraph")
    print("="*60)
    
    # Build the agent graph
    graph = StateGraph(AgentState)

    # Build the agent graph
    graph = StateGraph(AgentState)

    # Add agent nodes
    print("\n📋 Building Agent Graph...")
    graph.add_node("productivity", productivity_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("compliance", compliance_node)
    graph.add_node("interaction", interaction_node)
    graph.add_node("correlation", correlation_node)

    # Define workflow edges
    # All analysis agents run in parallel from START
    graph.add_edge(START, "productivity")
    graph.add_edge(START, "sentiment")
    graph.add_edge(START, "compliance")
    graph.add_edge(START, "interaction")

    # Correlation agent waits for all analysis agents
    graph.add_edge("productivity", "correlation")
    graph.add_edge("sentiment", "correlation")
    graph.add_edge("compliance", "correlation")
    graph.add_edge("interaction", "correlation")
    
    # Correlation is the final node
    graph.add_edge("correlation", END)

    # Compile and execute the graph
    print("✅ Graph compiled successfully")
    app = graph.compile()
    
    print("\n🚀 Starting Multi-Agent Analysis Pipeline...")
    print("-" * 60)
    
    # Run the workflow
    final_state = app.invoke(initialize_state())
    
    print("\n" + "="*60)
    print("📊 Multi-AI Agent Analysis Complete!")
    print("="*60)

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

    # Display Outcome Correlation Index with statistical significance
    print("\n🔗 Outcome Correlation Index (OCI):")
    ocs = final_state.get("OCS", None)
    if ocs:
        if isinstance(ocs, dict):
            print(f"  R² Score: {ocs.get('r_squared', 'N/A')}")
            print(f"  Statistical Significance: {ocs.get('significance', 'N/A')}")
            if ocs.get('p_values'):
                print(f"  P-values by Feature:")
                for feature, p_val in zip(ocs.get('feature_names', []), ocs.get('p_values', [])):
                    print(f"    - {feature}: {p_val}")
            if ocs.get('coefficients'):
                print(f"  Regression Coefficients:")
                for feature, coef in zip(ocs.get('feature_names', []), ocs.get('coefficients', [])):
                    print(f"    - {feature}: {coef}")
            if ocs.get('pca_variance'):
                print(f"  PCA Explained Variance Ratio:")
                for i, var in enumerate(ocs.get('pca_variance', []), 1):
                    print(f"    - Component {i}: {var}")
        else:
            print(f"  {ocs}")
    else:
        print("  Unable to calculate OCI")

    # ===== VISUALIZATIONS =====
    print("\n📊 Generating visualizations...")
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 12)
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Average Metrics Bar Chart
    ax1 = plt.subplot(2, 3, 1)
    metrics_names = ['TCR (%)', 'SPI', 'DCR (%)', 'CI']
    metrics_values = [avg_TCR, avg_SPI, avg_DCR, avg_CI]
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    bars = ax1.bar(metrics_names, metrics_values, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Score', fontsize=11, fontweight='bold')
    ax1.set_title('Average Agent Metrics', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 100)
    for bar, val in zip(bars, metrics_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Per-Entity TCR Distribution
    ax2 = plt.subplot(2, 3, 2)
    tcr_data = df['TCR'].dropna()
    ax2.hist(tcr_data, bins=30, color='#3498db', alpha=0.7, edgecolor='black')
    ax2.axvline(avg_TCR, color='red', linestyle='--', linewidth=2, label=f'Mean: {avg_TCR:.2f}%')
    ax2.set_xlabel('Task Completion Ratio (%)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax2.set_title('TCR Distribution', fontsize=12, fontweight='bold')
    ax2.legend()
    
    # 3. Scatter: TCR vs CI
    ax3 = plt.subplot(2, 3, 3)
    scatter = ax3.scatter(df['TCR'], df['CI'], alpha=0.6, c=df['SPI'], cmap='RdYlGn', s=100, edgecolor='black')
    ax3.set_xlabel('Task Completion Ratio (TCR)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Collaboration Index (CI)', fontsize=11, fontweight='bold')
    ax3.set_title('TCR vs CI (colored by SPI)', fontsize=12, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Sentiment Polarity Index', fontsize=10)
    
    # 4. Correlation Heatmap
    ax4 = plt.subplot(2, 3, 4)
    corr_matrix = df[['TCR', 'SPI', 'DCR', 'CI']].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                ax=ax4, cbar_kws={'label': 'Correlation'}, square=True)
    ax4.set_title('Metric Correlation Matrix', fontsize=12, fontweight='bold')
    
    # 5. Box Plot of Metrics (normalized)
    ax5 = plt.subplot(2, 3, 5)
    # Normalize metrics to 0-1 for comparison
    df_normalized = df[['TCR', 'DCR']].copy()
    df_normalized['TCR'] = df_normalized['TCR'] / 100
    df_normalized['DCR'] = df_normalized['DCR'] / 100
    df_normalized['SPI_norm'] = (df['SPI'] + 1) / 2  # Convert -1 to 1 scale to 0 to 1
    df_normalized['CI'] = df['CI']
    
    box_data = [df_normalized['TCR'], df_normalized['SPI_norm'], df_normalized['DCR'], df_normalized['CI']]
    bp = ax5.boxplot(box_data, labels=['TCR', 'SPI', 'DCR', 'CI'], patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax5.set_ylabel('Normalized Score (0-1)', fontsize=11, fontweight='bold')
    ax5.set_title('Metrics Distribution (Normalized)', fontsize=12, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3)
    
    # 6. OCI Summary
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    oci_text = f"""
    OUTCOME CORRELATION INDEX (OCI)
    {'='*40}
    
    R² Score: {ocs.get('r_squared', 'N/A')}
    Significance: {ocs.get('significance', 'N/A')}
    
    Regression Coefficients:
    • TCR: {ocs.get('coefficients', [None])[0]}
    • SPI: {ocs.get('coefficients', [None, None])[1] if len(ocs.get('coefficients', [])) > 1 else 'N/A'}
    • DCR: {ocs.get('coefficients', [None, None, None])[2] if len(ocs.get('coefficients', [])) > 2 else 'N/A'}
    • CI: {ocs.get('coefficients', [None, None, None, None])[3] if len(ocs.get('coefficients', [])) > 3 else 'N/A'}
    
    PCA Variance Explained:
    • Component 1: {ocs.get('pca_variance', [None])[0] if ocs.get('pca_variance') else 'N/A'}
    • Component 2: {ocs.get('pca_variance', [None, None])[1] if ocs.get('pca_variance') and len(ocs.get('pca_variance', [])) > 1 else 'N/A'}
    """
    ax6.text(0.05, 0.95, oci_text, transform=ax6.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save figure
    os.makedirs("results", exist_ok=True)
    viz_path = "results/multi_agent_analysis.png"
    plt.savefig(viz_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved: {viz_path}")
    plt.close()
    
    # Create additional focused visualizations
    # Visualization 2: Metric Radar/Spider Chart
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    categories = ['TCR', 'SPI', 'DCR', 'CI']
    values = [avg_TCR/100, (avg_SPI+1)/2, avg_DCR/100, avg_CI]  # Normalize to 0-1
    values += values[:1]  # Complete the circle
    angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
    angles += angles[:1]
    
    ax.plot(angles, values, 'o-', linewidth=2, color='#3498db', label='Current Metrics')
    ax.fill(angles, values, alpha=0.25, color='#3498db')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.set_title('Multi-Agent Metrics Radar Chart', fontsize=13, fontweight='bold', pad=20)
    ax.grid(True)
    
    radar_path = "results/metrics_radar.png"
    plt.savefig(radar_path, dpi=300, bbox_inches='tight')
    print(f"✅ Radar chart saved: {radar_path}")
    plt.close()
    
    print("\n✨ Visualization complete!")
