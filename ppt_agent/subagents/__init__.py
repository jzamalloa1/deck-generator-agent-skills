"""Sub-agents for specialized tasks.

This module contains sub-agent implementations that handle complex,
specialized tasks with their own context windows.
"""

from ppt_agent.subagents.research_agent import research_subagent_tool

__all__ = ["research_subagent_tool"]
