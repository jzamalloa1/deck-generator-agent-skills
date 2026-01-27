"""Simple synchronous test script for querying the agent.

This is a simpler alternative to test_agent_query.py that uses
synchronous calls instead of async/await.
"""

from langgraph_sdk import get_sync_client


def test_agent():
    """Test the agent with a simple query."""

    print("=" * 80)
    print("Simple Agent Test (Synchronous)")
    print("=" * 80)

    # Connect to local server
    client = get_sync_client(url="http://localhost:2024")

    # Test query
    query = "Create a presentation about the 2024 Paris Olympics with 5 slides."

    print(f"\nQuery: {query}\n")
    print("=" * 80)
    print("Response:")
    print("=" * 80)

    try:
        # Create a thread
        thread = client.threads.create()
        print(f"Thread ID: {thread['thread_id']}")

        # Run the agent
        run = client.runs.create(
            thread_id=thread['thread_id'],
            assistant_id="agent",
            input={"messages": [{"role": "user", "content": query}]}
        )

        print(f"Run ID: {run['run_id']}")

        # Wait for completion and get result
        result = client.runs.join(thread_id=thread['thread_id'], run_id=run['run_id'])

        print("\nAgent Output:")
        print("-" * 80)

        # Extract messages from result
        if 'messages' in result:
            for msg in result['messages']:
                if msg.get('type') == 'ai':
                    print(msg.get('content', ''))

        print("\n" + "=" * 80)
        print("✓ Query completed")
        print("=" * 80)

        print("\n📊 Check server terminal for [DEBUG] messages")
        print(f"🔍 LangSmith trace: https://smith.langchain.com/")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Is 'uv run langgraph dev' running?")


if __name__ == "__main__":
    test_agent()
