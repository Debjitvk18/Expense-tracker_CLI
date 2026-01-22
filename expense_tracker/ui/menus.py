from rich.console import Console

console = Console()


def show_dashboard_menu(username: str):
    console.print(f"\n👋 Welcome, [bold cyan]{username}[/bold cyan]")
    console.print("[bold]📊 DASHBOARD[/bold]")
    console.print("1. Add Expense")
    console.print("2. View Expenses")
    console.print("3. Analysis")
    console.print("4. Logout")
    console.print("5. Exit")


def show_auth_menu():
    console.print("\n[bold]User Access[/bold]")
    console.print("1. New User (Sign Up)")
    console.print("2. Existing User (Login)")
    console.print("3. Exit")


def show_analysis_menu():
    console.print("\n[bold]📈 Analysis Menu[/bold]")
    console.print("1. Summary")
    console.print("2. Category-wise Spending")
    console.print("3. Daily Trend")
    console.print("4. Monthly Trend")
    console.print("5. Charts")
    console.print("6. Back")
