# src/cli/main.py

import click
import pandas as pd
from pubmed_fetcher.fetcher import fetch_papers

@click.command()
@click.argument("query", required=True)
@click.option("--file", "-f", type=str, help="Output CSV filename")
@click.option("--debug", "-d", is_flag=True, help="Enable debug logging")
def main(query: str, file: str, debug: bool):
    """Fetch PubMed papers based on a search QUERY and extract those with company affiliations."""
    results = fetch_papers(query, debug)

    if not results:
        click.echo("No matching results found.")
        return

    df = pd.DataFrame(results)

    if file:
        df.to_csv(file, index=False)
        click.echo(f"Saved results to {file}")
    else:
        click.echo(df.to_string(index=False))
