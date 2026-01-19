# PowerPoint Deck Generator Agent

An intelligent agentic system built with **LangChain 1.1+** and **LangGraph 1.0+** that automatically generates PowerPoint presentations based on natural language requests.

## 🎯 Overview

This project implements a production-ready agent using LangChain's `create_agent` function, which provides a high-level abstraction for building agents while leveraging LangGraph's powerful runtime underneath. The agent uses GPT-5-nano for cost-effective reasoning and tool calling.

## ✨ Features

- **Natural Language Processing**: Understands user requests for presentation creation
- **Autonomous Generation**: Creates complete PowerPoint decks with minimal input
- **Modern Architecture**: Uses LangChain 1.1+ `create_agent` (not deprecated patterns)
- **Cost-Effective**: GPT-5-nano model ($0.05/1M input tokens)
- **Fast Package Management**: UV for 10-100x faster dependency resolution
- **Production Ready**: Built with LangGraph runtime for durable execution
- **LangSmith Deployable**: Configured for seamless deployment

## 🏗️ Architecture

### LangChain create_agent Pattern

This project uses **create_agent** from LangChain 1.1+, which:
- Returns a compiled LangGraph StateGraph
- Implements the ReAct pattern (Reasoning + Acting) automatically
- Handles state management and tool execution
- Provides full LangGraph deployment compatibility

```
User Request → Agent (GPT-5-nano reasoning)
                    ↓
              Tool Calls Detected?
                    ↓
            Execute PowerPoint Tools
                    ↓
            Agent Processes Results
                    ↓
            Response to User
```

### Key Components

1. **Agent Creation**: Uses `create_agent()` with tools and system prompt
2. **PowerPoint Tools**: `@tool` decorated functions for deck generation
3. **LangGraph Runtime**: Durable execution with checkpointing
4. **LangSmith Integration**: Observability and deployment

## 📋 Prerequisites

- Python >= 3.10
- UV package manager (recommended) or pip
- OpenAI API key (for GPT-5-nano)
- LangSmith API key (for deployment and observability)

## 🚀 Quick Start

### 1. Install UV (Recommended)

UV is a Rust-powered package manager that's 10-100x faster than pip:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Setup Project with UV

```bash
# Clone/navigate to project directory
cd ppt-agent

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Alternative Setup with pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies from pyproject.toml
pip install -e .
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env and add your API keys
# Required: OPENAI_API_KEY
# Optional: LANGSMITH_API_KEY (for observability)
```

Your `.env` should contain:
```env
OPENAI_API_KEY=sk-...your-key-here...
LANGSMITH_API_KEY=lsv2_pt_...your-key-here...
LANGSMITH_TRACING=true
```

### 5. Test the Agent

#### Option A: Run with UV

```bash
uv run python test_agent.py
```

#### Option B: Use LangGraph Dev Server

```bash
langgraph dev
# Server runs on http://127.0.0.1:2024
```

Test with curl:
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

## 📁 Project Structure

```
ppt-agent/
├── ppt_agent/              # Main application package
│   ├── utils/
│   │   ├── __init__.py
│   │   └── tools.py        # PowerPoint generation tools
│   ├── __init__.py
│   └── agent.py            # Agent creation with create_agent()
├── pyproject.toml          # UV/pip package configuration
├── langgraph.json          # LangGraph deployment config
├── .env.template           # Environment variable template
├── .env                    # Local environment (gitignored)
├── test_agent.py           # Quick test script
├── README.md               # This file
├── QUICKSTART.md           # 5-minute setup guide
└── CLAUDE.MD              # Design documentation
```

**Note**: No manual `nodes.py` or `state.py` files - `create_agent` handles this automatically.

## 🛠️ Development

### UV Package Management Commands

```bash
# Install dependencies
uv sync

# Add a new package
uv add package-name

# Add development dependency
uv add --dev pytest

# Run Python with UV environment
uv run python script.py

# Update dependencies
uv lock --upgrade

# Remove a package
uv remove package-name
```

### Adding New Tools/Skills

To add a new skill to the agent:

1. Create a tool function in `ppt_agent/utils/tools.py`:

```python
from langchain_core.tools import tool

@tool
def my_new_skill(param: str) -> str:
    """Description of what this skill does.

    Args:
        param: Description of the parameter
    """
    # Implementation here
    return "result"
```

2. Add the tool to the agent in `ppt_agent/agent.py`:

```python
from ppt_agent.utils.tools import create_powerpoint_deck, my_new_skill

graph = create_agent(
    model="gpt-5-nano",
    tools=[create_powerpoint_deck, my_new_skill],  # Add your tool here
    system_prompt=SYSTEM_PROMPT,
)
```

### Testing

Test individual tools directly:

```python
from ppt_agent.utils.tools import create_powerpoint_deck

result = create_powerpoint_deck.invoke({
    "topic": "Test Presentation",
    "num_slides": 3
})
print(result)
```

## 🚢 Deployment

### Deploy to LangSmith

1. **Set up credentials**:
```bash
export LANGSMITH_API_KEY=your_key_here
```

2. **Configure langgraph.json** (already configured):
```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./ppt_agent/agent.py:graph"
  },
  "env": ".env"
}
```

3. **Deploy**:
   - **Cloud**: Push to connected git repository
   - **Self-hosted**: Build Docker image and deploy

4. **Monitor**: Use LangSmith dashboard for observability

### Production Configuration

For production deployments, consider:

1. **PostgreSQL Checkpointer** for durable execution:
```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@host:5432/db"
)

graph = create_agent(
    model="gpt-5-nano",
    tools=[...],
    checkpointer=checkpointer,
)
```

2. **Environment variables** for production settings
3. **Horizontal scaling** via LangSmith
4. **Monitoring and alerts** through LangSmith dashboard

## 📊 Monitoring and Observability

With LangSmith integration, you get:

- **Trace Visualization**: See every step of agent execution
- **Performance Metrics**: Latency, token usage, success rates
- **Debugging Tools**: Inspect state and tool calls
- **Alerts**: Get notified of errors or anomalies

Access traces at: https://smith.langchain.com

## 🔧 Configuration

### pyproject.toml

Modern Python project configuration with UV support:

```toml
[project]
name = "ppt-agent"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "langchain>=1.1.0",
    "langgraph>=1.0.6",
    "langchain-openai>=0.3.0",
    "python-pptx>=1.0.0",
]
```

### langgraph.json

LangGraph deployment configuration:

```json
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./ppt_agent/agent.py:graph"
  },
  "env": ".env"
}
```

## 📝 Usage Examples

### Example 1: Basic Presentation

```python
"Create a 5-slide presentation about machine learning basics"
```

### Example 2: Specific Structure

```python
"Generate a pitch deck with 6 slides about a new SaaS product"
```

### Example 3: List Presentations

```python
"Show me all the presentations you've created"
```

## 💡 Why This Stack?

### LangChain 1.1+ create_agent
- **High-level abstraction** for quick development
- **Built on LangGraph** for production-grade runtime
- **Proven ReAct pattern** implementation
- **Easy to understand and maintain**

### LangGraph 1.0+
- **Stable v1.0 release** (October 2025)
- **Durable execution** with checkpointing
- **Production-ready** with proven track record
- **Seamless deployment** to LangSmith

### UV Package Manager
- **10-100x faster** than pip
- **Rust-powered** for reliability
- **Reproducible builds** with lockfile
- **Modern Python tooling**

### GPT-5-nano
- **Cost-effective**: $0.05/1M input tokens
- **Fast**: Optimized for quick responses
- **Capable**: Sufficient for agent reasoning

## 🤝 Contributing

To extend this project:

1. Add new tools in `utils/tools.py` with `@tool` decorator
2. Update agent in `agent.py` to include new tools
3. Test locally with `uv run python test_agent.py`
4. Update documentation

## 📚 Resources

- [LangChain 1.0 Documentation](https://docs.langchain.com/oss/python/langchain/)
- [LangGraph 1.0 Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Deployment](https://docs.langchain.com/langsmith/deployments)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)

## 🐛 Troubleshooting

### UV Issues

**Issue**: `uv: command not found`
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Issue**: Package conflicts
```bash
# Remove .venv and reinstall
rm -rf .venv
uv sync
```

### API Key Errors

- Ensure `.env` file exists with valid keys
- Check that `.env` is referenced in `langgraph.json`
- Verify OPENAI_API_KEY format: `sk-...`

### Import Errors

**Issue**: `create_agent` not found
```bash
# This is usually a cache issue - reinstall
rm -rf .venv
uv sync
```

**Issue**: Module not found
```bash
# Ensure you're in virtual environment
source .venv/bin/activate  # UV
# or
source venv/bin/activate   # pip

# Reinstall
uv sync  # or pip install -e .
```

### Graph Compilation Errors

- Check that `graph` variable is exported in `agent.py`
- Verify `langgraph.json` points to correct module path
- Ensure all imports are correct

## 📧 Support

For issues or questions:
- Check `QUICKSTART.md` for setup guide
- Review `CLAUDE.MD` for architecture details
- See LangChain/LangGraph official documentation
- LangSmith support channels

## 📄 License

MIT License - See LICENSE file for details
