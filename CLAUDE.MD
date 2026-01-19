# PowerPoint Deck Generator - Agentic Solution

## Project Overview
An agentic solution that automatically creates PowerPoint presentations based on user requests using LangChain's `create_agent` function (LangChain >= 1.1) built on LangGraph's modern architecture.

## Current Requirements
- Generate PowerPoint decks from natural language requests
- Agentic approach for autonomous deck creation using ReAct pattern
- LangSmith deployment-ready architecture
- Skill-based PowerPoint generation using @tool decorated functions
- UV package management for fast, reliable dependency resolution

## Tech Stack

### Package Management
- **UV**: Rust-powered package manager (10-100x faster than pip)
- **pyproject.toml**: Modern Python project configuration

### Core Framework
- **LangChain >= 1.1.0**: High-level agent abstraction with `create_agent` function
- **LangGraph >= 1.0.6**: Durable agent runtime (v1.0 stable release)
- **LangSmith >= 0.6.3**: Observability and deployment platform
- **Python >= 3.10**: Required Python version

### PowerPoint Generation
- **python-pptx >= 1.0.0**: PowerPoint file generation library

### LLM Provider
- **langchain-openai >= 0.3.0**: OpenAI integration
- **Model: gpt-5-nano**: Cost-effective GPT-5 model ($0.05/1M input tokens)

### Persistence (Production)
- **MemorySaver**: Development checkpointing
- **PostgreSQL Checkpointer**: Production durable execution (optional)

## Architecture

### High-Level Design

This project uses **LangChain's create_agent function** (introduced in LangChain 1.1), which provides a high-level abstraction for building agents while still leveraging LangGraph's powerful runtime underneath.

**Why create_agent?**
- Simpler API for standard agent workflows
- Built on LangGraph's StateGraph under the hood
- Returns a compiled StateGraph ready for deployment
- Implements proven ReAct pattern (Reasoning + Acting)
- Fully compatible with LangGraph deployment and observability

### Core Components

1. **Agent Creation** (`ppt_agent/agent.py`)
   - Uses `create_agent()` function from LangChain 1.1+
   - Returns a compiled LangGraph StateGraph
   - Configured with system prompt, tools, and checkpointer
   - No manual node/edge construction required

2. **PowerPoint Skills** (`ppt_agent/utils/tools.py`)
   - `create_powerpoint_deck`: Main presentation generation tool
   - `list_generated_presentations`: List created files
   - Implemented with @tool decorator
   - Type-hinted for automatic schema generation
   - Comprehensive docstrings for LLM understanding

3. **ReAct Pattern Flow**
   ```
   User Request → Agent (LLM reasoning with gpt-5-nano)
                     ↓
                  Tool Calls?
                     ↓
                  Execute Tools (create PowerPoint)
                     ↓
                  Agent (process results)
                     ↓
                  Response to User
   ```

### LangGraph Integration

Although we use `create_agent` for simplicity, it returns a **compiled LangGraph StateGraph**, which means:
- Full LangGraph deployment compatibility
- Checkpointing and durable execution support
- Human-in-the-loop capabilities
- LangSmith observability integration
- Can be composed with custom StateGraph workflows if needed

### Deployment Architecture
- **Development**: In-memory checkpointing, local testing
- **Production**: Optional PostgreSQL checkpointing, LangSmith deployment
- **Scaling**: Horizontal worker scaling via LangSmith

## Project Structure

```
ppt-agent/
├── ppt_agent/              # Main package
│   ├── utils/
│   │   ├── __init__.py
│   │   └── tools.py        # PowerPoint skills (@tool decorated)
│   ├── __init__.py
│   └── agent.py            # Agent creation with create_agent()
├── pyproject.toml          # UV package configuration
├── langgraph.json          # LangGraph deployment config
├── .env.template           # Environment variable template
├── .env                    # Local environment (gitignored)
├── README.md               # Project documentation
├── QUICKSTART.md           # Quick setup guide
└── CLAUDE.MD              # This file
```

**Note**: No `nodes.py` or `state.py` files needed - `create_agent` handles state management and node construction automatically.

## Features

### Phase 1: MVP ✅
- [x] UV package management setup
- [x] LangChain 1.1+ create_agent implementation
- [x] PowerPoint skill tools with @tool decorator
- [x] Basic deck generation (title, content slides)
- [x] LangSmith deployment configuration
- [x] GPT-5-nano model integration

### Phase 2: Enhanced Generation
- [ ] Custom themes and templates
- [ ] Image integration
- [ ] Chart and table generation
- [ ] Multi-slide content planning with AI
- [ ] Content research integration
- [ ] Template library

### Phase 3: Production Features
- [ ] PostgreSQL checkpointing
- [ ] Streaming responses
- [ ] Error handling and retry logic
- [ ] Human-in-the-loop approval workflow
- [ ] LangSmith observability dashboards
- [ ] Performance optimization

## Development Notes
- Project initialized: 2026-01-18
- Updated to UV + LangChain 1.1+ + create_agent: 2026-01-18
- Architecture based on LangChain 1.1 and LangGraph 1.0 stable releases
- Uses high-level `create_agent` abstraction for maintainability
- Built on LangGraph runtime for production-grade capabilities
- Designed for LangSmith deployment from day one

## Package Management with UV

### Why UV?
- **10-100x faster** than pip, Poetry, or Conda
- **Rust-powered** for reliability and speed
- **pyproject.toml** native support
- **Lockfile** generation for reproducible builds
- **Seamless** Python version management

### Common UV Commands
```bash
# Install dependencies
uv sync

# Add a new package
uv add package-name

# Add dev dependency
uv add --dev pytest

# Run Python with UV environment
uv run python script.py

# Create virtual environment
uv venv

# Lock dependencies
uv lock
```

## Deployment Strategy

### Local Development
```bash
# Using UV
uv sync
uv run python -m ppt_agent.agent  # Test agent

# Using LangGraph CLI
langgraph dev  # Runs on http://127.0.0.1:2024
```

### Production Deployment
1. Configure `langgraph.json` with graph reference
2. Set LangSmith environment variables
3. Deploy to LangSmith Cloud/Hybrid/Self-hosted
4. Monitor via LangSmith dashboards

## Model Selection: gpt-5-nano

**Why gpt-5-nano?**
- **Cost-effective**: $0.05/1M input tokens, $0.40/1M output tokens
- **Fast**: Optimized for quick responses
- **Capable**: Sufficient for task planning and tool calling
- **Released**: August 2025 as part of GPT-5 family

**Model Tiers**:
- `gpt-5`: Most capable, highest cost
- `gpt-5-mini`: Balanced performance and cost
- `gpt-5-nano`: **Fast and economical** ← We use this

## Next Steps
1. ✅ Define technology stack
2. ✅ Set up UV package management
3. ✅ Implement create_agent architecture
4. ✅ Create PowerPoint skill tools
5. Test locally with UV and langgraph dev
6. Add enhanced content generation features
7. Configure LangSmith production deployment

## Progressive Disclosure Pattern

This project implements **progressive disclosure** as recommended by LangChain for building scalable, context-efficient agents. This pattern is critical for maintaining lean agent contexts while providing powerful specialized capabilities.

### What is Progressive Disclosure?

Progressive disclosure means **loading specialized prompts and implementation code on-demand rather than upfront**. Instead of embedding all skill logic into the agent's system prompt and context, we use a lightweight gateway pattern that retrieves capabilities only when needed.

### Why Progressive Disclosure?

**Problem**: Traditional approaches load all tool implementations and specialized knowledge into the agent's context upfront, leading to:
- Bloated context windows
- Higher token costs
- Reduced focus and clarity
- Difficult to scale to many skills

**Solution**: Progressive disclosure keeps the agent's context lean by:
- Loading skills on-demand through a gateway tool
- Executing implementation code outside the agent's context
- Storing specialized prompts in external files
- Maintaining lightweight tool wrappers

### Architecture

#### Three-Layer Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Gateway Tool (Always in Agent Context)            │
│                                                             │
│ load_skill(skill_name: str) -> str                         │
│ - Lightweight (just reads a file)                          │
│ - Lists available skills in docstring                      │
│ - Acts as entry point to all skills                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Skill Definitions (Loaded On-Demand)              │
│                                                             │
│ skills/definitions/powerpoint_creator.txt                   │
│ - Specialized prompts and expertise                        │
│ - Context and guidelines for the skill                     │
│ - Information about available tools                        │
│ - NOT in agent context until loaded                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Implementation Scripts (Outside Context)          │
│                                                             │
│ skills/scripts/create_presentation.py                       │
│ - Actual implementation code (100+ lines)                  │
│ - Heavy business logic                                     │
│ - NEVER enters agent's context window                      │
│ - Called by lightweight tool wrappers                      │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Details

#### Directory Structure

```
ppt_agent/
├── skills/
│   ├── __init__.py                    # Exports load_skill
│   ├── loader.py                      # load_skill gateway tool
│   ├── README.md                      # Documentation
│   ├── definitions/                   # Skill prompts (on-demand)
│   │   └── powerpoint_creator.txt
│   └── scripts/                       # Implementations (external)
│       ├── create_presentation.py
│       └── list_presentations.py
└── utils/
    └── tools.py                       # Lightweight wrappers
```

#### Gateway Tool (load_skill)

```python
@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt.
    
    Available skills:
    - powerpoint_creator: Expert at creating PowerPoint presentations
    
    Returns the skill's specialized prompt and context.
    """
    skill_file = SKILLS_DIR / f"{skill_name}.txt"
    if not skill_file.exists():
        return f"Skill '{skill_name}' not found."
    
    # Load skill content from external file
    return skill_file.read_text()  # <-- This is the only time it enters context
```

**Key characteristics:**
- Always lightweight (< 20 lines)
- Lists available skills in docstring
- Reads from external files on-demand
- Returns specialized prompt to agent

#### Skill Definitions

File: `skills/definitions/powerpoint_creator.txt`

Contains:
- Role definition: "You are now a PowerPoint Presentation Creation Expert"
- Capabilities description
- Approach and guidelines
- List of available tools for this skill
- Best practices

**Loaded**: Only when `load_skill("powerpoint_creator")` is called
**Context cost**: ~500-1000 tokens (only when active)

#### Implementation Scripts

File: `skills/scripts/create_presentation.py`

Contains:
- Actual PowerPoint generation logic
- Validation and error handling
- File system operations
- Business logic (100+ lines)

**Loaded into context**: **NEVER**
**Executed**: Outside context by tool wrapper

#### Tool Wrappers

File: `utils/tools.py`

```python
from ppt_agent.skills.scripts.create_presentation import create_powerpoint

@tool
def create_presentation(topic: str, num_slides: int = 5, ...) -> str:
    """Create a PowerPoint presentation...
    
    [Docstring for LLM - describes parameters and behavior]
    """
    # Lightweight wrapper - just calls external script
    result = create_powerpoint(topic, num_slides, ...)
    return result["message"]
```

**Key characteristics:**
- Lightweight (< 10 lines of code)
- Rich docstring for LLM understanding
- Calls external implementation
- Implementation code never enters context

### Usage Flow

1. **User**: "Create a presentation about AI"
2. **Agent**: Calls `load_skill("powerpoint_creator")`
3. **load_skill**: Reads `definitions/powerpoint_creator.txt` and returns content
4. **Agent**: Now has specialized PowerPoint expertise in context
5. **Agent**: Calls `create_presentation(topic="AI", ...)`
6. **Tool wrapper**: Calls `scripts/create_presentation.py` (outside context)
7. **Script**: Executes PowerPoint generation, returns result
8. **Agent**: Receives result message and responds to user

### Benefits

1. **Lean Context**: Only active skills consume tokens
   - Base agent: ~200 tokens
   - With skill loaded: +500 tokens
   - Without progressive disclosure: +2000 tokens upfront

2. **Scalability**: Add unlimited skills
   - Each skill: ~500 tokens when loaded
   - 10 skills available, only 1 loaded: 200 + 500 = 700 tokens
   - Without progressive disclosure: 200 + (10 × 500) = 5,200 tokens

3. **Team Distribution**: Independent development
   - Team A: Works on PowerPoint skill
   - Team B: Works on PDF skill
   - No conflicts, no coordination overhead

4. **Maintainability**: Update skills without touching agent
   - Modify `definitions/powerpoint_creator.txt`
   - Update `scripts/create_presentation.py`
   - Agent code unchanged

5. **Flexibility**: Dynamic skill loading
   - Load "powerpoint_creator" for presentations
   - Load "data_analyst" for data tasks
   - Load "code_reviewer" for code analysis
   - Context adapts to current task

### Comparison: With vs Without Progressive Disclosure

#### Without Progressive Disclosure ❌

```python
SYSTEM_PROMPT = """You are a multi-skilled AI assistant.

**PowerPoint Creation**: [500 tokens of PowerPoint expertise]
**Data Analysis**: [500 tokens of data analysis expertise]
**Code Review**: [500 tokens of code review expertise]
**Document Processing**: [500 tokens of document expertise]
...

[All implementation details inline in tools.py: +2000 tokens]
"""

# Context cost: ~4,000 tokens ALWAYS
# Even if user only needs PowerPoint
```

#### With Progressive Disclosure ✅

```python
SYSTEM_PROMPT = """You are an AI assistant with access to skills.

Use load_skill tool to activate capabilities when needed.
"""

# Base context: ~200 tokens
# When user needs PowerPoint: load_skill adds +500 tokens
# Total: 700 tokens (83% reduction)
```

### Best Practices

1. **Keep Gateway Lightweight**: load_skill should be < 20 lines
2. **External Implementation**: Heavy code in scripts/
3. **Rich Docstrings**: Tool wrappers need good docs for LLM
4. **Clear Skill Definitions**: Make specialized prompts focused
5. **One Skill Per File**: Each skill gets own .txt file
6. **Descriptive Names**: Use clear skill names (powerpoint_creator, not ppt)

### Adding New Skills

See `ppt_agent/skills/README.md` for complete guide on adding new skills with progressive disclosure.

### References

- [LangChain Skills Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent/skills)
- [SQL Assistant Skills Example](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant)

