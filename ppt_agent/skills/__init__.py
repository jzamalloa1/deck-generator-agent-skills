"""Skills module with progressive disclosure pattern.

Skills are loaded on-demand to avoid bloating the agent's context window.
Only the lightweight load_skill tool is registered with the agent upfront.
"""

from .loader import load_skill

__all__ = ["load_skill"]
