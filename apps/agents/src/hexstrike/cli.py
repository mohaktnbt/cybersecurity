"""HexStrike CLI — Entry point for running scans."""

import typer
from rich.console import Console

app = typer.Typer(name="hexstrike", help="HexStrike AI Pentesting Platform")
console = Console()


@app.command()
def scan(
    target: str = typer.Argument(..., help="Target URL or IP address"),
    scan_type: str = typer.Option("full", help="Scan type: full, quick, recon_only"),
    output: str = typer.Option("report.json", help="Output file path"),
):
    """Run an AI-powered penetration test against a target."""
    console.print(f"[bold green]HexStrike[/] — Starting {scan_type} scan on {target}")
    console.print("[yellow]Initializing agent orchestrator...[/]")
    # TODO: Initialize orchestrator and run scan
    console.print("[red]Not yet implemented — agent engine coming in Phase 1[/]")


@app.command()
def status(scan_id: str = typer.Argument(..., help="Scan UUID")):
    """Check the status of a running scan."""
    console.print(f"[bold]Checking scan status:[/] {scan_id}")
    # TODO: Query API for scan status


@app.command()
def report(
    scan_id: str = typer.Argument(..., help="Scan UUID"),
    format: str = typer.Option("pdf", help="Report format: pdf, html, json"),
):
    """Generate a report from scan results."""
    console.print(f"[bold]Generating {format} report for scan:[/] {scan_id}")
    # TODO: Trigger report generation


if __name__ == "__main__":
    app()
