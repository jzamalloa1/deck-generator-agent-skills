"""Test script to query the deployed LangGraph agent and capture debug output.

This script:
1. Connects to the local LangGraph server (http://localhost:2024)
2. Sends a test query to create a presentation with research
3. Streams the response from the agent
4. Displays the agent's output
5. Shows the run URL for trace inspection in LangSmith

The terminal output from the server will show [DEBUG] messages from create_presentation.py
"""

import asyncio
from langgraph_sdk import get_client


async def test_agent_query():
    """Test querying the agent with a presentation request that needs research."""

    # Connect to local LangGraph server
    client = get_client(url="http://localhost:2024")

    print("=" * 80)
    print("Testing LangGraph Agent Query")
    print("=" * 80)
    print(f"Server URL: http://localhost:2024")
    print(f"Agent: agent (from langgraph.json)")
    print("=" * 80)

    # Test query that should trigger research sub-agent and presentation creation
    test_query = "Create a presentation about the 2024 Paris Olympics with 5 slides. Include current statistics and key highlights."

    print(f"\n📝 Test Query:")
    print(f"   {test_query}")
    print("\n" + "=" * 80)
    print("Agent Response (streaming):")
    print("=" * 80 + "\n")

    try:
        # Stream the response from the agent
        async for chunk in client.runs.stream(
            thread_id=None,  # Threadless run (new conversation each time)
            assistant_id="agent",  # Assistant name from langgraph.json
            input={"messages": [{"role": "user", "content": test_query}]},
            stream_mode="updates"  # Stream updates as they happen
        ):
            # Print each chunk of the response
            if chunk.data:
                print(f"[CHUNK] {chunk.event}: {chunk.data}")

        print("\n" + "=" * 80)
        print("✓ Query completed successfully")
        print("=" * 80)

        print("\n📊 Check the terminal running 'uv run langgraph dev' for [DEBUG] messages")
        print("   These show whether research_data was passed to create_presentation")

        print("\n🔍 To inspect the full trace in LangSmith:")
        print("   1. Go to https://smith.langchain.com/")
        print("   2. Navigate to your project")
        print("   3. Find the latest run")
        print("   4. Inspect tool calls and their parameters")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Make sure 'uv run langgraph dev' is running on http://localhost:2024")
        return False

    return True


async def list_assistants():
    """List available assistants on the server."""
    client = get_client(url="http://localhost:2024")

    print("\n" + "=" * 80)
    print("Available Assistants:")
    print("=" * 80)

    try:
        assistants = await client.assistants.list()
        for assistant in assistants:
            print(f"  - {assistant['assistant_id']}")
    except Exception as e:
        print(f"❌ Error listing assistants: {e}")


async def main():
    """Main test function."""
    # List available assistants
    await list_assistants()

    print("\n")

    # Test the agent query
    success = await test_agent_query()

    if success:
        print("\n" + "=" * 80)
        print("Next Steps:")
        print("=" * 80)
        print("1. Check the server terminal for [DEBUG] output from create_presentation.py")
        print("2. Look for these debug messages:")
        print("   - [DEBUG] research_data received: True/False")
        print("   - [DEBUG] research_data length: <number>")
        print("   - [DEBUG] research_data preview: <content>")
        print("   - [DEBUG] research_bullets extracted: <count>")
        print("   - [DEBUG] Slide X - research_data exists: <True/False>")
        print("\n3. Open the generated PowerPoint file from ./output/ to verify content")
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
