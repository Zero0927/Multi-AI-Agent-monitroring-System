# Multi-AI Agent Monitoring System
## Now Powered by LangChain Agent Framework

### 🎯 Overview
This system uses **LangChain** as the agent framework combined with **LangGraph** for workflow orchestration to analyze enterprise productivity, sentiment, compliance, and collaboration metrics.

### 🆕 What's New: LangChain Integration

#### Architecture
- **Agent Framework**: LangChain with tool-calling agents
- **Workflow Engine**: LangGraph for state management and orchestration
- **LLM**: OpenAI GPT-4o-mini (configurable)
- **Tools**: Each agent has specialized tools for data analysis

#### Key Components

1. **agent_config.py** - LangChain agent configuration
   - LLM setup and initialization
   - Agent prompts for each specialized agent
   - Mock LLM for testing without API keys

2. **agent_tools.py** - LangChain tools wrapping agent functionality
   - Productivity tools (TCR computation)
   - Sentiment tools (SPI analysis)
   - Compliance tools (DCR tracking)
   - Interaction tools (CI metrics)
   - Correlation tools (OCS calculation)

3. **state_schema.py** - Shared state using TypedDict
   - Core metrics (TCR, SPI, DCR, CI, OCS)
   - Message history for agent communication
   - Status tracking for each agent

4. **graph_nodes.py** - LangChain agent executors as graph nodes
   - Each node creates a LangChain agent with tools
   - Agents invoke tools and update shared state
   - Agents communicate via message passing

5. **main.py** - LangGraph workflow orchestration
   - Parallel execution of analysis agents
   - Sequential correlation analysis
   - Visualization and reporting

### 🚀 Quick Start

#### 1. Install Dependencies
```bash
source ai_agents_env/bin/activate
pip install -r requirements.txt
```

#### 2. Set Up OpenAI API Key

**Option A: Using .env file (Recommended)**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**Option B: Environment Variable**
```bash
export OPENAI_API_KEY=sk-your-key-here
```

**Option C: Testing Without API Key**
The system will use a mock LLM if no API key is provided. Agents will still compute metrics but won't provide LLM-generated insights.

#### 3. Run the System
```bash
python main.py
```

### 🤖 Agent Architecture

```
┌─────────────────────────────────────────────────────┐
│                   START                             │
└──────────┬──────────┬──────────┬──────────┬─────────┘
           │          │          │          │
           ▼          ▼          ▼          ▼
    ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐
    │Productiv.│ │Sentiment│ │Complianc.│ │Interacti.│
    │  Agent   │ │  Agent  │ │  Agent   │ │  Agent   │
    │          │ │         │ │          │ │          │
    │  Tools:  │ │ Tools:  │ │ Tools:   │ │ Tools:   │
    │ - TCR    │ │ - SPI   │ │ - DCR    │ │ - CI     │
    └────┬─────┘ └────┬────┘ └────┬─────┘ └────┬─────┘
         │            │           │            │
         └────────────┴───────────┴────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ Correlation   │
              │    Agent      │
              │               │
              │   Tools:      │
              │   - OCS       │
              │   - Regression│
              │   - PCA       │
              └───────┬───────┘
                      │
                      ▼
                  ┌───────┐
                  │  END  │
                  └───────┘
```

### 📊 Agents and Their Tools

#### 1. Productivity Agent
- **Purpose**: Analyze task completion and productivity trends
- **Tools**:
  - `compute_productivity_metrics`: Calculate TCR from project data
  - `get_productivity_data`: Retrieve raw productivity metrics
- **Output**: Task Completion Ratio (TCR) 0-100%

#### 2. Sentiment Agent
- **Purpose**: Analyze emotional data and worker sentiment
- **Tools**:
  - `compute_sentiment_metrics`: NLP-based sentiment analysis
  - `get_sentiment_data`: Retrieve raw sentiment scores
- **Output**: Sentiment Polarity Index (SPI) -1 to +1

#### 3. Compliance Agent
- **Purpose**: Monitor regulatory adherence and notice acknowledgment
- **Tools**:
  - `compute_compliance_metrics`: Track notice interactions
  - `get_compliance_data`: Retrieve compliance records
- **Output**: Disclosure Compliance Rate (DCR) 0-100%

#### 4. Interaction Agent
- **Purpose**: Analyze collaboration patterns and team dynamics
- **Tools**:
  - `compute_interaction_metrics`: Measure collaboration effectiveness
  - `get_interaction_data`: Retrieve interaction patterns
- **Output**: Collaboration Index (CI) 0-1

#### 5. Correlation Agent
- **Purpose**: Integrate all metrics and perform statistical analysis
- **Tools**:
  - `compute_correlation_analysis`: Multivariate regression + PCA
- **Output**: Outcome Correlation Score (OCS) with R², p-values, coefficients

### 🔧 Configuration

#### LLM Settings (agent_config.py)
```python
# Change model
llm = get_llm(model="gpt-4", temperature=0.2)

# Adjust temperature (0.0 = deterministic, 1.0 = creative)
llm = get_llm(temperature=0.5)
```

#### Agent Prompts
Each agent has a specialized prompt in `agent_config.py`. Customize them to adjust agent behavior.

### 📈 Output

The system generates:

1. **Console Output**
   - Agent execution logs
   - Metric summaries
   - Statistical analysis results

2. **CSV Files**
   - `results/merged_metrics.csv` - Combined metrics from all agents

3. **Visualizations**
   - `results/multi_agent_analysis.png` - Comprehensive dashboard
   - `results/metrics_radar.png` - Radar chart of key metrics
   - `results/individual_plots/` - Separate plots for each metric

### 🔍 How It Works

1. **Initialization**: State is initialized with default values
2. **Parallel Execution**: Analysis agents (Productivity, Sentiment, Compliance, Interaction) run in parallel
3. **Tool Invocation**: Each agent uses LangChain tools to compute metrics
4. **State Updates**: Agents update the shared state with computed metrics
5. **Correlation**: After all analysis agents complete, the Correlation agent runs
6. **Statistical Analysis**: OCS computed using regression and PCA
7. **Visualization**: Results are visualized and saved

### 🧪 Testing

**Without OpenAI API**
The system will work with mock LLM responses if no API key is provided. All metrics will be computed normally.

**With OpenAI API**
Agents will provide LLM-generated insights and analysis in addition to computed metrics.

### 📦 Dependencies

Core frameworks:
- `langgraph` - Workflow orchestration
- `langchain` - Agent framework
- `langchain-openai` - OpenAI integration
- `langchain-core` - Core utilities

Analysis libraries:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning
- `scipy` - Statistical analysis
- `textblob` - NLP sentiment analysis

Visualization:
- `matplotlib` - Plotting
- `seaborn` - Statistical visualization

### 🎓 Key Concepts

**LangChain Agents**
- Agents = LLM + Tools + Prompt
- Agents can reason about which tools to use
- Agents can chain multiple tool calls

**LangGraph**
- Stateful workflow orchestration
- Supports parallel and sequential execution
- Message passing between agents

**TypedDict State**
- Shared state across all agents
- Type-safe state management
- Message history for agent communication

### 🚨 Troubleshooting

**Issue**: `OPENAI_API_KEY not found`
- **Solution**: Set API key in `.env` file or environment variable
- **Alternative**: System will use mock LLM automatically

**Issue**: `Agent execution error`
- **Solution**: Check that all data files are present in `data/` directory
- **Solution**: Ensure all dependencies are installed

**Issue**: `Not enough samples for correlation`
- **Solution**: Ensure at least 2 rows of data in each dataset

### 📝 Migration from Old System

The system is now **fully powered by LangChain agents** instead of simple function calls:

**Before**: Direct function calls to agent classes
```python
df = ProductivityAgent("data.xlsx").get_metrics()
```

**Now**: LangChain agents with tools
```python
agent = create_tool_calling_agent(llm, PRODUCTIVITY_TOOLS, PRODUCTIVITY_AGENT_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "Analyze productivity..."})
```

### 🤝 Contributing

The system is modular and extensible:
- Add new agents: Create tools in `agent_tools.py` and node in `graph_nodes.py`
- Add new metrics: Extend `AgentState` in `state_schema.py`
- Customize agents: Modify prompts in `agent_config.py`

### 📄 License

MIT License - feel free to use and modify for your research and projects.

---

**Built with ❤️ using LangChain + LangGraph**
