from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

class AvailabilityView:
    """Vista para consultar disponibilidad de asientos."""
    
    def __init__(self):
        self.console = Console()
    
    def show_availability(self, availability: dict, cinema_name: str, movie_title: str, showtime: str):
        """Muestra la disponibilidad de asientos para una función."""
        panel = Panel.fit(
            f"[bold]Disponibilidad de Asientos[/]\n\n"
            f"Película: [magenta]{movie_title}[/]\n"
            f"Sala: [blue]{cinema_name}[/]\n"
            f"Horario: [white]{showtime}[/]\n",
            border_style="blue"
        )
        self.console.print(panel)
        
        table = Table(box=box.ROUNDED)
        table.add_column("Tipo de Asiento", style="cyan")
        table.add_column("Disponibles", style="green")
        table.add_column("Capacidad", style="white")
        
        for seat_type, available in availability.items():
            table.add_row(
                seat_type.capitalize(),
                str(available),
                str(availability.get('capacity', {}).get(seat_type, 'N/A'))
            )
        
        self.console.print(table)
    
    def show_seat_map(self, seat_map: list):
        """Muestra un mapa gráfico de los asientos."""
        self.console.print("\n[bold]Mapa de Asientos[/]")
        self.console.print("[white]X = Ocupado[/]  [green]O = Disponible[/]\n")
        
        for row in seat_map:
            self.console.print(" ".join(
                f"[green]{seat}[/]" if seat == 'O' else f"[red]{seat}[/]" 
                for seat in row
            ))