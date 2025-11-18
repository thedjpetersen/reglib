"""
Command-line interface for OSU Course Planner.
"""

import typer
from rich.console import Console
from rich.table import Table

from reglib.api import get_client
from reglib.models import Course
from reglib.planning import ScheduleBuilder

app = typer.Typer(help="OSU Course Planner - Plan your perfect schedule")
console = Console()


@app.command()
def search(
    term: str = typer.Option("202501", help="Term code (e.g., 202501)"),
    subject: str = typer.Option(None, help="Subject code (e.g., CS)"),
    number: str = typer.Option(None, help="Course number (e.g., 161)"),
):
    """Search for courses."""
    console.print(f"[bold blue]Searching courses for term {term}...[/bold blue]")

    client = get_client()
    courses = client.search_courses(term=term, subject=subject, course_number=number)

    if not courses:
        console.print("[yellow]No courses found.[/yellow]")
        return

    # Display results in table
    table = Table(title=f"Courses for {term}")
    table.add_column("CRN", style="cyan")
    table.add_column("Course", style="magenta")
    table.add_column("Title", style="green")
    table.add_column("Credits", justify="right")
    table.add_column("Seats", justify="right")

    for course in courses[:20]:  # Limit to 20
        table.add_row(
            course.crn,
            course.course_code,
            course.title[:40],
            str(course.credits),
            f"{course.seats_available}/{course.seats_total}",
        )

    console.print(table)
    console.print(f"\n[dim]Showing {min(20, len(courses))} of {len(courses)} results[/dim]")


@app.command()
def build(
    term: str = typer.Option("202501", help="Term code"),
    courses: List[str] = typer.Argument(
        ..., help="Courses to schedule (e.g., 'CS 161' 'MTH 111')"
    ),
    prefer_online: bool = typer.Option(False, help="Prefer online courses"),
    avoid_friday: bool = typer.Option(False, help="Avoid Friday classes"),
):
    """Build a conflict-free schedule."""
    console.print(f"[bold blue]Building schedule for {term}...[/bold blue]")
    console.print(f"Courses: {', '.join(courses)}")

    # TODO: Fetch actual course sections
    # For now, show placeholder
    console.print("\n[yellow]Note: This is a placeholder implementation.[/yellow]")
    console.print("[dim]Full implementation requires course data fetching.[/dim]")


@app.command()
def info():
    """Show information about OSU Course Planner."""
    console.print("\n[bold cyan]OSU Course Planner v2.0[/bold cyan]")
    console.print("\nA course planning tool for Oregon State University students.")
    console.print("\n[bold]Features:[/bold]")
    console.print("  • Search for courses")
    console.print("  • Build conflict-free schedules")
    console.print("  • Export to calendar formats")
    console.print("\n[bold]Status:[/bold] Alpha - Under active development")
    console.print("\n[dim]Visit: https://github.com/thedjpetersen/reglib[/dim]\n")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
