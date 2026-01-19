# Migration Guide: Updated to LangChain 1.1+ and UV

This document explains what changed when migrating from the original StateGraph approach to the modern `create_agent` approach with UV package management.

## Summary of Changes

### Package Management
- **Before**: `requirements.txt` with pip
- **After**: `pyproject.toml` with UV support
- **Benefit**: 10-100x faster dependency installation

### Architecture
- **Before**: Manual StateGraph construction with custom nodes
- **After**: LangChain's `create_agent` function
- **Benefit**: Simpler code, easier maintenance, same capabilities

### Dependencies
- **LangChain**: 0.3.66 → >= 1.1.0
- **LangGraph**: 0.4.10 → >= 1.0.6
- **Model**: GPT-4o → gpt-5-nano ($0.05/1M input tokens)

## Files Changed

### Removed Files
1. `ppt_agent/utils/nodes.py` - Not needed (create_agent handles nodes)
2. `ppt_agent/utils/state.py` - Not needed (create_agent handles state)
3. `requirements.txt` - Replaced by pyproject.toml

### New Files
1. `pyproject.toml` - Modern Python project configuration

### Modified Files
1. `ppt_agent/agent.py` - Simplified to use create_agent
2. `ppt_agent/utils/__init__.py` - Updated imports
3. `README.md` - UV instructions and updated architecture
4. `QUICKSTART.md` - UV workflow
5. `CLAUDE.MD` - Updated tech stack and architecture
6. `verify_setup.py` - Updated validation checks

## Code Changes

### Before: agent.py (Manual StateGraph)

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from ppt_agent.utils.state import AgentState
from ppt_agent.utils.nodes import call_model, tool_node, should_continue

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"continue": "tools", "end": END},
)
workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
```

### After: agent.py (create_agent)

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from ppt_agent.utils.tools import create_powerpoint_deck, list_generated_presentations

SYSTEM_PROMPT = """You are a helpful AI assistant specialized in creating PowerPoint presentations."""

graph = create_agent(
    model="gpt-5-nano",
    tools=[create_powerpoint_deck, list_generated_presentations],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=MemorySaver(),
)
```

**Result**: 40% less code, same functionality!

## Setup Changes

### Before: pip workflow

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python test_agent.py
```

### After: UV workflow (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # Install UV once
uv sync                                          # Install deps
source .venv/bin/activate
uv run python test_agent.py
```

### After: pip workflow (Still Supported)

```bash
python -m venv venv
source venv/bin/activate
pip install -e .  # Note: Install from pyproject.toml, not requirements.txt
python test_agent.py
```

## Key Differences

### 1. State Management

**Before**: Manual TypedDict definition
```python
# ppt_agent/utils/state.py
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

**After**: Handled automatically by create_agent
- No state.py file needed
- create_agent uses default message state internally

### 2. Node Functions

**Before**: Manual node implementation
```python
# ppt_agent/utils/nodes.py
def call_model(state: AgentState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state: AgentState):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        # Execute tools...
    return {"messages": outputs}

def should_continue(state: AgentState):
    if state["messages"][-1].tool_calls:
        return "continue"
    return "end"
```

**After**: Built into create_agent
- No nodes.py file needed
- ReAct pattern implemented automatically

### 3. Model Configuration

**Before**: Manual binding
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [create_powerpoint_deck, list_generated_presentations]
model_with_tools = model.bind_tools(tools)
```

**After**: Simple string parameter
```python
graph = create_agent(
    model="gpt-5-nano",  # Just pass the model name
    tools=[create_powerpoint_deck, list_generated_presentations],
)
```

## Migration Checklist

If you're migrating an existing project:

- [ ] Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Create `pyproject.toml` with dependencies
- [ ] Update `agent.py` to use `create_agent`
- [ ] Remove `nodes.py` and `state.py` files
- [ ] Update imports in `utils/__init__.py`
- [ ] Delete `requirements.txt`
- [ ] Run `uv sync` to install dependencies
- [ ] Test with `uv run python test_agent.py`
- [ ] Update documentation

## Benefits of New Approach

1. **Simpler Code**: 40% reduction in boilerplate
2. **Faster Setup**: UV installs dependencies 10-100x faster
3. **Modern Stack**: LangChain 1.1+ and LangGraph 1.0+ stable releases
4. **Cost Effective**: GPT-5-nano costs 90% less than GPT-4o
5. **Same Power**: Still returns compiled LangGraph StateGraph
6. **Better DX**: Clearer abstractions, easier to understand

## Compatibility Notes

### What Stayed the Same
- Tools implementation (no changes to tools.py)
- LangGraph deployment compatibility
- LangSmith observability
- Checkpointing support
- LangGraph dev server usage

### What Changed
- Agent construction approach (manual → create_agent)
- Package management (pip → UV recommended)
- Model (GPT-4o → gpt-5-nano)
- Dependencies versions (0.x → 1.x stable)

## Troubleshooting

### "create_agent not found"
This is usually a stale cache issue:
```bash
rm -rf .venv
uv sync
```

### "UV command not found"
Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal
```

### Import errors after migration
Make sure to use the new package versions:
```bash
uv sync  # Installs from pyproject.toml
```

### Want to use pip instead of UV?
You can still use pip:
```bash
pip install -e .  # Reads from pyproject.toml
```

## Questions?

- Check `README.md` for full documentation
- See `QUICKSTART.md` for setup guide
- Review `CLAUDE.MD` for architecture details

## When to Use create_agent vs Manual StateGraph

### Use create_agent when:
- Building standard agent workflows
- You want less boilerplate
- ReAct pattern fits your needs
- Quick prototyping

### Use manual StateGraph when:
- Complex custom workflows needed
- Multiple agents with intricate routing
- Need full control over state transitions
- Advanced patterns beyond ReAct

**Good news**: You can mix both! create_agent returns a StateGraph that can be used inside larger custom workflows.
