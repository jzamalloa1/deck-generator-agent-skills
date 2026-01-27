"""Tool wrappers implementing progressive disclosure pattern.

These are lightweight tool wrappers that call external script implementations.
The actual implementation code lives in ppt_agent/skills/scripts/ and is
executed outside the agent's context window, keeping it lean.

This follows LangChain's progressive disclosure best practice where tools
are lightweight dispatchers to external implementations.
"""

from langchain_core.tools import tool

# Import external script implementations (not loaded into agent context)
from ppt_agent.skills.scripts.create_presentation import create_powerpoint
from ppt_agent.skills.scripts.list_presentations import list_presentations


@tool
def create_presentation(
    topic: str,
    num_slides: int = 5,
    include_title_slide: bool = True,
    output_dir: str = "./output",
    research_data: str = None,
) -> str:
    """Create a PowerPoint presentation based on the specified topic and parameters.

    ⚠️ WORKFLOW REQUIREMENT:
    For topics about current events, recent data, statistics, or trends (like "2024 Olympics",
    "2026 AI trends", etc.), you MUST follow this workflow:

    1. FIRST: Call research_subagent_tool(query="...") to gather current information
    2. THEN: Call create_presentation(..., research_data=<result from step 1>)

    Without research_data, presentations about current topics will have placeholder content!

    This tool generates a complete PowerPoint deck with a title slide and content slides.
    If research_data is provided, the presentation will include a research findings slide
    and incorporate research insights into the content.

    Args:
        topic: The main topic or subject of the presentation.
               Example: "Introduction to Machine Learning" or "Q4 Sales Report"
        num_slides: Number of content slides to generate (excluding title slide if included).
                   Default is 5. Must be between 1 and 20.
        include_title_slide: Whether to include a dedicated title slide at the beginning.
                           Default is True.
        output_dir: Directory where the PowerPoint file will be saved.
                   Default is "./output". Directory will be created if it doesn't exist.
        research_data: Optional research findings from research_subagent_tool to incorporate
                      into the presentation. When provided, creates a research findings slide
                      and enriches content with current data.

    Returns:
        A string message indicating the file path where the presentation was saved,
        or an error message if generation failed.

    Example:
        >>> # Without research
        >>> create_presentation("AI Trends 2026", num_slides=6)
        "PowerPoint presentation created successfully: ./output/AI_Trends_2026_20260118_143022.pptx"

        >>> # With research
        >>> research = research_subagent_tool("Find 2026 AI adoption statistics")
        >>> create_presentation("AI Trends 2026", num_slides=6, research_data=research)
        "PowerPoint presentation created successfully (research-enhanced): ./output/AI_Trends_2026_20260118_143022.pptx"
    """
    # Call external implementation script (code stays outside agent context)
    result = create_powerpoint(
        topic=topic,
        num_slides=num_slides,
        include_title_slide=include_title_slide,
        output_dir=output_dir,
        research_data=research_data,
    )

    return result["message"]


@tool
def list_presentations(output_dir: str = "./output") -> str:
    """List all PowerPoint presentations that have been generated in the output directory.

    Args:
        output_dir: Directory to search for presentations. Default is "./output".

    Returns:
        A formatted string listing all .pptx files found, or a message if none exist.
    """
    # Call external implementation script (code stays outside agent context)
    result = list_presentations(output_dir=output_dir)

    return result["message"]
