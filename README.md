# DevHelper

DevHelper is a collection of AI-powered agents designed to help developers research, compare, and analyze developer tools, libraries, and platforms. The repository contains two main agents:

- **advanced-agent**: An advanced research agent that leverages LLMs, Firecrawl, and LangChain to extract, analyze, and recommend developer tools based on user queries.
- **simple-agent**: A lightweight agent that uses Firecrawl and LangChain tools via MCP for quick web scraping and information extraction.

---

## Repository Structure

```
advanced-agent/
    main.py
    pyproject.toml
    README.md
    uv.lock
    src/
        __init__.py
        firecrawl.py
        models.py
        prompts.py
        workflow.py
        __pycache__/

simple-agent/
    main.py
    pyproject.toml
    README.md
    uv.lock

README.md
```

---

## Getting Started

### Prerequisites

- Python 3.13+
- API keys for Firecrawl and OpenAI (add them to `.env` files in each agent directory)

### Installation

1. Clone the repository:
    ```zsh
    git clone https://github.com/yourusername/DevHelper.git
    cd DevHelper
    ```

2. Install dependencies for each agent using [uv](https://github.com/astral-sh/uv):
    ```zsh
    cd advanced-agent
    uv pip install -r pyproject.toml

    cd ../simple-agent
    uv pip install -r pyproject.toml
    ```

3. Add your API keys to the `.env` files in both `advanced-agent` and `simple-agent` directories.

---

## Usage

### Advanced Agent

The advanced agent provides in-depth research and recommendations for developer tools.

```zsh
cd advanced-agent
uv run main.py
```

- Enter your developer query (e.g., "best Postgres alternatives for SaaS").
- The agent will extract relevant tools, analyze them, and provide concise recommendations.

### Simple Agent

The simple agent offers quick scraping and tool usage via MCP.

```zsh
cd simple-agent
uv run main.py
```

- Interact with the agent using natural language queries.
- The agent uses Firecrawl and other tools to fetch and summarize information.

---

## Features

- Automated extraction and comparison of developer tools
- Uses LLMs (OpenAI GPT-4) for analysis and recommendations
- Integrates with Firecrawl for web scraping and data extraction
- Modular and extensible workflow

---

## License

MIT License

---

## Acknowledgements
Thanks to the video tutorial created by [TechWithTim](https://www.youtube.com/@TechWithTim)


- [LangChain](https://github.com/langchain-ai/langchain)
- [Firecrawl](https://firecrawl.dev/)
- [OpenAI](https://openai.com/)
