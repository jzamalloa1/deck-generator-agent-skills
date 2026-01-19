# Quick Start Guide

Get your PowerPoint agent up and running in 5 minutes using UV or pip.

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- LangSmith API key (optional for local development)

## Setup Steps

### 1. Install UV (Recommended)

UV is 10-100x faster than pip:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Setup with UV (Recommended)

```bash
# Navigate to project directory
cd ppt-agent

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Alternative: Setup with pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install from pyproject.toml
pip install -e .
```

### 3. Configure Environment

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your API keys
```

Your `.env` should look like:
```env
OPENAI_API_KEY=sk-...your-key-here...
LANGSMITH_API_KEY=lsv2_pt_...your-key-here...
LANGSMITH_TRACING=true
```

### 4. Test Locally (Option A: Python Script)

```bash
# With UV
uv run python test_agent.py

# Without UV
python test_agent.py
```

This will create a test presentation in the `output/` directory.

### 5. Run with LangGraph Dev Server (Option B: Recommended)

```bash
langgraph dev
# Runs on http://127.0.0.1:2024
```

#### Test with curl:

```bash
curl -X POST http://127.0.0.1:2024/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{
      "role": "user",
      "content": "Create a 5-slide presentation about Machine Learning"
    }]
  }'
```

#### Test with Python SDK:

```python
from langgraph_sdk import get_client

client = get_client(url="http://127.0.0.1:2024")
thread = client.threads.create()

response = client.runs.create(
    thread["thread_id"],
    "agent",
    input={
        "messages": [{
            "role": "user",
            "content": "Create a presentation about Python"
        }]
    }
)
print(response)
```

## Project Structure

```
.
├── ppt_agent/              # Main package
│   ├── __init__.py
│   ├── agent.py           # create_agent() implementation ⭐
│   └── utils/
│       ├── __init__.py
│       └── tools.py       # PowerPoint generation tools
├── pyproject.toml         # UV/pip package config
├── langgraph.json         # LangGraph deployment config
├── .env.template          # Environment template
├── .env                   # Your local config (create this)
├── test_agent.py          # Quick test script
├── README.md              # Full documentation
└── CLAUDE.MD             # Design document
```

## Key Files Explained

### `ppt_agent/agent.py`
Uses LangChain's `create_agent()` function to build the agent. This returns a compiled LangGraph StateGraph ready for deployment.

### `ppt_agent/utils/tools.py`
Contains PowerPoint generation skills:
- `create_powerpoint_deck`: Main tool for creating presentations
- `list_generated_presentations`: Lists created files

### `pyproject.toml`
Modern Python package configuration for UV and pip:
```toml
[project]
dependencies = [
    "langchain>=1.1.0",
    "langgraph>=1.0.6",
    "langchain-openai>=0.3.0",
    "python-pptx>=1.0.0",
]
```

### `langgraph.json`
Tells LangGraph where to find your graph:
```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./ppt_agent/agent.py:graph"
  },
  "env": ".env"
}
```

## Common Commands

### With UV (Recommended)

```bash
# Install dependencies
uv sync

# Run test
uv run python test_agent.py

# Start dev server
langgraph dev

# Add a package
uv add package-name

# Update dependencies
uv lock --upgrade
```

### Without UV

```bash
# Install dependencies
pip install -e .

# Run test
python test_agent.py

# Start dev server
langgraph dev
```

## Verify Installation

```bash
# Check Python version
python --version  # Should be 3.10+

# Check UV (if using)
uv --version

# Verify agent imports
uv run python -c "from ppt_agent.agent import graph; print('✓ Agent imports successfully')"

# Or without UV
python -c "from ppt_agent.agent import graph; print('✓ Agent imports successfully')"
```

## Troubleshooting

### "uv: command not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal
```

### "No module named 'ppt_agent'"
```bash
# Make sure you're in project root
pwd  # Should show .../ppt-agent or .../claude_code_desktop_test

# Reinstall
uv sync  # or pip install -e .
```

### "OpenAI API key not found"
- Check that `.env` file exists
- Verify it contains `OPENAI_API_KEY=sk-...`
- Ensure `.env` is in the same directory as `langgraph.json`

### "create_agent not found"
```bash
# This is usually a stale cache - remove and reinstall
rm -rf .venv
uv sync
```

### Import errors
```bash
# With UV
rm -rf .venv
uv sync

# Without UV
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Architecture Overview

The agent uses LangChain's `create_agent` function (LangChain 1.1+):

```
User → create_agent (ReAct pattern) → Tool (creates PPT) → Response → User
```

Internally:
1. User sends a message
2. `create_agent` invokes GPT-5-nano for reasoning
3. LLM decides to call `create_powerpoint_deck` tool
4. Tool executes PowerPoint generation
5. Results go back to LLM
6. LLM formats final response to user

**Key Point**: `create_agent` returns a **compiled LangGraph StateGraph**, giving you the best of both worlds:
- Simple, high-level API for development
- Production-grade LangGraph runtime for deployment

## Example Prompts to Try

```
"Create a 5-slide presentation about Python best practices"

"Generate a pitch deck with 6 slides"

"Make a presentation about AI trends in 2026"

"List all presentations you've created"
```

## What's Different from Old Approaches?

### ✅ This Project (Modern)
- Uses `create_agent` from LangChain 1.1+
- No manual node/edge construction
- Built on LangGraph 1.0 stable
- UV for fast package management
- GPT-5-nano for cost savings

### ❌ Old Approaches (Deprecated)
- Manual StateGraph construction with nodes.py
- `create_react_agent` from langgraph.prebuilt (deprecated)
- requirements.txt instead of pyproject.toml
- Older LangChain/LangGraph versions

## Next Steps

1. ✅ Get the agent running
2. Modify `ppt_agent/utils/tools.py` to customize PowerPoint generation
3. Add more tools for enhanced functionality
4. Deploy to LangSmith for production

## Resources

- [Full README](./README.md)
- [Design Doc](./CLAUDE.MD)
- [LangChain Docs](https://docs.langchain.com/oss/python/langchain/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [UV Docs](https://docs.astral.sh/uv/)
- [LangSmith](https://smith.langchain.com)
