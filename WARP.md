# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is an educational repository for **Agentic AI 2.0** containing comprehensive learning materials for three major AI agent frameworks:

1. **LangChain/LangGraph** - Multi-agent workflows and graph-based AI systems
2. **Autogen** - Multi-agent conversation frameworks
3. **Google ADK (Agent Development Kit)** - Google's agent development platform

The repository is structured as a live class learning environment with hands-on notebooks, projects, and practical examples.

## Architecture and Structure

### Core Framework Directories

- **`Agentic 2.0/0.Sunny Langchain-Langgraph Content/`** - LangChain/LangGraph materials
  - `langgraph/` - Core LangGraph notebooks covering intro to advanced multi-agent patterns
  - `agenticai-2.0/` - Supporting materials with embeddings and vector database content
  - `data/` and `data2/` - Sample datasets (PDF and text files)
  - `VectorDB/` - Vector database implementations

- **`Agentic 2.0/Autogen/`** - Microsoft Autogen framework materials
  - `1. Introduction/` through `10. MCP Project - Notion/` - Progressive modules
  - Covers basic agents, teams, human-in-the-loop, graph flows, and advanced concepts
  - Integration with MCP (Model Context Protocol) for external tool access

- **`Agentic 2.0/ADK/`** - Google Agent Development Kit materials
  - `Module 1` through `Module 11` - Structured learning progression
  - `Projects/` - Practical implementations including Streamlit integration
  - Covers installation, agents, tools, multi-agent systems, callbacks, and MCP

### Key Concepts Across Frameworks

**Multi-Agent Patterns:**
- **LangGraph**: Graph-based workflows with conditional edges and state management
- **Autogen**: Conversation-based teams with selectors and human oversight
- **ADK**: Session-based agents with structured outputs and workflow patterns

**Tool Integration:**
- All frameworks support external API calls, web search, and custom function tools
- MCP (Model Context Protocol) integration for standardized tool access
- Vector databases for RAG (Retrieval-Augmented Generation) implementations

**State Management:**
- LangGraph uses `StateGraph` with typed state objects
- Autogen manages conversation history and team dynamics
- ADK provides session and memory management through structured approaches

## Development Environment Setup

### Python Environment Requirements

Each framework has specific requirements. Use virtual environments for isolation:

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Unix/MacOS)
source .venv/bin/activate
```

### Framework-Specific Installation

**LangChain/LangGraph:**
```bash
pip install -r "Agentic 2.0/0.Sunny Langchain-Langgraph Content/requirements.txt"
```
Dependencies include: `langchain`, `langgraph`, `faiss-cpu`, `chromadb`, `langchain-openai`, `langchain_groq`

**Autogen:**
```bash
pip install autogen-agentchat autogen-core autogen-ext
```

**Google ADK:**
```bash
pip install google-adk google-adk[database] litellm google-generativeai python-dotenv
```

### Required API Keys

Configure these environment variables (use `.env` files locally):

- `OPENAI_API_KEY` - For GPT models across all frameworks
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - For Google ADK and Gemini models
- `GROQ_API_KEY` - For Groq models in LangChain
- `TAVILY_API_KEY` - For web search capabilities
- `SERPER_API_KEY` - Alternative web search provider

## Common Development Commands

### Running Jupyter Notebooks

Most examples are in Jupyter notebooks:
```bash
jupyter notebook
# Or
jupyter lab
```

### ADK-Specific Commands

```bash
# Verify ADK installation
adk --version
adk --help

# Start ADK API server (from project root)
bash scripts/run_api_server.sh
# Server runs at http://localhost:8000 (Swagger: /docs)

# For Streamlit integration
bash scripts/run_streamlit.sh
```

### Testing Framework Integrations

**LangGraph Graph Execution:**
```python
from langgraph.graph import StateGraph
# Create workflow, add nodes, compile and invoke
workflow = workflow.compile()
result = workflow.invoke({"input": "test"})
```

**Autogen Agent Communication:**
```python
from autogen_agentchat.agents import AssistantAgent
# Create agents and run tasks
result = await agent.run(task="your task")
```

**ADK Agent Sessions:**
```python
# ADK typically uses session-based interactions
# Check Module examples for current patterns
```

## Working with Different AI Models

### Model Configuration Patterns

**OpenAI Models (All Frameworks):**
```python
# LangChain
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4")

# Autogen
from autogen_ext.models.openai import OpenAIChatCompletionClient
model = OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key)

# ADK uses built-in model configuration
```

**Local Models:**
- Ollama integration available in ADK modules
- Check `Module 5 - Models/test_ollama.py` for local model setup

## Vector Database Integration

The repository includes multiple vector database implementations:

- **FAISS** - For local, CPU-based similarity search
- **Chroma** - For persistent vector storage
- **Pinecone** - For cloud-based vector operations
- **Weaviate** - Enterprise vector database integration

Example data processing patterns are in the `VectorDB/` and `data/` directories.

## Multi-Agent System Patterns

### LangGraph Approach
- Graph-based workflows with conditional routing
- State passed between nodes with typed schemas
- Human-in-the-loop via interrupt patterns

### Autogen Approach  
- Team-based conversations with role-based agents
- Selector patterns for dynamic agent routing
- Built-in human approval workflows

### ADK Approach
- Session-based agent interactions
- Workflow agents with structured state management
- MCP integration for external tool access

## Project Structure Guidelines

When creating new implementations:

1. **Use appropriate virtual environments** for each framework
2. **Store API keys in `.env` files** (already gitignored)
3. **Follow the modular structure** seen in existing directories
4. **Include requirements.txt** for any new project dependencies
5. **Use Jupyter notebooks** for experimental work and tutorials
6. **Create standalone Python files** for production implementations

## MCP (Model Context Protocol) Integration

MCP is extensively used across all frameworks for tool integration:

- **Gmail tools** - Email automation capabilities
- **Notion integration** - Knowledge management workflows  
- **Web search** - Via Tavily and Serper APIs
- **Custom tools** - Follow patterns in respective framework modules

Check the `MCP` directories in each framework for implementation examples.

## Development Notes

- **Async/Await**: Autogen requires async patterns; see `0. Async Funcationality in Python.ipynb`
- **State Management**: Each framework handles state differently - study the patterns in intro notebooks
- **Tool Integration**: Custom functions, LangChain tools, and MCP tools have different integration patterns
- **Memory Systems**: Advanced memory patterns available in Autogen's `Memory + mem0.ipynb`
- **Human-in-the-Loop**: All frameworks support human oversight with different implementation approaches