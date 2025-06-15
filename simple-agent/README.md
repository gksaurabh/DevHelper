# Simple Agent

The Simple Agent is a lightweight AI-powered assistant for quick web scraping and information extraction. It uses Firecrawl and LangChain tools via MCP to help developers fetch and summarize information about developer tools and platforms.

---

## Features

- Fast web scraping and data extraction
- Uses Firecrawl and LangChain via MCP
- Simple, natural language interface

---

## Getting Started

### Prerequisites

- Python 3.13+
- API keys for Firecrawl and OpenAI (add them to a `.env` file)

### Installation

1. Install dependencies using [uv](https://github.com/astral-sh/uv):
    ```zsh
    uv pip install -r pyproject.toml
    ```
2. Add your API keys to a `.env` file in this directory.

### Usage

Run the agent:
```zsh
uv run main.py
```

- Interact with the agent using natural language queries.
- The agent uses Firecrawl and other tools to fetch and summarize information.

---