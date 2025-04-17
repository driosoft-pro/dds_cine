from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

class ReservationView:
    """Vista para reservación y gestión de reservas."""
    
    def __init__(self):
        self.console = Console()
    
    def show_reservation_menu(self):
        """Muestra el menú de reservaciones."""
        self.console.print("\n[bold]Gestión de Reservas[/]")
        self.console.print("1. Hacer reservación")
        self.console.print("2. Ver mis reservas")
        self.console.print("3. Cancelar reserva")
        self.console.print("4. Convertir reserva a ticket")
        self.console.print("0. Volver al menú principal")
        return Prompt.ask("Seleccione una ID", choices=["0", "1", "2", "3", "4"])
    
    def show_reservations(self, reservations: list):
        """Muestra una lista de reservas del usuario."""
        if not reservations:
            self.console.print("[yellow]No tienes reservaciones activas actualmente.[/]")
            self.console.print("[dim]Visita la opción 'Reservar Entrada' para crear reservaciones.[/]")
            return
        
        table = Table(title="[bold]Mis Reservas[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Película", style="magenta")
        table.add_column("Fecha", style="white")
        table.add_column("Asiento", style="green")
        table.add_column("Tipo", style="blue")
        table.add_column("Precio", style="yellow")
        table.add_column("Estado", style="red")
        
        for res in reservations:
            status = "Activa" if res['status'] == 'activo' else "Cancelada"
            table.add_row(
                str(res['reservation_id']),
                res['movie_title'],
                res['showtime'],
                res['seat_number'],
                res['ticket_type'],
                f"${res['price']:,.0f}",
                status
            )
        
        self.console.print(table)
    
    def get_reservation_data(self, movies: list, showtimes: list):
        """Obtiene datos para hacer una reservación."""
        self.console.print("\n[bold]Nueva Reservación[/]")
        
        # Seleccionar película
        movie_id = int(Prompt.ask("Ingrese ID de la película"))
        
        # Seleccionar horario
        showtime_id = int(Prompt.ask("Ingrese ID del horario"))
        
        # Seleccionar tipo de asiento
        seat_type = Prompt.ask("Tipo de asiento", choices=["general", "preferencial"])
        
        return {
            'movie_id': movie_id,
            'showtime_id': showtime_id,
            'seat_type': seat_type
        }
    
    def show_reservation_summary(self, reservation: dict):
        """Muestra un resumen de la reserva antes de confirmar."""
        panel = Panel.fit(
            f"[bold]Resumen de Reserva[/]\n\n"
            f"Película: [magenta]{reservation['movie_title']}[/]\n"
            f"Fecha: [white]{reservation['showtime']}[/]\n"
            f"Asiento: [green]{reservation['seat_number']}[/] ([blue]{reservation['ticket_type']}[/])\n"
            f"Precio: [yellow]${reservation['price']:,.0f}[/]\n\n"
            f"[bold]La reserva debe ser confirmada 24 horas antes de la función.[/]",
            border_style="green"
        )
        self.console.print(panel)
    
    def select_reservation_to_cancel(self, reservations: list):
        """Permite seleccionar una reserva para cancelar."""
        self.show_reservations(reservations)
        if not reservations:
            return None
        
        return int(Prompt.ask("Ingrese ID de la reserva a cancelar"))
    
    def select_reservation_to_convert(self, reservations: list):
        """Permite seleccionar una reserva para convertir a ticket."""
        self.show_reservations(reservations)
        if not reservations:
            return None
        
        return int(Prompt.ask("Ingrese ID de la reserva a convertir"))