# Skills Directory - Progressive Disclosure Pattern

This directory implements the progressive disclosure pattern for LangChain skills, keeping the agent's context lean while providing powerful specialized capabilities.

## Directory Structure

```
skills/
├── __init__.py           # Exports load_skill gateway tool
├── loader.py             # load_skill tool implementation
├── definitions/          # Skill prompts and context (loaded on-demand)
│   └── powerpoint_creator.txt
└── scripts/              # Skill implementations (executed outside context)
    ├── create_presentation.py
    └── list_presentations.py
```

## How Progressive Disclosure Works

### 1. Gateway Tool (loader.py)
The `load_skill` tool is lightweight and acts as an entry point:
- Registered with the agent upfront (minimal context cost)
- Lists available skills in its docstring
- Loads skill content from `definitions/` on-demand

### 2. Skill Definitions (definitions/)
Specialized prompts and context stored as text files:
- **NOT loaded into agent context upfront**
- Loaded only when `load_skill` is called
- Contains skill-specific expertise and guidelines
- Tells the agent how to use associated tools

### 3. Skill Scripts (scripts/)
Actual implementation code:
- **Executed outside the agent's context window**
- Called by lightweight tool wrappers in `utils/tools.py`
- Contains the heavy implementation logic
- Never enters the agent's context

## Benefits

1. **Reduced Context Size**: Only active skills consume tokens
2. **Scalability**: Add new skills without bloating base agent
3. **Team Distribution**: Different teams can maintain skills independently
4. **Flexibility**: Update skills without changing agent code

## Adding a New Skill

### Step 1: Create Skill Definition

Create `definitions/my_skill.txt`:

```txt
You are now a [Skill Name] Expert.

## Your Capabilities
[Describe what the skill enables]

## Your Approach
[How to use the skill effectively]

## Available Tools for This Skill
[List the tools that work with this skill]

## Best Practices
[Guidelines for using the skill]
```

### Step 2: Create Implementation Scripts

Create `scripts/my_skill_action.py`:

```python
def my_action(param: str) -> dict:
    """Implementation that stays outside agent context."""
    # Your implementation here
    return {
        "success": True,
        "message": "Action completed",
    }
```

### Step 3: Create Tool Wrapper

In `utils/tools.py`:

```python
from ppt_agent.skills.scripts.my_skill_action import my_action

@tool
def my_tool(param: str) -> str:
    """Lightweight wrapper that calls external script."""
    result = my_action(param)
    return result["message"]
```

### Step 4: Register Tool with Agent

In `agent.py`:

```python
from ppt_agent.utils.tools import my_tool

graph = create_agent(
    model="gpt-5-nano",
    tools=[load_skill, my_tool, ...],  # Add your tool
    ...
)
```

### Step 5: Update load_skill Docstring

In `loader.py`, add your skill to the list:

```python
@tool
def load_skill(skill_name: str) -> str:
    """...

    Available skills:
    - powerpoint_creator: Expert at creating presentations
    - my_skill: Description of your skill  # Add this

    ..."""
```

## Usage Flow

1. **User** requests something that requires specialized knowledge
2. **Agent** calls `load_skill("powerpoint_creator")`
3. **load_skill** reads `definitions/powerpoint_creator.txt` and returns it
4. **Agent** now has specialized prompt and knows which tools to use
5. **Agent** calls `create_presentation` tool
6. **Tool wrapper** calls `scripts/create_presentation.py` (outside context)
7. **Script** executes and returns result
8. **Agent** receives result and responds to user

## Key Principles

- **Lightweight Gateway**: load_skill is always lightweight
- **External Implementation**: Heavy code stays in scripts/
- **On-Demand Loading**: Skills loaded only when needed
- **Clear Separation**: Prompts (definitions/) vs Code (scripts/)
- **Context Preservation**: Agent context stays lean and focused

## Reference

Based on LangChain's progressive disclosure pattern:
- https://docs.langchain.com/oss/python/langchain/multi-agent/skills
- https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant
