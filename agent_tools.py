"""
LangChain Tools for Multi-AI Agent System
Wraps agent functionality as LangChain tools for agent executors
"""
from langchain_core.tools import tool
from agents.ProductivityAgent import ProductivityAgent
from agents.SentimentAgent import SentimentAgent
from agents.ComplianceAgent import ComplianceAgent
from agents.InteractionAgent import InteractionAgent
from agents.CorrelationEngine import CorrelationEngine
import pandas as pd
import os

# ===== Productivity Tools =====

@tool
def compute_productivity_metrics(file_path: str = "data/Agile_Projects_Dataset.xlsx") -> str:
    """
    Compute Task Completion Ratio (TCR) metrics for all projects.
    Uses task mining and time series analysis to calculate productivity.
    
    Args:
        file_path: Path to the project dataset file (Excel or CSV)
    
    Returns:
        Summary of productivity metrics including average TCR and entity-level data
    """
    try:
        agent = ProductivityAgent(file_path)
        df = agent.get_metrics()
        
        avg_tcr = df["TCR"].mean()
        summary = f"""Productivity Metrics Analysis:
        
📊 Total Entities Analyzed: {len(df)}
📈 Average Task Completion Ratio (TCR): {avg_tcr:.2f}%
📉 Min TCR: {df['TCR'].min():.2f}%
📈 Max TCR: {df['TCR'].max():.2f}%
📊 Median TCR: {df['TCR'].median():.2f}%

Top 5 Performers:
{df.nlargest(5, 'TCR')[['EntityID', 'TCR']].to_string(index=False)}

Bottom 5 Performers:
{df.nsmallest(5, 'TCR')[['EntityID', 'TCR']].to_string(index=False)}
"""
        return summary
    except Exception as e:
        return f"Error computing productivity metrics: {str(e)}"

@tool
def get_productivity_data() -> pd.DataFrame:
    """
    Get raw productivity metrics data as DataFrame.
    Returns EntityID and TCR for all projects.
    """
    try:
        agent = ProductivityAgent("data/Agile_Projects_Dataset.xlsx")
        return agent.get_metrics()
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

# ===== Sentiment Tools =====

@tool
def compute_sentiment_metrics(file_path: str = None) -> str:
    """
    Compute Sentiment Polarity Index (SPI) for all workers using NLP analysis.
    Analyzes emotional data from communication to determine mood scores.
    
    Args:
        file_path: Optional path to sentiment data (defaults to mental_health_remote_workers.csv)
    
    Returns:
        Summary of sentiment metrics including average SPI and distribution
    """
    try:
        agent = SentimentAgent(file_path)
        df = agent.get_metrics()
        
        avg_spi = df["SPI"].mean()
        positive_count = len(df[df["SPI"] > 0.3])
        neutral_count = len(df[(df["SPI"] >= -0.3) & (df["SPI"] <= 0.3)])
        negative_count = len(df[df["SPI"] < -0.3])
        
        summary = f"""Sentiment Analysis Results:
        
😊 Total Workers Analyzed: {len(df)}
💭 Average Sentiment Polarity Index (SPI): {avg_spi:.3f}
📊 Sentiment Distribution:
   - Positive (>0.3): {positive_count} workers ({positive_count/len(df)*100:.1f}%)
   - Neutral (-0.3 to 0.3): {neutral_count} workers ({neutral_count/len(df)*100:.1f}%)
   - Negative (<-0.3): {negative_count} workers ({negative_count/len(df)*100:.1f}%)

📈 Most Positive Workers:
{df.nlargest(5, 'SPI').to_string(index=False)}

📉 Most Negative Workers:
{df.nsmallest(5, 'SPI').to_string(index=False)}
"""
        return summary
    except Exception as e:
        return f"Error computing sentiment metrics: {str(e)}"

@tool
def get_sentiment_data() -> pd.DataFrame:
    """
    Get raw sentiment metrics data as DataFrame.
    Returns worker identifiers and SPI scores.
    """
    try:
        agent = SentimentAgent()
        return agent.get_metrics()
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

# ===== Compliance Tools =====

@tool
def compute_compliance_metrics(file_path: str = None) -> str:
    """
    Compute Disclosure Compliance Rate (DCR) using log parsing and clickstream analysis.
    Tracks user interaction with AI monitoring notices.
    
    Args:
        file_path: Optional path to compliance data
    
    Returns:
        Summary of compliance metrics including DCR by company
    """
    try:
        agent = ComplianceAgent(file_path)
        df = agent.get_metrics()
        
        avg_dcr = df["DCR"].mean()
        
        summary = f"""Compliance Analysis Results:
        
🏢 Total Companies Analyzed: {len(df)}
✅ Average Disclosure Compliance Rate (DCR): {avg_dcr:.2f}%
📊 Total Employees Impacted: {df['Number of Employees Impacted'].sum()}

Top Compliant Companies:
{df.nlargest(5, 'DCR')[['Company Name', 'DCR']].to_string(index=False)}

Companies Needing Attention:
{df.nsmallest(5, 'DCR')[['Company Name', 'DCR']].to_string(index=False)}
"""
        return summary
    except Exception as e:
        return f"Error computing compliance metrics: {str(e)}"

@tool
def get_compliance_data() -> pd.DataFrame:
    """
    Get raw compliance metrics data as DataFrame.
    Returns company names and DCR scores.
    """
    try:
        agent = ComplianceAgent()
        return agent.get_metrics()
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

# ===== Interaction Tools =====

@tool
def compute_interaction_metrics(file_path: str = None) -> str:
    """
    Compute Collaboration Index (CI) using social graph analysis.
    Analyzes response time and message density from worker interactions.
    
    Args:
        file_path: Optional path to interaction data
    
    Returns:
        Summary of collaboration metrics including average CI
    """
    try:
        agent = InteractionAgent(file_path)
        df = agent.get_metrics()
        
        avg_ci = df["CI"].mean()
        high_collab = len(df[df["CI"] > 0.7])
        medium_collab = len(df[(df["CI"] >= 0.4) & (df["CI"] <= 0.7)])
        low_collab = len(df[df["CI"] < 0.4])
        
        summary = f"""Interaction Analysis Results:
        
👥 Total Workers Analyzed: {len(df)}
🤝 Average Collaboration Index (CI): {avg_ci:.3f}
📊 Collaboration Distribution:
   - High (>0.7): {high_collab} workers ({high_collab/len(df)*100:.1f}%)
   - Medium (0.4-0.7): {medium_collab} workers ({medium_collab/len(df)*100:.1f}%)
   - Low (<0.4): {low_collab} workers ({low_collab/len(df)*100:.1f}%)

Top Collaborators:
{df.nlargest(5, 'CI').to_string(index=False)}

Workers Needing Support:
{df.nsmallest(5, 'CI').to_string(index=False)}
"""
        return summary
    except Exception as e:
        return f"Error computing interaction metrics: {str(e)}"

@tool
def get_interaction_data() -> pd.DataFrame:
    """
    Get raw interaction metrics data as DataFrame.
    Returns worker IDs and CI scores.
    """
    try:
        agent = InteractionAgent()
        return agent.get_metrics()
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

# ===== Correlation Tools =====

@tool
def compute_correlation_analysis(merged_data_path: str = "results/merged_metrics.csv") -> str:
    """
    Perform multivariate regression and PCA analysis on all metrics.
    Computes Outcome Correlation Score (OCS) with statistical significance.
    
    Args:
        merged_data_path: Path to merged metrics CSV file
    
    Returns:
        Detailed correlation analysis including R², p-values, and PCA results
    """
    try:
        # Load merged data
        df = pd.read_csv(merged_data_path)
        df = df[["EntityID", "TCR", "SPI", "DCR", "CI"]].fillna(df[["TCR", "SPI", "DCR", "CI"]].mean())
        
        if len(df) < 2:
            return "❌ Insufficient data for correlation analysis (need at least 2 samples)"
        
        engine = CorrelationEngine()
        X = df[["TCR", "SPI", "DCR", "CI"]].values
        y = [1 if x > 70 else 0 for x in df["TCR"]]  # Binary outcome
        
        ocs = engine.run_regression(X, y)
        
        summary = f"""Correlation Analysis Results:
        
🔗 Outcome Correlation Score (OCS)
{'='*50}

📊 Statistical Metrics:
   - R² Score: {ocs.get('r_squared', 'N/A')}
   - Significance: {ocs.get('significance', 'N/A')}

📈 Regression Coefficients:
   - TCR: {ocs.get('coefficients', [None])[0]}
   - SPI: {ocs.get('coefficients', [None, None])[1] if len(ocs.get('coefficients', [])) > 1 else 'N/A'}
   - DCR: {ocs.get('coefficients', [None, None, None])[2] if len(ocs.get('coefficients', [])) > 2 else 'N/A'}
   - CI: {ocs.get('coefficients', [None, None, None, None])[3] if len(ocs.get('coefficients', [])) > 3 else 'N/A'}

🔬 P-Values (Statistical Significance):
"""
        if ocs.get('p_values'):
            for feature, p_val in zip(ocs.get('feature_names', []), ocs.get('p_values', [])):
                sig_marker = "✅" if p_val < 0.05 else "⚠️"
                summary += f"   {sig_marker} {feature}: {p_val}\n"
        
        summary += f"\n🧮 PCA Explained Variance:"
        if ocs.get('pca_variance'):
            for i, var in enumerate(ocs.get('pca_variance', []), 1):
                summary += f"\n   - Component {i}: {var}"
        
        return summary
    except Exception as e:
        return f"Error computing correlation analysis: {str(e)}"

# Tool Collections for each agent
PRODUCTIVITY_TOOLS = [compute_productivity_metrics, get_productivity_data]
SENTIMENT_TOOLS = [compute_sentiment_metrics, get_sentiment_data]
COMPLIANCE_TOOLS = [compute_compliance_metrics, get_compliance_data]
INTERACTION_TOOLS = [compute_interaction_metrics, get_interaction_data]
CORRELATION_TOOLS = [compute_correlation_analysis]
