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

class TicketView:
    """Vista para compra y gestión de tickets."""
    def __init__(self):
        self.db = Database(str(Config.DATA_DIR))
        self.console = Console()
        self.movie_view = MovieView()
        self.showtime_controller = ShowtimeController(self.db)
        
    def show_ticket_menu(self):
        """Muestra el menú de tickets con estilo uniforme."""
        table = Table(
            title="Gestión de Tickets",
            border_style="magenta",
            box=box.ROUNDED,
        )
        table.add_column("ID", justify="center")
        table.add_column("Descripción")

        table.add_row("1", "Comprar ticket")
        table.add_row("2", "Ver mis tickets")
        table.add_row("3", "Cancelar ticket")
        table.add_row("0", "Volver al menú principal")

        self.console.print(table)
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
        """Obtiene datos para comprar un ticket.
        
        Args:
            movies: Lista de películas disponibles
            showtimes: Lista de horarios disponibles
        """
        self.console.print("\n[bold]Compra de Ticket[/]")
        
        # Mostrar películas disponibles
        self.movie_view.show_movies(movies, showtimes)
        
        # Seleccionar película
        movie_id = int(Prompt.ask("Ingrese ID de la película"))
        # Saber si es 2D o 3D
        movie = next(m for m in movies if m["movie_id"] == movie_id)
        is_3d = movie.get("room_type", "").upper() == "3D"

        # Filtrar y mostrar horarios para la película seleccionada
        movie_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
        self.movie_view.show_showtimes(movie_showtimes)
            
        # Seleccionar horario
        showtime_id = int(Prompt.ask("Ingrese ID del horario"))
        
        # Seleccionar tipo de asiento, omitimos Preferencial si NO es 3D
        if is_3d:
            self.console.print("Tipo de asiento:\n1: General.\n2: Preferencial.")
            seat_choice = Prompt.ask("Opciones", choices=["1", "2"])
            seat_type = "general" if seat_choice == "1" else "preferencial"
        else:
            # Sólo general para 2D
            self.console.print("Tipo de asiento:\n1: General. \nLa Sala 2D No Cuenta Con Asientos Preferenciales.")
            Prompt.ask("Presiona 1 para continuar", choices=["1"], default="1")
            seat_type = "general"
        
        # Cantidad de tickets
        quantity = int(Prompt.ask("Cantidad de tickets", default="1"))
        
        return {
            'movie_id': movie_id,
            'showtime_id': showtime_id,
            'seat_type': seat_type,
            'quantity': quantity
        }
    
    def show_ticket_summary(self, ticket: dict):
        """mauestra un resumen de la compra."""
        try:
            # Extraer y formatear fecha-hora
            showtime_str = ticket['showtime']
            if isinstance(showtime_str, str):
                # Si ya es string, mostrarlo directamente
                display_time = showtime_str
            else:
                # Si es datetime, formatearlo
                display_time = showtime_str.strftime("%Y-%m-%d %H:%M")
                
            panel = Panel.fit(
                f"[bold]Resumen de Compra[/]\n\n"
                f"Película: [magenta]{ticket['movie_title']}[/]\n"
                f"Fecha: [white]{display_time}[/]\n"
                f"Asiento: [green]{ticket['seat_number']}[/] ([blue]{ticket['ticket_type']}[/])\n"
                f"Precio: [yellow]${ticket['price']:,.0f}[/]\n\n"
                f"[bold]Total a pagar:[/] [yellow]${ticket['price']:,.0f}[/]",
                border_style="green"
            )
            self.console.print(panel)
        except Exception as e:
            self.console.print(f"[red]Error al mostrar resumen: {str(e)}[/]")
    
    def get_payment_method(self):
        """Obtiene el método de pago."""
        return Prompt.ask(
            "Método de pago\n1: Efectivo.\n2: Tarjeta.\n3: Transferencia.\nOpciones",
            choices=["1", "2", "3"]
            )
    
    def get_cash_amount(self, total: float) -> float:
        """Obtiene el monto en efectivo y valida el formato.
        
        Args:
            total: Monto total a pagar (ej: 18000)
            
        Returns:
            float: Monto recibido convertido a float
        """
        while True:
            try:
                cash_input = Prompt.ask(
                    f"Ingrese el monto recibido (Total: {TicketService.format_cop(total)})"
                )
                
                # Limpiar el input (quitar puntos y comas)
                cash_clean = cash_input.replace(".", "").replace(",", "")
                
                # Convertir a float
                cash = float(cash_clean)
                
                if cash < total:
                    self.console.print("[red]Error: El monto es menor al total[/]")
                    continue
                    
                return cash
                
            except ValueError:
                self.console.print("[red]Error: Ingrese un valor numérico válido[/]")
    
    def show_change(self, total: float, received: float):
        """Muestra el cambio al usuario en formato COP.
        
        Args:
            total: Monto total a pagar (ej: 18000)
            received: Monto recibido (ej: 20000)
        """
        change = received - total
        if change > 0:
            # Formatear con separador de miles (punto) y sin decimales
            formatted_change = f"${change:,.0f}".replace(",", ".")
            self.console.print(f"[green]Cambio a devolver: {formatted_change}[/]")
        elif change == 0:
            self.console.print("[yellow]No hay cambio a devolver.[/]")
        else:
            self.console.print("[red]Error: Monto insuficiente[/]")

    def select_seat(self, available_seats: List[str]) -> str:
        """Permite seleccionar un solo asiento disponible."""
        self.console.print("\n[bold]Asientos disponibles:[/]")
        self.console.print("[green]" + ", ".join(available_seats) + "[/]")
        while True:
            seat = Prompt.ask("Ingrese el número del asiento deseado").upper()
            if seat in available_seats:
                return seat
            self.console.print("[red]Asiento no disponible. Intente nuevamente.[/]")

    def select_multiple_seats(self, available_seats: List[str], quantity: int) -> List[str]:
        """Permite seleccionar N asientos distintos según la cantidad."""
        self.console.print(f"\n[bold]Selecciona {quantity} asientos disponibles:[/]")
        self.console.print("[green]" + ", ".join(available_seats) + "[/]")
        selected: List[str] = []
        while len(selected) < quantity:
            seat = Prompt.ask(f"Asiento #{len(selected)+1}").upper()
            if seat in available_seats and seat not in selected:
                selected.append(seat)
            else:
                self.console.print("[red]Asiento no disponible o ya seleccionado. Intenta otro.[/]")
        return selected