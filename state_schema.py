from typing import TypedDict, Optional, List, Dict, Any, Annotated
from operator import add
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    """
    Shared state for the Multi-AI Agent System using LangGraph.
    Uses TypedDict for better LangGraph integration.
    """
    # Core Metrics - Using Optional to allow None initially
    TCR: Optional[float]  # Task Completion Ratio
    SPI: Optional[float]  # Sentiment Polarity Index
    DCR: Optional[float]  # Disclosure Compliance Rate
    CI: Optional[float]   # Collaboration Index
    OCS: Optional[Dict[str, Any]]  # Outcome Correlation Score
    
    # Agent Communication - accumulate messages
    messages: Annotated[List[AnyMessage], add]  # Message history for agents
    
    # Data Storage
    merged_data_path: Optional[str]  # Path to merged metrics CSV
    
    # Agent Status Tracking - collect completed agents
    completed_agents: Annotated[List[str], add]  # Track which agents finished