"""Quick test script for the PowerPoint agent.

This script demonstrates how to invoke the agent locally without
using the LangGraph dev server.
"""

from langchain_core.messages import HumanMessage
from ppt_agent.agent import graph


def test_agent(prompt: str):
    """Test the agent with a given prompt.

    Args:
        prompt: User request for PowerPoint generation
    """
    print(f"\n{'='*60}")
    print(f"Testing PowerPoint Agent")
    print(f"{'='*60}")
    print(f"\nUser Request: {prompt}")
    print(f"\n{'='*60}\n")

    # Create a thread configuration
    config = {"configurable": {"thread_id": "test-thread-1"}}

    # Invoke the agent
    result = graph.invoke(
        {"messages": [HumanMessage(content=prompt)]},
        config=config
    )

    # Print the response
    print("Agent Response:")
    print("-" * 60)
    for message in result["messages"]:
        if hasattr(message, "content"):
            print(f"{message.__class__.__name__}: {message.content}")
    print("-" * 60)

    return result


if __name__ == "__main__":
    # Example 1: Create a basic presentation
    test_agent("Create a 5-slide presentation about Python best practices")

    # Example 2: Custom parameters
    # test_agent("Generate a 3-slide deck about AI trends in 2026")

    # Example 3: List existing presentations
    # test_agent("List all the presentations you've created")
