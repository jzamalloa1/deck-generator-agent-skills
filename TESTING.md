# Testing the PowerPoint Agent

This document explains how to test the LangGraph PowerPoint agent independently, including programmatic queries, debug output inspection, and trace analysis.

## Prerequisites

1. **Server Running**: Ensure the LangGraph development server is running:
   ```bash
   uv run langgraph dev
   ```
   This starts the server at `http://localhost:2024`

2. **Environment Variables**: Make sure `.env` file has:
   - `OPENAI_API_KEY` - For GPT model access
   - `TAVILY_API_KEY` - For research sub-agent
   - `LANGSMITH_API_KEY` - For trace inspection (optional)

## Testing Methods

### Method 1: Interactive Testing (LangSmith Studio)

**Best for**: Manual testing and visual debugging

1. Server automatically opens LangSmith Studio at:
   ```
   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
   ```

2. Test queries to try:
   ```
   Create a presentation about the 2024 Paris Olympics with 5 slides
   ```

3. Check server terminal for `[DEBUG]` messages showing:
   - `[DEBUG] research_data received: True/False`
   - `[DEBUG] research_data length: <number>`
   - `[DEBUG] research_data preview: <content>`
   - `[DEBUG] research_bullets extracted: <count>`
   - `[DEBUG] Slide X - research_data exists: True/False`

### Method 2: Programmatic Testing (Async)

**Best for**: Automated testing with full control

```bash
uv run python test_agent_query.py
```

**What it does**:
- Connects to local LangGraph server
- Sends test query to create presentation with research
- Streams agent response in real-time
- Shows run URL for trace inspection

**Output**: Agent response + instructions for checking debug logs

### Method 3: Simple Synchronous Testing

**Best for**: Quick tests without async complexity

```bash
uv run python test_agent_simple.py
```

**What it does**:
- Synchronous API calls (no async/await)
- Creates a thread and runs the agent
- Waits for completion and displays result
- Simpler code, easier to understand

### Method 4: Trace Inspection

**Best for**: Debugging tool calls and parameter passing

```bash
uv run python inspect_traces.py
```

**What it does**:
- Connects to LangSmith API
- Fetches recent traces (last 1-2 hours)
- Displays tool calls with parameters
- **Shows whether `research_data` was passed to `create_presentation`**
- Provides URLs to full traces in LangSmith UI

**Key Information**:
- Lists all recent runs with inputs/outputs
- Specifically searches for `create_presentation` tool calls
- Checks if `research_data` parameter has content
- Shows preview of `research_data` content

## Debug Output Analysis

### What to Look For

When you run tests, check the server terminal for debug messages:

1. **Research Data Received**:
   ```
   [DEBUG] research_data received: True
   [DEBUG] research_data length: 1234
   [DEBUG] research_data preview (first 200 chars): **Key Findings:**
   - The 2024 Paris Olympics featured over 10,500 athletes...
   ```

2. **Parsing Results**:
   ```
   [DEBUG] research_bullets extracted: 8 bullets
   [DEBUG] First 3 bullets: ['The 2024 Paris Olympics featured...', 'Breaking made...', 'Record 329...']
   ```

3. **Slide Content Decision**:
   ```
   [DEBUG] Slide 1 - research_data exists: True, research_bullets count: 8
   [DEBUG] Slide 2 - research_data exists: True, research_bullets count: 8
   [DEBUG] Slide 3 - research_data exists: True, research_bullets count: 8
   ```

### Troubleshooting

**Problem**: `research_data received: False` or length is 0

**Possible Causes**:
- Research sub-agent not being called by main agent
- Main agent not passing research results to `create_presentation`
- Issue with tool parameter binding

**Solution**: Check trace in LangSmith (use `inspect_traces.py`) to see:
- Was `research_subagent_tool` called?
- What did it return?
- Was `create_presentation` called with `research_data` parameter?

---

**Problem**: `research_bullets extracted: 0 bullets`

**Possible Causes**:
- Research data format doesn't match parsing logic
- Filtering logic is too strict

**Solution**: Look at `research_data preview` in debug output to see actual format

---

**Problem**: Placeholder content in slides 3+

**Possible Causes**:
- `research_bullets` is empty (filtering failed)
- Logic condition `if research_data and research_bullets:` evaluating to False

**Solution**: Check debug output for exact state at each slide

## Workflow for Debugging the Current Issue

The current issue is that slides 3+ show placeholder content instead of research data.

**Step 1**: Run automated test
```bash
uv run python test_agent_query.py
```

**Step 2**: Check server terminal for debug messages
- Is `research_data` being received?
- How many `research_bullets` were extracted?
- What is the actual content of research_data?

**Step 3**: Inspect traces programmatically
```bash
uv run python inspect_traces.py
```
- Was `research_subagent_tool` called?
- Was `research_data` passed to `create_presentation`?

**Step 4**: Verify output file
```bash
ls -la ./output/*.pptx
```
Open the latest PowerPoint file and check slide content.

## Expected Behavior

When everything works correctly:

1. **Research sub-agent is called** → Returns structured findings
2. **Main agent calls create_presentation** → Passes `research_data` parameter
3. **Debug output shows**:
   ```
   [DEBUG] research_data received: True
   [DEBUG] research_data length: 1000+ chars
   [DEBUG] research_bullets extracted: 5-10 bullets
   [DEBUG] Slide 1/2/3 - research_data exists: True, research_bullets count: 5-10
   ```
4. **PowerPoint file contains**:
   - Title slide
   - Key Research Findings slide (with actual data)
   - Content slides 3+ with actual research bullets (NOT placeholders)

## Files Reference

| File | Purpose |
|------|---------|
| `test_agent_query.py` | Async test with streaming responses |
| `test_agent_simple.py` | Simple synchronous test |
| `inspect_traces.py` | LangSmith trace inspection |
| `ppt_agent/skills/scripts/create_presentation.py` | Implementation with DEBUG logging |

## Additional Resources

- [LangGraph SDK Documentation](https://docs.langchain.com/langsmith/sdk)
- [Run a LangGraph app locally](https://docs.langchain.com/langsmith/local-server)
- [LangSmith Trace API](https://docs.smith.langchain.com/observability/how_to_guides/tracing/trace_with_api)
- [Trace with LangChain (Python)](https://docs.langchain.com/langsmith/trace-with-langchain)

## Quick Reference

```bash
# Start server
uv run langgraph dev

# Run async test
uv run python test_agent_query.py

# Run simple test
uv run python test_agent_simple.py

# Inspect traces
uv run python inspect_traces.py

# Check output files
ls -la ./output/

# View server logs (in separate terminal)
tail -f <server-output-file>
```
