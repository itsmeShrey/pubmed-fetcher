# PubMed Fetcher

A Python command-line tool to fetch research papers from PubMed based on user queries, identify those with authors affiliated to pharmaceutical or biotech companies, and export the results as CSV.

---

## Code Organization

- `src/pubmed_fetcher/fetcher.py` — Core functions to query the PubMed API and process paper data.
- `src/pubmed_fetcher/utils.py` — Utility functions for filtering and formatting data.
- `src/cli/main.py` — Command-line interface implemented using Typer and Click to handle user input and run the fetcher.
- `pyproject.toml` — Poetry configuration file managing dependencies and defining the CLI executable.

---

## Installation and Usage

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) package manager

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pubmed-fetcher.git
   cd pubmed-fetcher

2. Install dependencies with Poetry:
    poetry install

3. Running the Program
    Use the CLI command through Poetry:
    poetry run get-papers-list "your search query" [OPTIONS]
    Options:

    -f, --file — Specify the output CSV filename (optional).

    -d, --debug — Enable debug logging (optional).

    --help — Show help message and usage instructions.

4. Tools and Libraries Used
PubMed API
Official API for accessing biomedical literature.
https://pubmed.ncbi.nlm.nih.gov/help/

Typer & Click
Python libraries for building robust command-line interfaces.
Typer | Click

Poetry
Dependency and packaging management tool for Python.
https://python-poetry.org/

Pandas
Used for data handling and CSV output.
https://pandas.pydata.org/

Typed Python
Extensive use of Python typing for improved code clarity and maintainability.

Large Language Models (LLMs)
Assisted development with AI-based code generation tools.

