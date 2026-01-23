"""Minimal test agent to debug Studio connection."""

from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def test_tool(input: str) -> str:
    """A simple test tool."""
    return f"Test: {input}"

# Minimal agent configuration
graph = create_agent(
    model="gpt-5-nano",
    tools=[test_tool],
    system_prompt="You are a test assistant.",
)
