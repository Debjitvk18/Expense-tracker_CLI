from rich.console import Console

console = Console()


def success(message: str):
    console.print(f"✅ [bold green]{message}[/bold green]")


def error(message: str):
    console.print(f"❌ [bold red]{message}[/bold red]")


def info(message: str):
    console.print(f"ℹ️ [bold cyan]{message}[/bold cyan]")
