# Independent Testing Setup - Complete Guide

## Summary

You now have **3 automated testing scripts** that allow you to test the PowerPoint agent independently without manual interaction in LangSmith Studio.

## What We've Built

### 1. **test_agent_query.py** (Async + Streaming)
- Most comprehensive test script
- Streams agent responses in real-time
- Shows chunk-by-chunk updates
- Best for: Watching the agent think and act

### 2. **test_agent_simple.py** (Synchronous + Simple)
- ✅ **Easiest to use**
- Synchronous API (no async/await)
- Waits for completion and shows result
- Best for: Quick tests and debugging

### 3. **inspect_traces.py** (LangSmith API)
- Queries LangSmith for recent traces
- Shows tool calls with parameters
- Reveals if `research_data` was passed
- Best for: Deep debugging of tool interactions

## How to Use

### Quick Test (Recommended)

```bash
# In terminal where server is running, you'll see [DEBUG] output
# In another terminal, run:
uv run python test_agent_simple.py
```

**What happens:**
1. Script connects to `http://localhost:2024`
2. Sends query: "Create a presentation about 2024 Paris Olympics"
3. Agent processes request (may or may not use research)
4. Returns result with file path
5. **Server terminal shows [DEBUG] messages**

### Check Debug Output

In the server terminal, look for:
```
[DEBUG] research_data received: True/False  ← KEY FINDING
[DEBUG] research_data length: 0 or 1000+   ← KEY FINDING
[DEBUG] research_bullets extracted: X      ← KEY FINDING
```

### Current Findings from Debug Output

**Problem Confirmed**: `research_data received: False`

This means:
- ❌ Research sub-agent is NOT being called, OR
- ❌ Main agent IS calling research sub-agent but NOT passing results to `create_presentation`

**Next Step**: Use `inspect_traces.py` to see tool call sequence

## Complete Testing Workflow

### Step 1: Start Server (Terminal 1)
```bash
uv run langgraph dev
```
Keep this running - you'll see [DEBUG] output here.

### Step 2: Run Test (Terminal 2)
```bash
uv run python test_agent_simple.py
```

### Step 3: Check Debug Output (Terminal 1)
Look for `[DEBUG]` lines in server output.

### Step 4: Inspect Traces (Terminal 2)
```bash
uv run python inspect_traces.py
```

This shows:
- Which tools were called
- In what order
- With what parameters
- Whether `research_data` was passed

### Step 5: Check Output File
```bash
ls -la ./output/*.pptx
# Open the latest file
open ./output/2024_Paris_Olympics_*.pptx
```

## What Each Script Does

| Script | Purpose | Output Location |
|--------|---------|-----------------|
| `test_agent_simple.py` | Sends query to agent | Terminal 2 (script output) |
| `create_presentation.py` | Creates PowerPoint | Terminal 1 (server logs with [DEBUG]) |
| `inspect_traces.py` | Analyzes tool calls | Terminal 2 (trace analysis) |

## Expected vs Actual Behavior

### Expected (when working correctly):
1. Agent receives: "Create presentation about 2024 Olympics"
2. Agent thinks: "This needs current data"
3. Agent calls: `research_subagent_tool("2024 Olympics statistics")`
4. Research returns: "**Key Findings:** ..."
5. Agent calls: `create_presentation(topic="...", research_data="**Key Findings:...")`
6. Debug shows: `[DEBUG] research_data received: True, length: 1000+`
7. PowerPoint has: Real content in all slides

### Actual (current behavior):
1. Agent receives: "Create presentation about 2024 Olympics"
2. Agent calls: `create_presentation(topic="2024 Olympics")` **WITHOUT research_data**
3. Debug shows: `[DEBUG] research_data received: False, length: 0`
4. PowerPoint has: Placeholder content in slides 3+

## Root Cause Investigation

The debug output confirms the issue is **upstream** of the parsing logic:

- ✅ Parsing logic works (verified with `/tmp/test_research_parsing.py`)
- ❌ Research data is not being passed to the function
- ❓ Is research sub-agent being called at all?
- ❓ If called, are results being passed to `create_presentation`?

**Use `inspect_traces.py` to answer these questions.**

## Quick Reference Commands

```bash
# Start server (Terminal 1)
uv run langgraph dev

# Run simple test (Terminal 2)
uv run python test_agent_simple.py

# Inspect traces (Terminal 2)
uv run python inspect_traces.py

# Check latest PowerPoint
open ./output/*.pptx

# Tail server logs (Terminal 3, if needed)
tail -f <path-to-server-logs>

# Search for DEBUG in server output
# (In the terminal running langgraph dev, just scroll up or search)
```

## For More Details

See `TESTING.md` for comprehensive documentation on all testing methods, debugging workflows, and troubleshooting guides.

## Sources

- [LangGraph SDK Documentation](https://docs.langchain.com/langsmith/sdk)
- [Run a LangGraph app locally](https://docs.langchain.com/langsmith/local-server)
- [LangSmith Trace API](https://docs.smith.langchain.com/observability/how_to_guides/tracing/trace_with_api)
- [Trace with LangChain Python](https://docs.langchain.com/langsmith/trace-with-langchain)
