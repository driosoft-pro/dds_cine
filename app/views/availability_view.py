from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

# Importando recursos necesarios
from core.database import Database
from controllers.cinema_controller import CinemaController
from controllers.showtime_controller import ShowtimeController

# Configuración
from config import Config

class AvailabilityView:
    """Vista para consultar disponibilidad de asientos."""
    
    def __init__(self):
        self.db = Database(str(Config.DATA_DIR))
        self.console = Console()
        self.cinema_controller = CinemaController(self.db)
        self.showtime_controller = ShowtimeController(self.db)
    
    def show_availability(self, showtime_id: int, cinema_id: int,
                            cinema_name: str, movie_title: str,
                            showtime_str: str):
        """Muestra disponibilidad detallada para un horario específico."""
        panel = Panel.fit(
            f"[bold]Disponibilidad de Asientos[/]\n\n"
            f"Película: [magenta]{movie_title}[/]\n"
            f"Sala: [blue]{cinema_name}[/]\n"
            f"Horario: [white]{showtime_str}[/]\n",
            border_style="blue"
        )
        self.console.print(panel)

        showtimes = self.showtime_controller.load_data("showtimes.json")
        st = next((x for x in showtimes if x["showtime_id"] == showtime_id), None)
        if not st:
            self.console.print("[red]Error: Horario no encontrado[/]")
            return

        tickets = self.db.load_data("tickets.json")
        reservations = self.db.load_data("reservations.json")
        dt_str = showtime_str  # "YYYY-MM-DD HH:MM"

        table = Table(box=box.ROUNDED, header_style="bold cyan")
        table.add_column("Tipo", style="cyan", min_width=12)
        table.add_column("Disponibles", justify="right", style="green")
        table.add_column("Ocupados", justify="right", style="red")
        table.add_column("Total", justify="right", style="white")

        for seat_type, capacity in st.get("available_seats", {}).items():
            # tickets activos de este tipo y horario
            occ_t = sum(
                1 for t in tickets
                if t.get("showtime") == dt_str
                    and t.get("ticket_type") == seat_type
                    and t.get("status") == "activo"
            )
            # reservas activas de este tipo y horario
            occ_r = sum(
                1 for r in reservations
                if r.get("showtime_id") == showtime_id
                    and r.get("ticket_type") == seat_type
                    and r.get("status") == "activo"
            )
            occupied = occ_t + occ_r
            available = capacity - occupied

            table.add_row(
                seat_type.capitalize(),
                str(available),
                str(occupied),
                str(capacity)
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