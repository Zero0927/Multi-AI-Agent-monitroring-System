"""
LangChain Agent Configuration for Multi-AI Agent System
Provides LLM setup and agent configurations for all agents
"""
import os
try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
except ImportError:
    # If dotenv not available, just use environment variables
    pass

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize LLM with environment variable or fallback
def get_llm(model="gpt-4o-mini", temperature=0.2):
    """
    Get configured LLM instance
    Set OPENAI_API_KEY in .env file or as environment variable
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not found. Set it in .env file or as environment variable")
        print("💡 For testing without OpenAI, the system will use mock responses")
        return None
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key
    )

# Agent Prompts
PRODUCTIVITY_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Productivity Analysis Agent specializing in task mining and time series analysis.
    Your role is to analyze worker productivity metrics, calculate Task Completion Ratios (TCR),
    and provide insights on productivity trends.
    
    You have access to tools that compute productivity metrics from project data.
    Use these tools to analyze the data and provide comprehensive productivity insights.
    
    When analyzing productivity:
    - Calculate TCR = (Tasks Completed / Tasks Assigned) * 100
    - Identify trends and patterns
    - Provide actionable insights for improvement
    """),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

SENTIMENT_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Sentiment Analysis Agent using advanced NLP and transformer models.
    Your role is to analyze emotional data from worker communications and compute Sentiment Polarity Index (SPI).
    
    You have access to tools that perform sentiment analysis on text data.
    Use these tools to analyze mood, emotional state, and overall sentiment.
    
    When analyzing sentiment:
    - Calculate SPI on scale from -1 (very negative) to +1 (very positive)
    - Identify emotional patterns and trends
    - Provide insights on worker well-being and morale
    """),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

COMPLIANCE_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Compliance Monitoring Agent specializing in regulatory adherence tracking.
    Your role is to analyze user interaction with AI monitoring notices and compute Disclosure Compliance Rate (DCR).
    
    You have access to tools that track compliance metrics through log parsing and clickstream analysis.
    Use these tools to ensure regulatory compliance and notice acknowledgment.
    
    When analyzing compliance:
    - Calculate DCR = Average notice viewed events per session
    - Track acknowledgment patterns
    - Identify compliance risks and gaps
    """),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

INTERACTION_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Social Interaction Analysis Agent using social graph analysis.
    Your role is to analyze collaboration patterns and compute Collaboration Index (CI).
    
    You have access to tools that analyze response times, message density, and interaction patterns.
    Use these tools to understand team dynamics and collaboration effectiveness.
    
    When analyzing interactions:
    - Calculate CI based on response time and message density
    - Analyze collaboration patterns
    - Identify communication bottlenecks and opportunities
    """),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

CORRELATION_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Correlation Analysis Agent specializing in multivariate regression and PCA.
    Your role is to integrate insights from all agents and compute the Outcome Correlation Score (OCS).
    
    You have access to tools that perform statistical analysis, regression, and correlation studies.
    Use these tools to identify relationships between different metrics and predict outcomes.
    
    When performing correlation analysis:
    - Run multivariate regression on TCR, SPI, DCR, and CI
    - Calculate R² scores and statistical significance (p-values)
    - Perform PCA for dimensionality reduction
    - Provide actionable insights on metric relationships
    """),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def get_configured_llm():
    """
    Get LLM or None for testing without API key.
    Returns None if no API key is available - system will skip LLM reasoning
    but still compute all metrics correctly.
    """
    llm = get_llm()
    if llm is None:
        print("📝 Running without LLM - metrics will be computed without AI reasoning")
        return None
    return llm
