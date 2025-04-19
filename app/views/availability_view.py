from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
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
        table.add_column("Asientos Disponibles", style="green")
        
        for seat_type, seats in availability.items():
            seats_display = ', '.join(seats) if seats else "Ninguno"
            table.add_row(
                seat_type.capitalize(),
                seats_display
            )
        
        self.console.print(table)
    
    def select_seat(self, available_seats: dict):
        """Permite al usuario seleccionar un asiento disponible."""
        self.console.print("\n[bold]Selección de Asiento[/]")
        
        # Extraer el tipo de asiento (solo debería haber uno)
        seat_type = next(iter(available_seats.keys()))
        seats = available_seats[seat_type]
        
        if not seats:
            return None
        
        self.console.print(f"Asientos {seat_type} disponibles: [green]{', '.join(seats)}[/]")
        
        while True:
            seat_number = Prompt.ask("Ingrese el número del asiento deseado").upper()
            if seat_number in seats:
                return seat_number
            self.console.print("[red]Asiento no disponible. Intente nuevamente.[/]")
    
    def show_seat_map(self, seat_map: list):
        """Muestra un mapa gráfico de los asientos."""
        self.console.print("\n[bold]Mapa de Asientos[/]")
        self.console.print("[white]X = Ocupado[/]  [green]O = Disponible[/]\n")
        
        for row in seat_map:
            self.console.print(" ".join(
                f"[green]{seat}[/]" if seat == 'O' else f"[red]{seat}[/]" 
                for seat in row
            ))