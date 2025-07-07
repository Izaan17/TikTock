from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table


class DisplayManager:
    """Handles all console output and visual elements."""

    def __init__(self):
        self.console = Console()

    def show_progress(self) -> Progress:
        """Initialize and return progress bar instance."""
        return Progress(TextColumn("[bold]Downloading {task.fields[filename]}", justify="right"),
                        BarColumn(bar_width=None), "[white]{task.percentage:>3.1f}%", TimeRemainingColumn(),
                        console=self.console)

    def show_response_table(self, response: dict) -> None:
        """Display single download result table."""
        table = self._create_response_table(response)
        self.console.print(table)

    def show_summary(self, completed: list, failed: list) -> None:
        """Display the final download summary."""
        self.console.print(self._create_summary_table(completed, failed))
        if failed:
            self.console.print("\n[bold]Details of Failed Downloads:[/]")
            self.console.print(self._create_failed_table(failed))
            self.console.print(f"[bold]Total[/]: {len(failed)} videos failed\n")

    @staticmethod
    def _create_response_table(response: dict) -> Table:
        """Generate table for a single download result."""
        success = '✓' if response.get('success') else '𐄂'
        status_color = "green" if success == '✓' else "red"

        table = Table(show_header=False, box=None)
        table.add_column(style="bold")

        table.add_row("Status:", f"[bold {status_color}]{success}[/]")
        table.add_row("URL:", response.get('url', 'None'))
        table.add_row("Output:", response.get('path', 'None'))
        table.add_row("Size:", str(response.get('size', 'None')))
        if error := response.get('error'):
            table.add_row("[red]Error[/]:", error)

        return table

    @staticmethod
    def _create_summary_table(completed: list, failed: list) -> Table:
        """Generate overall summary table."""
        table = Table(title="Download Summary", show_header=True, header_style="bold")
        table.add_column("Total URLs", justify="right")
        table.add_column("Successful", justify="right", style="green")
        table.add_column("Failed", justify="right", style="red")
        table.add_row(str(len(completed) + len(failed)), str(len(completed)), str(len(failed)))
        return table

    @staticmethod
    def _create_failed_table(failed: list) -> Table:
        """Generate detailed failed downloads table."""
        table = Table(show_header=True, header_style="bold")
        table.add_column("#", style="cyan", justify="right")
        table.add_column("URL", style="bold")
        table.add_column("Error", style="red")

        for i, (url, error) in enumerate(failed, 1):
            table.add_row(str(i), url, error)

        return table
