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
SYSTEM_PROMPT = """You are a helpful AI assistant with access to specialized skills.

## Your Approach

1. **Understand User Needs**: Listen carefully to what the user wants to accomplish
2. **Load Relevant Skills**: Use the load_skill tool to activate specialized capabilities when needed
3. **Use Tools Effectively**: Once a skill is loaded, use its associated tools to complete tasks
4. **Provide Clear Feedback**: Confirm actions and provide helpful information

## Available Skills

You have access to skills through the load_skill tool. When a user asks for something specific
(like creating presentations), load the appropriate skill first to gain specialized expertise.

## Progressive Disclosure

Skills are loaded on-demand to keep your context focused. Only load skills when you need them,
and they will provide you with specialized prompts and capabilities.

Be professional, helpful, and proactive in loading skills when tasks require specialized knowledge."""


# Create the agent using create_agent function from LangChain 1.1+
# This returns a compiled StateGraph that can be used with LangGraph deployment
#
# IMPORTANT: Progressive Disclosure Pattern
# - load_skill: Lightweight gateway tool (loads specialized prompts on-demand)
# - create_presentation: Lightweight wrapper (calls external script)
# - list_presentations: Lightweight wrapper (calls external script)
#
# The actual implementation code in skills/scripts/ stays outside the agent's context
#
# NOTE: No checkpointer needed - LangGraph API handles persistence automatically
# For local testing without langgraph dev, you can add: checkpointer=MemorySaver()
graph = create_agent(
    model="gpt-5-nano",  # Using cost-effective GPT-5 nano model
    tools=[load_skill, create_presentation, list_presentations],
    system_prompt=SYSTEM_PROMPT,
)


# Optional: Test the agent structure when run directly
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("PowerPoint Agent Configuration")
    print("=" * 70)
    print(f"Model: gpt-5-nano")
    print(f"Environment: {'Loaded from .env' if env_path.exists() else 'No .env found'}")
    print(f"\nTools (Progressive Disclosure Pattern):")
    print(f"  1. load_skill - Gateway to specialized skills")
    print(f"  2. create_presentation - Creates PowerPoint files")
    print(f"  3. list_presentations - Lists created files")
    print(f"\nPersistence: Managed by LangGraph API")
    print("=" * 70)
    print("\n✓ Agent created successfully using LangChain's create_agent function")
    print("  Returns a compiled LangGraph StateGraph ready for deployment")
    print("\n✓ Progressive disclosure pattern implemented:")
    print("  - Skill implementations in skills/scripts/ (outside agent context)")
    print("  - Specialized prompts in skills/definitions/ (loaded on-demand)")
    print("  - Lightweight tool wrappers keep context lean")
    print("\nReAct Pattern Flow:")
    print("  User → Agent → Load Skill → Use Tools → Agent → Response")
    print("=" * 70 + "\n")
