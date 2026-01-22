from rich.table import Table
from rich.console import Console

console = Console()


def render_expense_table(rows):
    table = Table(title="📄 Expense Records")

    table.add_column("Date", style="cyan")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Amount", style="yellow")
    table.add_column("Payment")
    table.add_column("Receiver")
    table.add_column("Description")

    for row in rows:
        expense_date, type_, category, amount, payment, receiver, description = row

        table.add_row(
            str(expense_date),
            type_,
            category,
            str(amount),
            payment or "-",
            receiver or "-",
            description or "-"
        )

    console.print(table)
