# Advanced Agent

The Advanced Agent is an AI-powered research assistant designed to help developers discover, compare, and analyze developer tools, libraries, and platforms. It leverages LLMs, Firecrawl, and LangChain to extract, analyze, and recommend developer tools based on user queries.

---

## Features

- Automated extraction and comparison of developer tools
- Uses LLMs (OpenAI GPT-4) for analysis and recommendations
- Integrates with Firecrawl for web scraping and data extraction
- Modular and extensible workflow

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

- Enter your developer query (e.g., "best Postgres alternatives for SaaS").
- The agent will extract relevant tools, analyze them, and provide concise recommendations.

