"""Script to inspect LangSmith traces programmatically.

This script uses the LangSmith Python SDK to query and display
traces from recent agent runs, showing tool calls and parameters.
"""

import os
from datetime import datetime, timedelta
from langsmith import Client


def inspect_recent_traces(limit=5):
    """Inspect recent traces from LangSmith."""

    print("=" * 80)
    print("LangSmith Trace Inspector")
    print("=" * 80)

    # Initialize LangSmith client
    # Reads LANGSMITH_API_KEY from environment
    try:
        client = Client()
        print(f"✓ Connected to LangSmith")
    except Exception as e:
        print(f"❌ Error connecting to LangSmith: {e}")
        print("   Make sure LANGSMITH_API_KEY is set in .env")
        return

    print(f"\n📊 Fetching last {limit} runs...")
    print("=" * 80)

    try:
        # Get recent runs from the project
        # Filter for runs from the last hour
        runs = client.list_runs(
            project_name=os.getenv("LANGSMITH_PROJECT", "default"),
            limit=limit,
            start_time=datetime.now() - timedelta(hours=1)
        )

        for i, run in enumerate(runs, 1):
            print(f"\n{i}. Run ID: {run.id}")
            print(f"   Name: {run.name}")
            print(f"   Start Time: {run.start_time}")
            print(f"   Status: {run.status}")

            # Show inputs
            if run.inputs:
                print(f"   Inputs:")
                for key, value in run.inputs.items():
                    print(f"      {key}: {str(value)[:100]}...")

            # Show outputs
            if run.outputs:
                print(f"   Outputs:")
                for key, value in run.outputs.items():
                    print(f"      {key}: {str(value)[:100]}...")

            # Show tool calls if this is a tool run
            if run.run_type == "tool":
                print(f"   Tool: {run.name}")
                if run.inputs:
                    print(f"   Tool Inputs:")
                    for key, value in run.inputs.items():
                        if key == "research_data" and value:
                            print(f"      research_data: [LENGTH: {len(str(value))} chars]")
                            print(f"      research_data (preview): {str(value)[:200]}...")
                        else:
                            print(f"      {key}: {value}")

            print(f"   URL: {run.url}")
            print("-" * 80)

        print("\n" + "=" * 80)
        print("Trace Inspection Tips:")
        print("=" * 80)
        print("1. Look for 'create_presentation' tool calls")
        print("2. Check if 'research_data' parameter has content")
        print("3. Verify 'research_subagent_tool' was called before create_presentation")
        print("4. Click the URL to see full trace in LangSmith UI")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error fetching runs: {e}")


def find_presentation_tool_calls(limit=20):
    """Find and display create_presentation tool calls specifically."""

    print("\n" + "=" * 80)
    print("Searching for create_presentation Tool Calls")
    print("=" * 80)

    try:
        client = Client()

        # Get recent runs
        runs = client.list_runs(
            project_name=os.getenv("LANGSMITH_PROJECT", "default"),
            limit=limit,
            start_time=datetime.now() - timedelta(hours=2)
        )

        found_any = False
        for run in runs:
            if run.name == "create_presentation":
                found_any = True
                print(f"\n✓ Found create_presentation call")
                print(f"   Run ID: {run.id}")
                print(f"   Time: {run.start_time}")

                if run.inputs:
                    print(f"   Parameters:")
                    for key, value in run.inputs.items():
                        if key == "research_data":
                            if value:
                                print(f"      ✓ research_data: PROVIDED (length: {len(str(value))})")
                                print(f"        Preview: {str(value)[:200]}...")
                            else:
                                print(f"      ✗ research_data: None or empty")
                        else:
                            print(f"      {key}: {value}")

                print(f"   Trace: {run.url}")
                print("-" * 80)

        if not found_any:
            print("\n❌ No create_presentation tool calls found in recent runs")
            print("   Run test_agent_query.py first to generate traces")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Inspect recent traces
    inspect_recent_traces(limit=10)

    # Focus on create_presentation calls
    find_presentation_tool_calls(limit=30)
