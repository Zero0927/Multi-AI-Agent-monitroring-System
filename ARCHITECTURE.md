# LangChain Multi-Agent Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   MULTI-AI AGENT SYSTEM                     │
│            Powered by LangChain + LangGraph                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     AGENT CONFIGURATION                     │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   LLM      │  │   Prompts    │  │   Mock LLM       │   │
│  │ (GPT-4o)   │  │ (Specialized)│  │  (No API Key)    │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    LANGCHAIN TOOLS                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐   │
│  │ Productivity │ │  Sentiment   │ │   Compliance     │   │
│  │    Tools     │ │    Tools     │ │     Tools        │   │
│  │              │ │              │ │                  │   │
│  │ compute_TCR  │ │ compute_SPI  │ │  compute_DCR     │   │
│  │ get_data     │ │ get_data     │ │  get_data        │   │
│  └──────────────┘ └──────────────┘ └──────────────────┘   │
│  ┌──────────────┐ ┌──────────────┐                        │
│  │ Interaction  │ │ Correlation  │                        │
│  │    Tools     │ │    Tools     │                        │
│  │              │ │              │                        │
│  │ compute_CI   │ │ compute_OCS  │                        │
│  │ get_data     │ │ regression   │                        │
│  └──────────────┘ └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   LANGGRAPH WORKFLOW                        │
│                                                             │
│                       ┌─────────┐                          │
│                       │  START  │                          │
│                       └────┬────┘                          │
│                            │                               │
│         ┌─────────┬────────┼────────┬─────────┐           │
│         │         │        │        │         │           │
│         ▼         ▼        ▼        ▼         │           │
│   ┌──────────┐ ┌─────┐ ┌─────┐ ┌──────────┐  │           │
│   │Productiv.│ │Sent.│ │Comp.│ │Interact. │  │           │
│   │  Agent   │ │Agent│ │Agent│ │  Agent   │  │           │
│   │          │ │     │ │     │ │          │  │           │
│   │ Tools:   │ │Tools│ │Tools│ │ Tools:   │  │           │
│   │ - TCR    │ │-SPI │ │-DCR │ │ - CI     │  │           │
│   └────┬─────┘ └──┬──┘ └──┬──┘ └────┬─────┘  │           │
│        │          │       │         │         │           │
│        └──────────┴───────┴─────────┘         │           │
│                   │                            │           │
│                   ▼                            │           │
│             ┌────────────┐                     │           │
│             │Correlation │                     │           │
│             │   Agent    │                     │           │
│             │            │                     │           │
│             │  Tools:    │                     │           │
│             │  - OCS     │                     │           │
│             │  - Regress │                     │           │
│             │  - PCA     │                     │           │
│             └─────┬──────┘                     │           │
│                   │                            │           │
│                   ▼                            │           │
│               ┌───────┐                        │           │
│               │  END  │                        │           │
│               └───────┘                        │           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SHARED STATE                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  TCR, SPI, DCR, CI, OCS                             │  │
│  │  messages: List[AnyMessage]                          │  │
│  │  completed_agents: List[str]                         │  │
│  │  merged_data_path: str                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       OUTPUTS                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐   │
│  │  CSV Data    │ │  Dashboards  │ │  Individual      │   │
│  │              │ │              │ │  Plots           │   │
│  │ merged_      │ │ analysis.png │ │ productivity.png │   │
│  │ metrics.csv  │ │ radar.png    │ │ sentiment.png    │   │
│  │              │ │              │ │ ...6 plots       │   │
│  └──────────────┘ └──────────────┘ └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Input Data Files
     ↓
Agent-Specific Processing
     ↓
LangChain Tools
     ↓
Agent Executors (with LLM)
     ↓
Shared State Updates
     ↓
Correlation Analysis
     ↓
Visualization & Output
```

## Agent Communication Pattern

```
Agent 1 → Update State → Merge
Agent 2 → Update State → Merge  ┐
Agent 3 → Update State → Merge  ├→ Correlation Agent
Agent 4 → Update State → Merge  ┘
```

## Tool Invocation Flow

```
User Query
    ↓
Agent Executor
    ↓
LLM Reasoning (which tool to use?)
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Result to Agent
    ↓
Agent Response
    ↓
State Update
```

## Key Components Interaction

```
┌─────────────┐
│   main.py   │ ← Orchestrates workflow
└──────┬──────┘
       │
       ├─→ ┌─────────────────┐
       │   │ state_schema.py │ ← Defines shared state
       │   └─────────────────┘
       │
       ├─→ ┌─────────────────┐
       │   │ graph_nodes.py  │ ← Agent node implementations
       │   └─────────────────┘
       │        │
       │        ├─→ ┌──────────────────┐
       │        │   │ agent_config.py  │ ← LLM & Prompts
       │        │   └──────────────────┘
       │        │
       │        └─→ ┌──────────────────┐
       │            │ agent_tools.py   │ ← Tool definitions
       │            └──────────────────┘
       │                  │
       │                  └─→ ┌─────────────┐
       │                      │ agents/*.py │ ← Original logic
       │                      └─────────────┘
       │
       └─→ Results & Visualizations
```
