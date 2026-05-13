from __future__ import annotations

import os
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.rule import Rule
from dotenv import load_dotenv

from .fetcher import parse_input, fetch_issue, build_prompt
from .ai import analyze

load_dotenv()
console = Console()


@click.command()
@click.argument("issue_ref")
@click.option(
    "--backend", "-b",
    default=None,
    type=click.Choice(["claude", "openai"], case_sensitive=False),
    help="AI backend. Defaults to AI_BACKEND env var or claude.",
)
def main(issue_ref: str, backend: str | None) -> None:
    """Summarize any GitHub issue with AI — instant triage.

    \b
    Accepted formats:
      issuescan https://github.com/owner/repo/issues/123
      issuescan owner/repo#123
    """
    selected_backend = backend or os.getenv("AI_BACKEND", "claude").lower()

    # Parse the issue reference
    try:
        repo, number = parse_input(issue_ref)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    console.print()
    console.print(Rule("[dim]issuescan[/dim]"))
    console.print(f"  [dim]Repo:[/dim]    {repo}")
    console.print(f"  [dim]Issue:[/dim]   #{number}")
    console.print(f"  [dim]Backend:[/dim] {selected_backend}")
    console.print()

    # Fetch issue data via gh CLI
    with console.status("[bold green]Fetching issue...[/bold green]"):
        try:
            issue = fetch_issue(repo, number)
        except RuntimeError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    title = issue.get("title", "")
    label_names = [l["name"] for l in issue.get("labels", [])]
    comment_count = len(issue.get("comments", []))

    console.print(f"  [bold]{title}[/bold]")
    if label_names:
        console.print(f"  [dim]Labels:[/dim] {', '.join(label_names)}")
    console.print(f"  [dim]Comments:[/dim] {comment_count}")
    console.print()

    prompt = build_prompt(issue, repo)

    # Analyze with AI
    with console.status("[bold green]Analyzing issue...[/bold green]"):
        try:
            result = analyze(prompt, selected_backend)
        except ValueError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
        except Exception as e:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")
            sys.exit(1)

    console.print(
        Panel(
            Markdown(result),
            title=f"[bold cyan]Issue Analysis[/bold cyan]  [dim]#{number} · {repo}[/dim]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


if __name__ == "__main__":
    main()
