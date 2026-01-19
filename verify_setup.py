"""Verification script to check if the project is set up correctly."""

import sys
import os


def check_python_version():
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor} is too old. Need 3.10+")
        return False


def check_imports():
    """Check if all required packages can be imported."""
    packages = {
        "langgraph": "LangGraph >= 1.0.6",
        "langchain": "LangChain >= 1.1.0",
        "langchain_core": "LangChain Core",
        "langchain_openai": "LangChain OpenAI",
        "pptx": "python-pptx",
        "ppt_agent": "PPT Agent package",
    }

    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - not installed")
            all_ok = False

    return all_ok


def check_env_file():
    """Check if .env file exists."""
    if os.path.exists(".env"):
        print("✓ .env file exists")

        # Check if OPENAI_API_KEY is set
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY=" in content and "your_" not in content:
                print("✓ OPENAI_API_KEY appears to be set")
            else:
                print("⚠ OPENAI_API_KEY may not be configured correctly")
        return True
    else:
        print("✗ .env file not found - copy .env.template to .env")
        return False


def check_graph():
    """Check if the graph can be loaded."""
    try:
        from ppt_agent.agent import graph
        print("✓ Agent graph loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to load agent graph: {e}")
        return False


def check_project_structure():
    """Check if all required files exist."""
    required_files = [
        "ppt_agent/__init__.py",
        "ppt_agent/agent.py",
        "ppt_agent/utils/__init__.py",
        "ppt_agent/utils/tools.py",
        "langgraph.json",
        "pyproject.toml",
        ".env.template",
    ]

    all_ok = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - missing")
            all_ok = False

    return all_ok


def main():
    """Run all verification checks."""
    print("=" * 70)
    print("PowerPoint Agent Setup Verification")
    print("=" * 70)

    print("\n1. Checking Python Version:")
    print("-" * 70)
    python_ok = check_python_version()

    print("\n2. Checking Project Structure:")
    print("-" * 70)
    structure_ok = check_project_structure()

    print("\n3. Checking Package Imports:")
    print("-" * 70)
    imports_ok = check_imports()

    print("\n4. Checking Environment Configuration:")
    print("-" * 70)
    env_ok = check_env_file()

    print("\n5. Checking Agent Graph:")
    print("-" * 70)
    graph_ok = check_graph()

    print("\n" + "=" * 70)
    if all([python_ok, structure_ok, imports_ok, env_ok, graph_ok]):
        print("✓ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. With UV: uv run python test_agent.py")
        print("  2. Or run dev server: langgraph dev")
        print("  3. Without UV: python test_agent.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install with UV: uv sync")
        print("  - Or with pip: pip install -e .")
        print("  - Create .env file: cp .env.template .env")
        print("  - Add OpenAI API key to .env")
    print("=" * 70)


if __name__ == "__main__":
    main()
