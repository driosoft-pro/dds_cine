# Importando la clase Console para mostrar mensajes en consola
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from typing import List

# Importando recursos necesarios
from core.database import Database
from views.movie_view import MovieView
from services.ticket_service import TicketService
from controllers.showtime_controller import ShowtimeController

# Configuración
from config import Config

class ReservationView:
    """Vista para reservación y gestión de reservas."""
    def __init__(self):
        self.db = Database(str(Config.DATA_DIR))
        self.console = Console()
        self.movie_view = MovieView()
        self.showtime_controller = ShowtimeController(self.db)
    
    def show_reservation_menu(self):
        """Muestra el menú de reservaciones con estilo uniforme."""
        table = Table(
            title="Gestión de Reservas",
            border_style="magenta",
            box=box.ROUNDED,)
        table.add_column("ID", justify="center")
        table.add_column("Descripción")

        table.add_row("1", "Hacer reservación")
        table.add_row("2", "Ver mis reservas")
        table.add_row("3", "Cancelar reserva")
        table.add_row("4", "Convertir reserva a ticket")
        table.add_row("0", "Volver al menú principal")

        self.console.print(table)
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
        
        # Seleccionar y mostrar horarios específicos
        showtimes = self.showtime_controller.load_data("showtimes.json")
        movie_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
        self.movie_view.show_showtimes(movie_showtimes)
        
        # Seleccionar horario
        showtime_id = int(Prompt.ask("Ingrese ID del horario"))
        
        # Seleccionar tipo de asiento
        seat_type_choice = Prompt.ask("Tipo de asiento \n1: General. \n2: Preferencial. \nOpciones",choices=["1", "2"])
        seat_type = "general" if seat_type_choice == "1" else "preferencial"
        
        quantity = int(Prompt.ask("Cantidad de tickets", default="1"))
        
        return {
            'movie_id': movie_id,
            'showtime_id': showtime_id,
            'seat_type': seat_type,
            'quantity': quantity
        }
    
    def show_reservation_summary(self, reservation: dict):
        """Muestra un resumen de la reserva antes de confirmar."""
        try:
            # Extraer y formatear fecha-hora
            showtime_str = reservation['showtime']
            if isinstance(showtime_str, str):
                # Si ya es string, mostrarlo directamente
                display_time = showtime_str
            else:
                # Si es datetime, formatearlo
                display_time = showtime_str.strftime("%Y-%m-%d %H:%M")
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
        except Exception as e:
            self.console.print(f"[red]Error al mostrar resumen: {str(e)}[/]")
    
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
    
    def select_seat(self, available_seats: List[str]) -> str:
        """Muestra y permite seleccionar un asiento disponible"""
        self.console.print("\n[bold]Asientos disponibles:[/]")
        self.console.print("[green]" + ", ".join(available_seats) + "[/]")
        
        while True:
            seat_number = Prompt.ask("Ingrese el número del asiento deseado").upper()
            if seat_number in available_seats:
                return seat_number
            self.console.print("[red]Asiento no disponible. Intente nuevamente.[/]")
            
    def get_ticket_purchase_data(self, showtimes: list):
        """Obtiene datos para comprar un ticket."""
        self.console.print("\n[bold]Compra de Ticket[/]")
        
        # Seleccionar película
        movie_id = int(Prompt.ask("Ingrese ID de la película"))
                
        # Seleccionar y mostrar horarios específicos
        showtimes = self.showtime_controller.load_data("showtimes.json")
        movie_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
        self.movie_view.show_showtimes(movie_showtimes)
            
        # Seleccionar horario
        showtime_id = int(Prompt.ask("Ingrese ID del horario"))
        
        # Seleccionar tipo de asiento
        seat_type_choice = Prompt.ask("Tipo de asiento \n1: General. \n2: Preferencial. \nOpciones",choices=["1", "2"])
        seat_type = "general" if seat_type_choice == "1" else "preferencial"
        
        # Cantidad de tickets
        quantity = int(Prompt.ask("Cantidad de tickets", default="1"))
        
        return {
            'movie_id': movie_id,
            'showtime_id': showtime_id,
            'seat_type': seat_type,
            'quantity': quantity
        }
    
    def make_reservation(self, showtime_id: int, seat_type: str, seat_number: str):
        """Registra una reserva y actualiza la disponibilidad."""
        showtimes = self.showtime_controller.load_data("showtimes.json")
        
        for st in showtimes:
            if st['showtime_id'] == showtime_id:
                if 'occupied_seats' not in st:
                    st['occupied_seats'] = {seat_type: []}
                elif seat_type not in st['occupied_seats']:
                    st['occupied_seats'][seat_type] = []
                
                st['occupied_seats'][seat_type].append(seat_number)
                break
        
        self.showtime_controller.save_data("showtimes.json", showtimes)