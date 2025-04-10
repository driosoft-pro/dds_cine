from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from datetime import datetime
from typing import List

class TicketView:
    def __init__(self, console: Console):
        self.console = console
    
    def show_seat_map(self, hall, showtime):
        """Muestra el mapa de asientos disponibles"""
        self.console.clear()
        self.console.print(Panel.fit(f"Mapa de Asientos - {hall.hall_type} Sala", style="bold blue"))
        
        available_seats = hall.get_available_seats(showtime)
        seat_map = {}
        
        # Organizar asientos por fila
        for seat in available_seats:
            row = seat.number[0]
            if row not in seat_map:
                seat_map[row] = []
            seat_map[row].append(seat.number[1:])
        
        # Mostrar mapa
        for row, seats in sorted(seat_map.items()):
            seats_str = "  ".join([f"[green]{s}[/green]" for s in sorted(seats)])
            self.console.print(f"Fila {row}: {seats_str}")
        
        self.console.print("\n[green]Verde[/green] = Disponible")
        self.console.print("[red]Rojo[/red] = Ocupado/Reservado\n")
    
    def select_seats(self, hall, showtime, max_seats: int = 10) -> List[str]:
        """Permite al usuario seleccionar asientos"""
        selected_seats = []
        
        while len(selected_seats) < max_seats:
            self.show_seat_map(hall, showtime)
            
            if selected_seats:
                self.console.print(f"\nAsientos seleccionados: {', '.join(selected_seats)}")
            
            seat = Prompt.ask(
                "Ingrese el número de asiento (ej: A1) o Enter para terminar",
                default="",
                show_default=False
            )
            
            if not seat:
                break
            
            if not hall.is_seat_available(seat):
                self.console.print("[red]Asiento no disponible. Intente otro.[/red]")
                continue
            
            if seat in selected_seats:
                self.console.print("[red]Ya ha seleccionado este asiento.[/red]")
                continue
            
            selected_seats.append(seat)
        
        return selected_seats
    
    def show_purchase_summary(self, movie, showtime, seats: List[str], ticket_type: str, 
                            price: float, food_items: List[dict], food_controller):
        """Muestra resumen de compra antes de confirmar"""
        self.console.print(Panel.fit("Resumen de Compra", style="bold green"))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Item")
        table.add_column("Detalle")
        
        table.add_row("Película", movie.title)
        table.add_row("Horario", f"{showtime['date']} {showtime['time']}")
        table.add_row("Sala", f"{movie.room_type} - {movie.hall}")
        table.add_row("Asientos", ", ".join(seats))
        table.add_row("Tipo de entrada", ticket_type.capitalize())
        table.add_row("Precio entrada", f"${price:,.0f}")
        
        if food_items:
            table.add_row("", "")  # Separador
            table.add_row("[bold]Comida[/bold]", "")
            for item in food_items:
                food = food_controller.get_food_item(item['item_id'])
                table.add_row(
                    f"{food.product} x{item['quantity']}",
                    f"${item['quantity'] * food.price:,.0f}"
                )
        
        total = price + sum(item['quantity'] * food_controller.get_food_item(item['item_id']).price 
                            for item in food_items)
        table.add_row("", "")  # Separador
        table.add_row("[bold]TOTAL[/bold]", f"[bold]${total:,.0f}[/bold]")
        
        self.console.print(table)
    
    def show_reservation_summary(self, movie, showtime, seats: List[str]):
        """Muestra resumen de reserva antes de confirmar"""
        self.console.print(Panel.fit("Resumen de Reserva", style="bold green"))
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Item")
        table.add_column("Detalle")
        
        table.add_row("Película", movie.title)
        table.add_row("Horario", f"{showtime['date']} {showtime['time']}")
        table.add_row("Sala", f"{movie.room_type} - {movie.hall}")
        table.add_row("Asientos reservados", ", ".join(seats))
        table.add_row("Válido hasta", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M"))
        
        self.console.print(table)
    
    def show_payment_methods(self):
        """Muestra opciones de pago"""
        self.console.print("\n[bold]Métodos de pago:[/bold]")
        self.console.print("1. Efectivo")
        self.console.print("2. Tarjeta crédito/débito")
        self.console.print("3. Transferencia bancaria")
    
    def get_payment_method(self) -> str:
        """Obtiene método de pago del usuario"""
        while True:
            self.show_payment_methods()
            choice = Prompt.ask("Seleccione método de pago", choices=["1", "2", "3"])
            
            methods = {
                "1": "efectivo",
                "2": "tarjeta",
                "3": "transferencia"
            }
            return methods[choice]
    
    def show_ticket(self, ticket):
        """Muestra los detalles de un ticket"""
        self.console.print(Panel.fit("Entrada de Cine", style="bold blue"))
        
        table = Table(show_header=False)
        table.add_row("[bold]Película:[/bold]", ticket.movie.title)
        table.add_row("[bold]Horario:[/bold]", f"{ticket.showtime['date']} {ticket.showtime['time']}")
        table.add_row("[bold]Sala:[/bold]", f"{ticket.room_type} - Asiento {', '.join(ticket.seats)}")
        table.add_row("[bold]Tipo:[/bold]", ticket.ticket_type.capitalize())
        table.add_row("[bold]Precio:[/bold]", f"${ticket.price:,.0f}")
        table.add_row("[bold]N° Ticket:[/bold]", str(ticket.ticket_id))
        
        self.console.print(table)
    
    def show_reservation(self, reservation, movie_controller):
        """Muestra los detalles de una reservación"""
        movie = movie_controller.get_movie(reservation.movie_id)
        
        self.console.print(Panel.fit("Reservación de Cine", style="bold blue"))
        
        table = Table(show_header=False)
        table.add_row("[bold]Película:[/bold]", movie.title)
        table.add_row("[bold]Horario:[/bold]", f"{reservation.showtime['date']} {reservation.showtime['time']}")
        table.add_row("[bold]Sala:[/bold]", f"{reservation.room_type} - Asiento {', '.join(reservation.seats)}")
        table.add_row("[bold]Estado:[/bold]", reservation.status.capitalize())
        table.add_row("[bold]Reservado el:[/bold]", reservation.reservation_date)
        table.add_row("[bold]Válido hasta:[/bold]", reservation.expiry_date)
        table.add_row("[bold]N° Reservación:[/bold]", str(reservation.reservation_id))
        
        self.console.print(table)
        
    def display_sales_report(console, ticket_controller):
        console.clear()
        console.print(Panel.fit("📊 REPORTES DE VENTAS", style="bold blue"))
        
        # Implementa la lógica de reportes aquí
        console.print("Funcionalidad de reportes en desarrollo...")
        Prompt.ask("\nPresione Enter para continuar...")