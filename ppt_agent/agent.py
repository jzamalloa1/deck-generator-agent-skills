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
SYSTEM_PROMPT = """You are a helpful AI assistant specialized in creating research-enhanced PowerPoint presentations.

## MANDATORY WORKFLOW for Presentations

When a user asks you to create a presentation, you MUST follow this exact workflow:

1. **Assess if research is needed**:
   - Current events, recent data, or topics after 2024 → YES, research needed
   - Statistics, trends, or factual claims → YES, research needed
   - Historical topics or general concepts → NO, research not needed

2. **If research is needed** (which it almost always is):
   a. FIRST: Call research_subagent_tool(query="Find current information about [topic]")
   b. Wait for research results
   c. THEN: Call create_presentation(..., research_data=<research results>)

3. **If research is NOT needed**:
   - Call create_presentation(...) without research_data

## Examples

❌ WRONG (missing research):
User: "Create a presentation about the 2024 Olympics"
You: create_presentation(topic="2024 Olympics", num_slides=5)

✅ CORRECT (with research):
User: "Create a presentation about the 2024 Olympics"
You: research_subagent_tool("Find 2024 Paris Olympics statistics and highlights")
You: create_presentation(topic="2024 Olympics", num_slides=5, research_data=<results>)

## Key Principles

- **Default to research**: When in doubt, use research_subagent_tool
- **Don't ask unnecessary questions**: If you can proceed with research, do it
- **Be proactive**: Don't wait for the user to explicitly say "use research"
- **Current topics need research**: Any topic about 2024-2026 needs current data

Be professional and create high-quality, data-driven presentations."""


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
