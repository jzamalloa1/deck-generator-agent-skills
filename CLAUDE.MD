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
- **Python >= 3.13**: Required Python version

### PowerPoint Generation
- **python-pptx >= 1.0.0**: PowerPoint file generation library

### Research & Web Search
- **langchain-tavily >= 0.2.0**: Official Tavily integration for LangChain
- **Tavily API**: AI-optimized search engine for LLM research tasks

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
   - Integrates research sub-agent as a tool

2. **Research Sub-Agent** (`ppt_agent/subagents/research_agent.py`) ✨ NEW
   - Independent agent with own context window
   - Uses Tavily search for current information gathering
   - Wrapped as `research_subagent_tool` for main agent
   - Returns synthesized research findings
   - Keeps main agent context lean through context isolation

3. **PowerPoint Skills** (`ppt_agent/utils/tools.py`)
   - `create_presentation`: Main presentation generation tool (supports research data)
   - `list_presentations`: List created files
   - Implemented with @tool decorator
   - Type-hinted for automatic schema generation
   - Comprehensive docstrings for LLM understanding

4. **Progressive Disclosure Skills** (`ppt_agent/skills/`)
   - `load_skill`: Gateway tool for on-demand skill loading
   - Skill definitions in `definitions/` (loaded when needed)
   - Implementation scripts in `scripts/` (executed outside context)

5. **Enhanced ReAct Pattern Flow**
   ```
   User Request → Agent (LLM reasoning with gpt-5-nano)
                     ↓
              Research Needed?
                     ↓
          Call Research Sub-Agent (Tavily search)
                     ↓
         Receive Research Findings (context isolation)
                     ↓
              Load PowerPoint Skill
                     ↓
    Execute Tools (create PowerPoint with research data)
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

## Sub-Agent Architecture

### Why Sub-Agents?

Sub-agents solve the **context bloat problem** that occurs when agents need to perform extensive research or exploration before generating final output. Without sub-agents, all intermediate tool calls (searches, data gathering, analysis) would fill up the main agent's context window, leading to:
- Wasted tokens on intermediate steps
- Reduced capacity for the actual task
- Higher costs
- Slower performance

### How Sub-Agents Work

**Context Isolation**: Sub-agents run with their own independent context window. The main agent only receives the final result, not the 20+ search calls that produced it.

**Workflow Example**:
```
Main Agent: "I need current AI statistics"
     ↓
Research Sub-Agent spawns with own context
     ↓
Sub-Agent makes 5 Tavily searches (in its own context)
Sub-Agent reads 10+ web pages (in its own context)
Sub-Agent synthesizes findings
     ↓
Main Agent receives: "Here are the key statistics..." (final summary only)
```

**Token Savings**:
- Without sub-agent: Main agent context includes all 15 search results (~10,000 tokens)
- With sub-agent: Main agent receives only final summary (~500 tokens)
- **Savings: 95% context reduction**

### Research Sub-Agent Details

**File**: `ppt_agent/subagents/research_agent.py`

**Purpose**: Gather current information from the internet using Tavily search

**Tools Available**:
- `TavilySearch`: AI-optimized search engine
  - Returns relevant results ranked by quality
  - Includes answer summaries
  - Provides image URLs for visual content
  - Supports general and news topics

**System Prompt**: Specialized for research synthesis
- Focus on current facts, statistics, and data
- Suggest visual content (charts, graphs, tables)
- Cite credible sources
- Provide structured output

**Usage Pattern**:
```python
# Main agent calls research sub-agent as a tool
research_subagent_tool("Find 2026 AI adoption trends and statistics")

# Sub-agent performs multiple searches internally
# Returns: Structured findings with data and visual suggestions
```

**Integration with PowerPoint**:
```python
# 1. Main agent determines research is needed
research = research_subagent_tool("Research electric vehicle market data")

# 2. Main agent passes findings to presentation tool
create_presentation(
    topic="EV Market Trends",
    num_slides=6,
    research_data=research  # Enriches presentation with current data
)
```

**Benefits**:
1. **Context Efficiency**: Main agent stays focused, sub-agent handles messy research
2. **Specialization**: Research sub-agent optimized for data gathering and synthesis
3. **Parallel Execution**: Could run multiple sub-agents simultaneously
4. **Modular Design**: Easy to add more sub-agents (PDF analysis, data viz, etc.)

## Project Structure

```
ppt-agent/
├── ppt_agent/                   # Main package
│   ├── subagents/              # Sub-agent implementations ✨ NEW
│   │   ├── __init__.py
│   │   └── research_agent.py   # Research sub-agent with Tavily search
│   ├── skills/                 # Progressive disclosure skills ✨ NEW
│   │   ├── __init__.py
│   │   ├── loader.py           # load_skill gateway tool
│   │   ├── definitions/        # Skill prompts (loaded on-demand)
│   │   │   └── powerpoint_creator.txt
│   │   └── scripts/            # Implementation (outside context)
│   │       ├── create_presentation.py
│   │       └── list_presentations.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── tools.py            # Lightweight tool wrappers
│   ├── __init__.py
│   └── agent.py                # Main agent with sub-agent integration
├── output/                     # Generated PowerPoint files
├── pyproject.toml              # UV package configuration
├── uv.lock                     # UV lockfile for reproducible builds
├── langgraph.json              # LangGraph deployment config
├── .env.template               # Environment variable template
├── .env                        # Local environment (gitignored)
├── README.md                   # Project documentation
├── QUICKSTART.md               # Quick setup guide
└── CLAUDE.MD                  # This file (architecture guide)
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
- [x] Progressive disclosure pattern for skills
- [x] Research sub-agent with Tavily integration ✨ NEW
- [x] Research-enhanced presentation creation ✨ NEW

### Phase 2: Enhanced Generation (In Progress)
- [x] Internet research integration via Tavily ✅
- [x] Research findings incorporated into presentations ✅
- [ ] Rich graphics: charts and tables from research data
- [ ] Custom themes and templates
- [ ] Image integration from research URLs
- [ ] Advanced chart generation (bar, line, pie charts)
- [ ] Table generation from structured data
- [ ] Multi-slide content planning with AI
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


## Skills vs Sub-Agents: When to Use Which?

Both skills (progressive disclosure) and sub-agents solve context management problems, but they serve different purposes:

### Skills (Progressive Disclosure)

**Purpose**: Load specialized expertise and prompts on-demand

**Use When**:
- You need specialized instructions or domain knowledge
- The agent needs to "become an expert" in a specific area
- You want to add behavioral guidance or best practices
- The capability is primarily **knowledge-based** rather than **action-heavy**

**Example**: PowerPoint creation skill
- Loads expert prompts about presentation structure
- Provides guidelines for slide organization
- Offers best practices for content creation
- Tells agent about available tools

**Characteristics**:
- Loaded as text into main agent's context
- Adds ~500-1000 tokens when activated
- No independent execution
- Primarily instructional/educational

### Sub-Agents (Context Isolation)

**Purpose**: Perform complex, multi-step tasks in isolation

**Use When**:
- Task requires many intermediate tool calls
- You need extensive exploration or research
- Results need synthesis from multiple sources
- The capability is primarily **action-heavy** rather than **knowledge-based**

**Example**: Research sub-agent
- Makes 5-10 Tavily search calls (in own context)
- Reads and processes multiple web pages
- Synthesizes findings into structured output
- Returns only final summary to main agent

**Characteristics**:
- Runs with independent context window
- Saves 90%+ tokens through context isolation
- Independent execution and reasoning
- Primarily action-oriented/computational

### Decision Matrix

| Scenario | Solution | Reason |
|----------|----------|--------|
| "Act like a presentation expert" | **Skill** | Need specialized knowledge/prompts |
| "Find current AI statistics" | **Sub-Agent** | Requires multiple searches and synthesis |
| "Follow these coding standards" | **Skill** | Behavioral guidelines |
| "Analyze this 50-page PDF" | **Sub-Agent** | Many read operations, context heavy |
| "Use formal business language" | **Skill** | Stylistic instructions |
| "Research and compare 5 products" | **Sub-Agent** | Extensive research with synthesis |

### Combining Both

The PowerPoint agent uses **both patterns together**:

1. **Skill**: `powerpoint_creator` provides presentation expertise
   - "You are now a PowerPoint expert. Use these guidelines..."

2. **Sub-Agent**: `research_subagent_tool` gathers current data
   - Main Agent → Research Sub-Agent (10 searches) → Final Summary

3. **Result**: Expert presentation creation with current, researched content
   - Skill (expertise) + Sub-Agent (data) = Research-Enhanced Presentations

### Architecture References

- [LangChain Multi-Agent Docs](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangChain Subagents Guide](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant)
- [Tavily LangChain Integration](https://docs.tavily.com/documentation/integrations/langchain)
