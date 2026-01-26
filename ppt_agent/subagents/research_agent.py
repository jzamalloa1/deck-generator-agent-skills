"""Research sub-agent for gathering current information from the internet.

This sub-agent uses Tavily search to find recent, relevant information
that can enrich PowerPoint presentations with up-to-date facts, statistics,
and insights. The sub-agent runs with its own context window, keeping the
main agent's context lean.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver


# Load environment variables (same pattern as agent.py)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


# System prompt for the research sub-agent
RESEARCH_AGENT_PROMPT = """You are a research specialist focused on gathering accurate,
current information to support content creation.

## Your Role

You search the internet using Tavily to find:
- Recent facts, statistics, and data
- Current trends and developments
- Expert insights and industry information
- Visual content suggestions (charts, graphs, images)

## IMPORTANT: Search Efficiently

- **Make 1-3 targeted searches maximum** - Don't over-search
- Use broad queries that capture multiple aspects at once
- Stop searching once you have sufficient information
- Quality over quantity - a few good sources are better than many mediocre ones

## Your Approach

1. **Understand the Request**: Parse what information is needed
2. **Search Strategically**: Make 1-3 targeted Tavily searches (DO NOT search more than 3 times)
3. **Synthesize Results**: Combine findings into clear, usable insights immediately
4. **Suggest Visuals**: Recommend charts, tables, or images that would enhance the content
5. **Cite Sources**: Include URLs for fact-checking and credibility
6. **STOP**: Once you have key findings, STOP and provide your summary - do NOT continue searching

## Output Format

After your searches (max 3), immediately provide your research in this structure:

**Key Findings:**
- [Bullet points of important facts and data]

**Visual Suggestions:**
- [Specific recommendations for charts, tables, or graphics]
- [What data should be visualized and why]

**Sources:**
- [URLs of credible sources used]

Be efficient and focused. Make 1-3 searches, then immediately synthesize and respond. DO NOT make more than 3 searches."""


# Initialize Tavily search tool
tavily_search = TavilySearch(
    max_results=5,
    topic="general",  # Can be "general" or "news"
    include_answer=True,  # Get AI-generated answer
    include_raw_content=False,  # Don't include full page content (keep context lean)
    include_images=True,  # Include image URLs for visual content
)

# Create the research sub-agent using create_agent
# This returns a compiled StateGraph
research_subagent_graph = create_agent(
    model="gpt-5-nano",  # Use fast, cost-effective model for research
    tools=[tavily_search],
    system_prompt=RESEARCH_AGENT_PROMPT,
    checkpointer=MemorySaver(),  # Maintain conversation state within sub-agent
)


@tool
def research_subagent_tool(query: str) -> str:
    """Invoke the research sub-agent to gather current information from the internet.

    This tool spawns a specialized research agent that uses Tavily search to find
    recent, relevant information. Use this when creating presentations that would
    benefit from current facts, statistics, trends, or visual content suggestions.

    The sub-agent runs with its own context window, so the main agent only receives
    the final research summary, not all the intermediate search results. This keeps
    the main agent's context lean while still providing comprehensive research.

    Args:
        query: A clear description of what information to research.
               Examples:
               - "Find recent AI trends and adoption statistics for 2026"
               - "Research climate change impact data with chart suggestions"
               - "Get current market data for electric vehicles with graphs"

    Returns:
        A structured research summary including:
        - Key findings and data points
        - Visual content suggestions (charts, tables, images)
        - Source URLs for credibility

    Example:
        >>> research_subagent_tool("Find 2026 renewable energy statistics")
        '''
        **Key Findings:**
        - Solar energy capacity grew 45% in 2025-2026
        - Wind power accounts for 28% of US electricity

        **Visual Suggestions:**
        - Bar chart: Solar capacity growth 2020-2026
        - Pie chart: US energy mix breakdown

        **Sources:**
        - https://energy.gov/2026-renewable-report
        '''
    """
    # Invoke the sub-agent with the research query
    # The sub-agent will use Tavily search and return synthesized results
    # IMPORTANT: Set recursion_limit to prevent excessive searches
    # Formula: recursion_limit = 2 * max_tool_calls + 1
    # For 3 max searches: 2 * 3 + 1 = 7
    result = research_subagent_graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Make 1-3 targeted searches to research this topic, then immediately provide your structured findings:\n\n{query}\n\nRemember: Search efficiently (max 3 searches), then STOP and synthesize your findings."
                }
            ]
        },
        config={
            "configurable": {"thread_id": "research_subagent"},
            "recursion_limit": 15  # Allows ~7 tool calls max (2*7+1=15)
        }
    )

    # Extract the final message from the sub-agent
    # The result contains the full conversation, but we only want the final response
    messages = result.get("messages", [])

    if not messages:
        return "Error: No response from research sub-agent"

    # Get the last AI message
    final_message = messages[-1]

    # Return the content
    return final_message.content
