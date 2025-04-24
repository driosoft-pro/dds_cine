from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from datetime import datetime
from typing import Optional, List, Dict

class ReportView:
    """Vista para mostrar menús y tablas de reportes."""
    def __init__(self):
        self.console = Console()

    def show_report_menu(self) -> str:
        """Muestra el menú principal de reportes y devuelve la opción elegida."""
        table = Table(title="Reportes", box=box.ROUNDED, border_style="magenta")
        table.add_column("ID", justify="center")
        table.add_column("Descripción")
        for id_, desc in [
            ("1","Reporte de ventas"),
            ("2","Reporte por película"),
            ("3","Reporte por usuario"),
            ("0","Volver al menú principal"),
        ]:
            table.add_row(id_, desc)
        self.console.print(table)

        while True:
            opt = Prompt.ask("Seleccione una ID [0-3]").strip()
            if opt in {"0","1","2","3"}:
                return opt
            self.console.print("[red]Opción inválida[/]")

    def ask_date(self, label: str) -> Optional[datetime.date]:
        """Pregunta una fecha YYYY-MM-DD; devuelve None si se deja vacío."""
        resp = Prompt.ask(f"{label} (YYYY-MM-DD, vacío para todas)", default="").strip()
        if not resp:
            return None
        try:
            return datetime.strptime(resp, "%Y-%m-%d").date()
        except ValueError:
            self.console.print("[red]Formato inválido.[/]")
            return self.ask_date(label)

    def show_total_sales(
        self,
        total: float,
        start: Optional[datetime.date],
        end:   Optional[datetime.date]
    ):
        """Muestra el total de ventas en un panel."""
        msg = f"Ventas totales de "
        msg += f"{start.isoformat()} " if start else "el inicio "
        msg += f"a {end.isoformat()}" if end else "a la fecha"
        msg += f": [green]{total:,.2f}[/]"
        panel = Table(box=box.SIMPLE)
        panel.add_column("")
        panel.add_row(msg)
        self.console.print(panel)

    def show_sales_by_movie(self, data: List[Dict]):
        """Muestra tabla con ventas por película."""
        table = Table(title="Ventas por Película", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Título", style="magenta")
        table.add_column("Ventas", justify="right", style="yellow")
        for row in data:
            table.add_row(str(row["movie_id"]), row["title"], f"{row['sales']:,.2f}")
        self.console.print(table)

    def show_sales_by_user(self, data: List[Dict]):
        """Muestra tabla con ventas por usuario."""
        table = Table(title="Ventas por Usuario", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Usuario", style="magenta")
        table.add_column("Ventas", justify="right", style="yellow")
        for row in data:
            table.add_row(str(row["user_id"]), row["username"], f"{row['sales']:,.2f}")
        self.console.print(table)