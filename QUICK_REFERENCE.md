# Quick Reference Guide

## Running the System

### Basic Run
```bash
cd "/Users/zero/Documents/City UMaster:Phd/RESR694D/Multi-AI-Agent-monitroring-System"
./ai_agents_env/bin/python main.py
```

### With OpenAI API
```bash
# Set API key
export OPENAI_API_KEY="sk-your-key-here"
# Or create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Run
./ai_agents_env/bin/python main.py
```

## Key Files

| File | Purpose |
|------|---------|
| `agent_config.py` | LLM setup and agent prompts |
| `agent_tools.py` | LangChain tool definitions |
| `graph_nodes.py` | Agent node implementations |
| `state_schema.py` | Shared state structure |
| `main.py` | Main entry point |
| `split_analysis_plots.py` | Plot splitting utility |

## Agent Tools

### Productivity Agent
- `compute_productivity_metrics()` - Calculate TCR
- `get_productivity_data()` - Get raw data

### Sentiment Agent
- `compute_sentiment_metrics()` - Calculate SPI
- `get_sentiment_data()` - Get raw data

### Compliance Agent
- `compute_compliance_metrics()` - Calculate DCR
- `get_compliance_data()` - Get raw data

### Interaction Agent
- `compute_interaction_metrics()` - Calculate CI
- `get_interaction_data()` - Get raw data

### Correlation Agent
- `compute_correlation_analysis()` - Calculate OCS with regression

## Metrics

| Metric | Range | Description |
|--------|-------|-------------|
| TCR | 0-100% | Task Completion Ratio |
| SPI | -1 to +1 | Sentiment Polarity Index |
| DCR | 0-100% | Disclosure Compliance Rate |
| CI | 0-1 | Collaboration Index |
| OCS | - | Outcome Correlation Score (R², p-values) |

## Output Files

### Data
- `results/merged_metrics.csv` - Combined metrics from all agents

### Visualizations
- `results/multi_agent_analysis.png` - 6-panel dashboard
- `results/metrics_radar.png` - Radar chart
- `results/individual_plots/*.png` - 6 separate plots

## Customization

### Change LLM Model
Edit `agent_config.py`:
```python
def get_llm(model="gpt-4", temperature=0.2):
```

### Modify Agent Prompt
Edit `agent_config.py`:
```python
PRODUCTIVITY_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Your custom prompt here..."),
    ...
])
```

### Add New Tool
Edit `agent_tools.py`:
```python
@tool
def new_tool(param: str) -> str:
    """Tool description for LLM"""
    # Implementation
    return result
```

### Add New Agent
1. Create tools in `agent_tools.py`
2. Add prompt in `agent_config.py`
3. Create node in `graph_nodes.py`
4. Add to graph in `main.py`

## Troubleshooting

### Problem: No OpenAI API Key
**Solution**: System works without it! Uses mock LLM.

### Problem: Import Error
**Solution**: Reinstall dependencies
```bash
./ai_agents_env/bin/pip install -r requirements.txt
```

### Problem: Data Files Not Found
**Solution**: Check data/ directory has:
- `Agile_Projects_Dataset.xlsx`
- `mental_health_remote_workers.csv`
- `remote_worker_productivity_1000.csv`
- `Enterprise_GenAI_Adoption_Impact.csv`

### Problem: Visualizations Not Generated
**Solution**: Install matplotlib and seaborn
```bash
./ai_agents_env/bin/pip install matplotlib seaborn
```

## Common Commands

### Install All Dependencies
```bash
./ai_agents_env/bin/pip install -r requirements.txt
```

### Upgrade pip
```bash
./ai_agents_env/bin/python3 -m pip install --upgrade pip
```

### Check Installed Packages
```bash
./ai_agents_env/bin/pip list | grep langchain
```

### Split Analysis Plots
```bash
./ai_agents_env/bin/python split_analysis_plots.py
```

## Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.2
```

## Workflow Execution Order

1. **Initialize State** - Set defaults
2. **Parallel Analysis** - Run 4 agents concurrently
   - Productivity Agent
   - Sentiment Agent  
   - Compliance Agent
   - Interaction Agent
3. **Correlation** - Wait for all, then analyze
4. **Visualization** - Generate plots
5. **Save Results** - CSV and images

## Performance Tips

- System runs faster without OpenAI API (no network calls)
- Large datasets may take longer for correlation analysis
- Visualizations are cached in memory before saving

## Next Steps

1. ✅ System converted to LangChain
2. ✅ All agents working correctly
3. ✅ Visualizations generated
4. ⭕ Add OpenAI API key for LLM insights
5. ⭕ Customize agent prompts
6. ⭕ Add new tools/agents
7. ⭕ Deploy to production

---

**Quick Start**: Just run `./ai_agents_env/bin/python main.py` and everything works! 🚀
