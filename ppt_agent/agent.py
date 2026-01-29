"""Main agent graph construction for PowerPoint generator.

This module builds the PowerPoint generation agent using LangChain's
create_agent function (available in LangChain >= 1.1.0).

The create_agent function returns a compiled LangGraph StateGraph that
implements the ReAct pattern (Reasoning + Acting) with automatic tool
execution and state management.

Environment variables are loaded from .env file in the project root.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

# Import progressive disclosure skill loader and presentation tools
from ppt_agent.skills import load_skill
from ppt_agent.utils.tools import create_presentation, list_presentations

# Import research sub-agent
from ppt_agent.subagents import research_subagent_tool


# Load environment variables from .env file
# Look for .env in project root (parent of ppt_agent directory)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✓ Loaded environment variables from: {env_path}")
else:
    print(f"⚠ Warning: .env file not found at {env_path}")
    print("  Create .env file from .env.template and add your API keys")


# System prompt that defines the agent's role and behavior
SYSTEM_PROMPT = """You are a helpful AI assistant specialized in creating research-enhanced PowerPoint presentations with rich visual content.

## MANDATORY WORKFLOW for ALL Presentations

When a user asks you to create a presentation, you MUST ALWAYS follow this workflow:

1. **ALWAYS Use Research** (for ANY topic):
   - Call research_subagent_tool(query="Find statistics, data, and facts about [topic]")
   - Research provides the numbers needed for charts, tables, and diagrams
   - Even for general topics, research makes presentations more compelling

2. **Research Query Requirements**:
   - ALWAYS request "statistics", "data", "numbers", "comparisons" in your query
   - Example: "Find statistics, medal counts, and participation data for 2024 Olympics"
   - Example: "Find market share data, growth statistics, and trends for AI industry"
   - The more specific numbers you request, the better the visuals

3. **Create Presentation with Research**:
   - ALWAYS call: create_presentation(..., research_data=<research results>)
   - NEVER call create_presentation without research_data
   - Research data automatically generates charts, tables, and diagrams

## Visual Content Requirements

ALL presentations MUST include:
- **Charts**: Bar charts or pie charts showing comparisons and distributions
- **Tables**: Summary statistics and structured data
- **Diagrams**: Visual representations of data (auto-generated from research)

The system automatically creates these visuals from research data that includes numbers.

## Examples

❌ WRONG (no research = no visuals):
User: "Create a presentation about AI"
You: create_presentation(topic="AI", num_slides=5)
Result: Text-only slides with no charts or tables

✅ CORRECT (research = automatic visuals):
User: "Create a presentation about AI"
You: research_subagent_tool("Find AI adoption statistics, market share data, and growth trends with specific numbers")
You: create_presentation(topic="AI", num_slides=5, research_data=<results>)
Result: Slides with bar charts, pie charts, tables, and rich visual content

## Key Principles

- **ALWAYS use research**: Every presentation needs research for visuals
- **Request numbers**: Always ask for "statistics", "data", "numbers" in research queries
- **Don't ask unnecessary questions**: Just proceed with research immediately
- **Visual-first mindset**: Presentations without charts/tables are incomplete

Be professional and create high-quality, data-driven, visually rich presentations."""


# Create the agent using create_agent function from LangChain 1.1+
# This returns a compiled StateGraph that can be used with LangGraph deployment
#
# IMPORTANT: Progressive Disclosure Pattern + Sub-Agent Architecture
# - load_skill: Lightweight gateway tool (loads specialized prompts on-demand)
# - create_presentation: Lightweight wrapper (calls external script)
# - list_presentations: Lightweight wrapper (calls external script)
# - research_subagent_tool: Wraps a sub-agent for internet research (Tavily search)
#
# The actual implementation code in skills/scripts/ stays outside the agent's context
# The research sub-agent runs with its own context window, keeping main agent lean
#
# NOTE: No checkpointer needed - LangGraph API handles persistence automatically
# For local testing without langgraph dev, you can add: checkpointer=MemorySaver()
graph = create_agent(
    model="gpt-5-nano",  # Using cost-effective GPT-5 nano model
    tools=[load_skill, create_presentation, list_presentations, research_subagent_tool],
    system_prompt=SYSTEM_PROMPT,
)


# Optional: Test the agent structure when run directly
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("PowerPoint Agent Configuration")
    print("=" * 70)
    print(f"Model: gpt-5-nano")
    print(f"Environment: {'Loaded from .env' if env_path.exists() else 'No .env found'}")
    print(f"\nTools (Progressive Disclosure + Sub-Agent Pattern):")
    print(f"  1. load_skill - Gateway to specialized skills")
    print(f"  2. research_subagent_tool - Research sub-agent (Tavily search)")
    print(f"  3. create_presentation - Creates PowerPoint files")
    print(f"  4. list_presentations - Lists created files")
    print(f"\nPersistence: Managed by LangGraph API")
    print("=" * 70)
    print("\n✓ Agent created successfully using LangChain's create_agent function")
    print("  Returns a compiled LangGraph StateGraph ready for deployment")
    print("\n✓ Progressive disclosure pattern implemented:")
    print("  - Skill implementations in skills/scripts/ (outside agent context)")
    print("  - Specialized prompts in skills/definitions/ (loaded on-demand)")
    print("  - Lightweight tool wrappers keep context lean")
    print("\n✓ Sub-agent architecture implemented:")
    print("  - Research sub-agent with Tavily search (independent context)")
    print("  - Main agent receives only final research summaries")
    print("  - Sub-agent keeps main context lean while providing rich data")
    print("\nReAct Pattern Flow:")
    print("  User → Agent → Research (optional) → Load Skill → Use Tools → Agent → Response")
    print("=" * 70 + "\n")
