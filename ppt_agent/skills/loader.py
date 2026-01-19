"""Skill loader implementing progressive disclosure pattern.

This module provides the load_skill tool which acts as a gateway to
specialized skills. The actual skill implementations are stored in
external files and loaded on-demand, keeping the agent's context lean.
"""

from pathlib import Path
from langchain_core.tools import tool

# Path to skill definitions and scripts
SKILLS_DIR = Path(__file__).parent / "definitions"
SCRIPTS_DIR = Path(__file__).parent / "scripts"


@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt and make its capabilities available.

    This tool implements progressive disclosure - skills are loaded on-demand
    rather than being present in the agent's context upfront. This keeps the
    context window lean and allows for many specialized capabilities.

    Available skills:
    - powerpoint_creator: Expert at creating PowerPoint presentations with
      customization, formatting, and content generation capabilities

    Args:
        skill_name: Name of the skill to load

    Returns:
        The skill's specialized prompt, context, and available tools
    """
    skill_file = SKILLS_DIR / f"{skill_name}.txt"

    if not skill_file.exists():
        available = [f.stem for f in SKILLS_DIR.glob("*.txt")]
        return (
            f"Skill '{skill_name}' not found.\n\n"
            f"Available skills: {', '.join(available)}\n\n"
            f"Use load_skill with one of these names to activate that skill."
        )

    # Load the skill's specialized prompt from external file
    skill_content = skill_file.read_text()
    return skill_content
