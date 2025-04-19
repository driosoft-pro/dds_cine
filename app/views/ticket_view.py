# Importando la clase Console para mostrar mensajes en consola
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from typing import List

# Importando la clase MovieView para mostrar horarios de películas
from core.database import Database
from views.movie_view import MovieView
from controllers.showtime_controller import ShowtimeController

# Configuración
from config import Config

class TicketView:
    """Vista para compra y gestión de tickets."""
    def __init__(self):
        self.db = Database(str(Config.DATA_DIR))
        self.console = Console()
        self.movie_view = MovieView()
        self.showtime_controller = ShowtimeController(self.db)
        
    def show_ticket_menu(self):
        """Muestra el menú de tickets."""
        self.console.print("\n[bold]Gestión de Tickets[/]")
        self.console.print("1. Comprar ticket")
        self.console.print("2. Ver mis tickets")
        self.console.print("3. Cancelar ticket")
        self.console.print("0. Volver al menú principal")
        return Prompt.ask("Seleccione una ID", choices=["0", "1", "2", "3"])
    
    def show_tickets(self, tickets: list):
        """Muestra una lista de tickets del usuario."""
        if not tickets:
            self.console.print("[yellow]No tienes tickets comprados actualmente.[/]")
            self.console.print("[dim]Visita la opción 'Comprar Entrada' para adquirir tickets.[/]")
            return
        
        table = Table(title="[bold]Mis Tickets[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Película", style="magenta")
        table.add_column("Fecha", style="white")
        table.add_column("Asiento", style="green")
        table.add_column("Tipo", style="blue")
        table.add_column("Precio", style="yellow")
        
        for ticket in tickets:
            table.add_row(
                str(ticket['ticket_id']),
                ticket['movie_title'],
                ticket['showtime'],
                ticket['seat_number'],
                ticket['ticket_type'],
                f"${ticket['price']:,.0f}"
            )
        
        self.console.print(table)
    
    def get_ticket_purchase_data(self, movies: list, showtimes: list):
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
    
    def show_ticket_summary(self, ticket: dict):
        """Muestra un resumen del ticket antes de confirmar la compra."""
        panel = Panel.fit(
            f"[bold]Resumen de Compra[/]\n\n"
            f"Película: [magenta]{ticket['movie_title']}[/]\n"
            f"Fecha: [white]{ticket['showtime']}[/]\n"
            f"Asiento: [green]{ticket['seat_number']}[/] ([blue]{ticket['ticket_type']}[/])\n"
            f"Precio: [yellow]${ticket['price']:,.0f}[/]\n\n"
            f"[bold]Total a pagar:[/] [yellow]${ticket['price']:,.0f}[/]",
            border_style="green"
        )
        self.console.print(panel)
    
    def get_payment_method(self):
        """Obtiene el método de pago."""
        return Prompt.ask(
            "Método de pago\n1: Efectivo.\n2: Tarjeta.\n3: Transferencia.\nOpciones",
            choices=["1", "2", "3"]
            )
    
    def get_cash_amount(self, total: float):
        """Obtiene el monto en efectivo para calcular el cambio."""
        return float(Prompt.ask(f"Ingrese el monto recibido (Total: ${total:,.0f})"))
    
    def select_seat(self, available_seats: List[str]) -> str:
        """Muestra y permite seleccionar un asiento disponible"""
        self.console.print("\n[bold]Asientos disponibles:[/]")
        self.console.print("[green]" + ", ".join(available_seats) + "[/]")
        
        while True:
            seat_number = Prompt.ask("Ingrese el número del asiento deseado").upper()
            if seat_number in available_seats:
                return seat_number
            self.console.print("[red]Asiento no disponible. Intente nuevamente.[/]")