from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime, timedelta
from typing import List, Optional

class TicketMenu:
    def __init__(self, console: Console, ticket_controller, movie_controller, 
                    food_controller, cinema_controller, ticket_view):
        self.console = console
        self.ticket_controller = ticket_controller
        self.movie_controller = movie_controller
        self.food_controller = food_controller
        self.cinema_controller = cinema_controller
        self.ticket_view = ticket_view
    
    def display_menu(self, user):
        """Menú principal de tickets"""
        while True:
            self.console.clear()
            self.console.print(Panel.fit(" COMPRAS Y RESERVACIONES", style="bold blue"))
            
            self.console.print("\n1. Comprar entradas")
            self.console.print("2. Reservar entradas")
            self.console.print("3. Ver mis compras")
            self.console.print("4. Ver mis reservaciones")
            self.console.print("5. Volver\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"])
            
            if option == "1":
                self.handle_purchase(user)
            elif option == "2":
                self.handle_reservation(user)
            elif option == "3":
                self.show_user_purchases(user)
            elif option == "4":
                self.show_user_reservations(user)
            elif option == "5":
                return
    
    def handle_purchase(self, user):
        """Proceso completo de compra de tickets"""
        self.console.clear()
        self.console.print(Panel.fit(" COMPRAR ENTRADAS", style="bold green"))
        
        # 1. Seleccionar película
        movie = self._select_movie()
        if not movie:
            return
        
        # 2. Seleccionar función
        showtime = self._select_showtime(movie)
        if not showtime:
            return
        
        # 3. Obtener sala correspondiente
        hall = self.cinema_controller.get_hall_for_showtime(movie.room_type, showtime)
        if not hall:
            self.console.print("[red]No hay sala disponible para este horario[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        # 4. Seleccionar asientos
        seat_numbers = self.ticket_view.select_seats(hall, showtime)
        if not seat_numbers:
            return
        
        # 5. Seleccionar tipo de ticket
        ticket_type = self._select_ticket_type(hall, seat_numbers[0])
        if not ticket_type:
            return
        
        # 6. Calcular precio
        seat_type = hall.get_seat_type(seat_numbers[0])
        price = calculate_ticket_price(ticket_type, seat_type, showtime)
        
        # 7. Seleccionar comida
        food_items = []
        if Confirm.ask("\n¿Desea agregar comida a su compra?"):
            food_items = self._select_food_items()
        
        # 8. Mostrar resumen y confirmar
        self.ticket_view.show_purchase_summary(
            movie, showtime, seat_numbers, ticket_type, price, food_items, self.food_controller
        )
        
        if not Confirm.ask("\n¿Confirmar compra?"):
            return
        
        # 9. Procesar compra
        ticket = self.ticket_controller.create_ticket(
            user_id=user.user_id,
            movie_id=movie.movie_id,
            showtime=showtime,
            room_type=movie.room_type,
            seat_numbers=seat_numbers,
            ticket_type=ticket_type
        )
        
        if not ticket:
            self.console.print("\n[red]Error al crear el ticket. Intente nuevamente.[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        # 10. Seleccionar método de pago
        payment_method = self.ticket_view.get_payment_method()
        
        # 11. Crear purchase
        purchase = self.ticket_controller.create_purchase(
            user_id=user.user_id,
            tickets=[ticket],
            food_items=food_items,
            payment_method=payment_method
        )
        
        if purchase:
            self.console.print("\n[green]¡Compra realizada con éxito![/green]")
            self.ticket_view.show_ticket(ticket)
        else:
            self.console.print("\n[red]Error al procesar la compra[/red]")
        
        Prompt.ask("\nPresione Enter para continuar...")
    
    def handle_reservation(self, user):
        """Proceso completo de reservación"""
        self.console.clear()
        self.console.print(Panel.fit("📅 RESERVAR ENTRADAS", style="bold green"))
        
        # 1. Seleccionar película
        movie = self._select_movie()
        if not movie:
            return
        
        # 2. Seleccionar función
        showtime = self._select_showtime(movie)
        if not showtime:
            return
        
        # 3. Obtener sala
        hall = self.cinema_controller.get_hall_for_showtime(movie.room_type, showtime)
        if not hall:
            self.console.print("[red]No hay sala disponible para este horario[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        # 4. Seleccionar asientos
        seat_numbers = self.ticket_view.select_seats(hall, showtime)
        if not seat_numbers:
            return
        
        # 5. Mostrar resumen y confirmar
        self.ticket_view.show_reservation_summary(movie, showtime, seat_numbers)
        
        if not Confirm.ask("\n¿Confirmar reservación?"):
            return
        
        # 6. Crear reservación
        reservation = self.ticket_controller.create_reservation(
            user_id=user.user_id,
            movie_id=movie.movie_id,
            showtime=showtime,
            room_type=movie.room_type,
            seat_numbers=seat_numbers
        )
        
        if reservation:
            self.console.print("\n[green]¡Reservación realizada con éxito![/green]")
            self.ticket_view.show_reservation(reservation, self.movie_controller)
        else:
            self.console.print("\n[red]Error al crear la reservación[/red]")
        
        Prompt.ask("\nPresione Enter para continuar...")
    
    def _select_movie(self):
        """Helper para seleccionar película"""
        movies = self.movie_controller.get_active_movies()
        if not movies:
            self.console.print("[red]No hay películas disponibles[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return None
        
        self.console.print("\n[bold]Películas disponibles:[/bold]")
        for i, movie in enumerate(movies, 1):
            self.console.print(f"{i}. {movie.title} ({movie.room_type})")
        
        try:
            selection = int(Prompt.ask("\nSeleccione una película", choices=[str(i) for i in range(1, len(movies)+1)]))
            return movies[selection-1]
        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida[/red]")
            return None
    
    def _select_showtime(self, movie):
        """Helper para seleccionar horario"""
        if not movie.showtimes:
            self.console.print("[red]No hay horarios disponibles para esta película[/red]")
            Prompt.ask("\nPresione Enter para continuar...")
            return None
        
        self.console.print("\n[bold]Horarios disponibles:[/bold]")
        for i, showtime in enumerate(movie.showtimes, 1):
            self.console.print(f"{i}. {showtime['date']} {showtime['time']} ({showtime['session']})")
        
        try:
            selection = int(Prompt.ask("\nSeleccione un horario", choices=[str(i) for i in range(1, len(movie.showtimes)+1)]))
            return movie.showtimes[selection-1]
        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida[/red]")
            return None
    
    def _select_ticket_type(self, hall, seat_number: str):
        """Helper para seleccionar tipo de ticket"""
        seat_type = hall.get_seat_type(seat_number)
        
        self.console.print("\n[bold]Tipos de entrada:[/bold]")
        self.console.print("1. General ($18,000)")
        
        if seat_type == "preferential":
            self.console.print("2. Preferencial ($25,000)")
            choices = ["1", "2"]
            types = {"1": "general", "2": "preferential"}
        else:
            choices = ["1"]
            types = {"1": "general"}
        
        try:
            selection = Prompt.ask("Seleccione el tipo de entrada", choices=choices)
            return types[selection]
        except (ValueError, KeyError):
            self.console.print("[red]Selección inválida[/red]")
            return None
    
    def _select_food_items(self) -> List[dict]:
        """Helper para seleccionar items de comida"""
        food_items = []
        foods = self.food_controller.get_active_items()
        
        while True:
            self.console.clear()
            self.console.print(Panel.fit("🍿 MENÚ DE COMIDA", style="bold yellow"))
            
            if food_items:
                self.console.print("\n[bold]Items seleccionados:[/bold]")
                for item in food_items:
                    food = self.food_controller.get_food_item(item['item_id'])
                    self.console.print(f"- {food.product} x{item['quantity']}")
            
            self.console.print("\n[bold]Menú disponible:[/bold]")
            for i, item in enumerate(foods, 1):
                self.console.print(f"{i}. {item.product} - ${item.price:,.0f}")
            
            try:
                selection = Prompt.ask(
                    "\nSeleccione un ítem (o Enter para terminar)", 
                    choices=[str(i) for i in range(1, len(foods)+1)],
                    default="",
                    show_default=False
                )
                
                if not selection:
                    break
                
                food = foods[int(selection)-1]
                quantity = int(Prompt.ask("Cantidad", default="1"))
                
                food_items.append({
                    'item_id': food.item_id,
                    'quantity': quantity,
                    'unit_price': food.price
                })
            except (ValueError, IndexError):
                self.console.print("[red]Selección inválida[/red]")
                continue
        
        return food_items
    
    def show_user_purchases(self, user):
        """Muestra las compras del usuario"""
        purchases = self.ticket_controller.get_user_purchases(user.user_id)
        self.console.clear()
        
        if not purchases:
            self.console.print("[yellow]No tienes compras registradas[/yellow]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        self.console.print(Panel.fit("🛍️ MIS COMPRAS", style="bold green"))
        
        table = Table(title="Historial de Compras", show_header=True, header_style="bold magenta")
        table.add_column("N° Compra", style="dim")
        table.add_column("Fecha", justify="right")
        table.add_column("Total", justify="right")
        table.add_column("Película")
        
        for purchase in purchases:
            movie = self.movie_controller.get_movie(purchase.tickets[0].movie_id)
            table.add_row(
                str(purchase.purchase_id),
                purchase.purchase_date,
                f"${purchase.total_amount:,.0f}",
                movie.title
            )
        
        self.console.print(table)
        
        # Opción para ver detalles
        if Confirm.ask("\n¿Ver detalles de alguna compra?"):
            try:
                purchase_id = int(Prompt.ask("Ingrese el N° de compra"))
                selected = next(p for p in purchases if p.purchase_id == purchase_id)
                
                if selected:
                    self._show_purchase_details(selected)
            except (ValueError, StopIteration):
                self.console.print("[red]Compra no encontrada[/red]")
        
        Prompt.ask("\nPresione Enter para continuar...")
    
    def _show_purchase_details(self, purchase):
        """Muestra detalles de una compra específica"""
        self.console.clear()
        self.console.print(Panel.fit(f"COMPRA #{purchase.purchase_id}", style="bold blue"))
        
        # Mostrar tickets
        for ticket in purchase.tickets:
            self.ticket_view.show_ticket(ticket)
            self.console.print()  # Separador
        
        # Mostrar comida si existe
        if purchase.food_items:
            self.console.print("[bold]Comida:[/bold]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Item")
            table.add_column("Cantidad")
            table.add_column("Precio Unit.")
            table.add_column("Total")
            
            for item in purchase.food_items:
                food = self.food_controller.get_food_item(item.item_id)
                table.add_row(
                    food.product,
                    str(item.quantity),
                    f"${item.unit_price:,.0f}",
                    f"${item.total_price:,.0f}"
                )
            
            self.console.print(table)
        
        self.console.print(f"\n[bold]Total compra: ${purchase.total_amount:,.0f}[/bold]")
        self.console.print(f"[bold]Método de pago:[/bold] {purchase.payment_method.capitalize()}")
    
    def show_user_reservations(self, user):
        """Muestra las reservaciones del usuario"""
        reservations = self.ticket_controller.get_user_reservations(user.user_id)
        self.console.clear()
        
        if not reservations:
            self.console.print("[yellow]No tienes reservaciones activas[/yellow]")
            Prompt.ask("\nPresione Enter para continuar...")
            return
        
        self.console.print(Panel.fit("📅 MIS RESERVACIONES", style="bold green"))
        
        table = Table(title="Reservaciones Activas", show_header=True, header_style="bold magenta")
        table.add_column("N° Reserva", style="dim")
        table.add_column("Película")
        table.add_column("Horario")
        table.add_column("Asientos")
        table.add_column("Estado")
        
        for res in reservations:
            movie = self.movie_controller.get_movie(res.movie_id)
            table.add_row(
                str(res.reservation_id),
                movie.title,
                f"{res.showtime['date']} {res.showtime['time']}",
                ", ".join(res.seats),
                res.status.capitalize()
            )
        
        self.console.print(table)
        
        # Opciones adicionales
        self.console.print("\nOpciones:")
        self.console.print("1. Ver detalles de reservación")
        self.console.print("2. Confirmar reservación (pagar)")
        self.console.print("3. Cancelar reservación")
        self.console.print("4. Volver")
        
        choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            try:
                res_id = int(Prompt.ask("Ingrese el N° de reservación"))
                selected = next(r for r in reservations if r.reservation_id == res_id)
                
                if selected:
                    self.console.clear()
                    self.ticket_view.show_reservation(selected, self.movie_controller)
                    Prompt.ask("\nPresione Enter para continuar...")
            except (ValueError, StopIteration):
                self.console.print("[red]Reservación no encontrada[/red]")
                Prompt.ask("\nPresione Enter para continuar...")
        
        elif choice == "2":
            self._confirm_reservation(user)
        
        elif choice == "3":
            self._cancel_reservation(user)
    
    def _confirm_reservation(self, user):
        """Convierte reservación en ticket (pago)"""
        try:
            res_id = int(Prompt.ask("Ingrese el N° de reservación a confirmar"))
            
            ticket = self.ticket_controller.confirm_reservation(res_id)
            if ticket:
                self.console.print("\n[green]¡Reservación confirmada con éxito![/green]")
                self.ticket_view.show_ticket(ticket)
            else:
                self.console.print("\n[red]Error al confirmar la reservación[/red]")
        except ValueError:
            self.console.print("[red]Número de reservación inválido[/red]")
        
        Prompt.ask("\nPresione Enter para continuar...")
    
    def _cancel_reservation(self, user):
        """Cancela una reservación"""
        try:
            res_id = int(Prompt.ask("Ingrese el N° de reservación a cancelar"))
            
            if self.ticket_controller.cancel_reservation(res_id):
                self.console.print("\n[green]Reservación cancelada con éxito[/green]")
            else:
                self.console.print("\n[red]Error al cancelar la reservación[/red]")
        except ValueError:
            self.console.print("[red]Número de reservación inválido[/red]")
        
        Prompt.ask("\nPresione Enter para continuar...")
        
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime, timedelta
from controllers.cinema_controller import CinemaController
from services.ticket_pricing import calculate_ticket_price

def handle_purchase(console: Console, ticket_controller, user, movie_controller, food_controller):
    """Maneja el proceso completo de compra de tickets"""
    console.clear()
    console.print(Panel.fit("🎬 COMPRAR ENTRADAS", style="bold green"))
    
    # 1. Seleccionar película
    movies = movie_controller.get_active_movies()
    if not movies:
        console.print("[red]No hay películas disponibles[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    movie = _select_movie(console, movies)
    if not movie:
        return

    # 2. Seleccionar función
    showtime = _select_showtime(console, movie)
    if not showtime:
        return

    # 3. Seleccionar asientos
    hall = ticket_controller.cinema_controller.get_hall_for_showtime(movie.room_type, showtime)
    if not hall:
        console.print("[red]No hay sala disponible para este horario[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    seat_numbers = _select_seats(console, hall, showtime)
    if not seat_numbers:
        return

    # 4. Seleccionar tipo de ticket
    ticket_type = _select_ticket_type(console, hall, seat_numbers[0])
    if not ticket_type:
        return

    # 5. Calcular precio
    seat_type = hall.get_seat_type(seat_numbers[0])
    price = calculate_ticket_price(ticket_type, seat_type, showtime)

    # 6. Seleccionar comida
    food_items = []
    if Confirm.ask("\n¿Desea agregar comida a su compra?"):
        food_items = _select_food_items(console, food_controller)

    # 7. Mostrar resumen y confirmar
    _show_purchase_summary(console, movie, showtime, seat_numbers, ticket_type, price, food_items, food_controller)
    
    if not Confirm.ask("\n¿Confirmar compra?"):
        return

    # 8. Procesar compra
    ticket = ticket_controller.create_ticket(
        user_id=user.user_id,
        movie_id=movie.movie_id,
        showtime=showtime,
        room_type=movie.room_type,
        seats=seat_numbers,
        ticket_type=ticket_type,
        price=price
    )
    
    if ticket:
        purchase = ticket_controller.create_purchase(
            user_id=user.user_id,
            tickets=[ticket],
            food_items=food_items,
            payment_method=_select_payment_method(console)
        )
        
        if purchase:
            console.print("\n[green]¡Compra realizada con éxito![/green]")
            _show_ticket(console, ticket, movie)
        else:
            console.print("\n[red]Error al procesar la compra[/red]")
    else:
        console.print("\n[red]Error al crear el ticket[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def handle_reservation(console: Console, ticket_controller, user, movie_controller):
    """Maneja el proceso completo de reservación"""
    console.clear()
    console.print(Panel.fit("📅 RESERVAR ENTRADAS", style="bold green"))
    
    # 1. Seleccionar película
    movies = movie_controller.get_active_movies()
    if not movies:
        console.print("[red]No hay películas disponibles[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    movie = _select_movie(console, movies)
    if not movie:
        return

    # 2. Seleccionar función
    showtime = _select_showtime(console, movie)
    if not showtime:
        return

    # 3. Seleccionar asientos
    hall = ticket_controller.cinema_controller.get_hall_for_showtime(movie.room_type, showtime)
    if not hall:
        console.print("[red]No hay sala disponible para este horario[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    seat_numbers = _select_seats(console, hall, showtime)
    if not seat_numbers:
        return

    # 4. Mostrar resumen y confirmar
    _show_reservation_summary(console, movie, showtime, seat_numbers)
    
    if not Confirm.ask("\n¿Confirmar reservación?"):
        return

    # 5. Crear reservación
    reservation = ticket_controller.create_reservation(
        user_id=user.user_id,
        movie_id=movie.movie_id,
        showtime=showtime,
        room_type=movie.room_type,
        seats=seat_numbers
    )
    
    if reservation:
        console.print("\n[green]¡Reservación realizada con éxito![/green]")
        _show_reservation(console, reservation, movie)
    else:
        console.print("\n[red]Error al crear la reservación[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def display_user_tickets(console: Console, ticket_controller, user):
    """Muestra tickets y reservaciones del usuario"""
    console.clear()
    console.print(Panel.fit("🎟️ MIS ENTRADAS Y RESERVACIONES", style="bold blue"))
    
    # Mostrar tickets
    purchases = ticket_controller.get_user_purchases(user.user_id)
    if purchases:
        console.print("\n[bold]COMPRAS:[/bold]")
        for purchase in purchases:
            _show_purchase(console, purchase)
    else:
        console.print("\n[yellow]No tienes compras registradas[/yellow]")
    
    # Mostrar reservaciones
    reservations = ticket_controller.get_user_reservations(user.user_id)
    if reservations:
        console.print("\n[bold]RESERVACIONES:[/bold]")
        for reservation in reservations:
            _show_reservation(console, reservation)
    else:
        console.print("\n[yellow]No tienes reservaciones activas[/yellow]")
    
    Prompt.ask("\nPresione Enter para continuar...")

# Funciones auxiliares
def _select_movie(console, movies):
    console.print("\n[bold]Películas disponibles:[/bold]")
    for i, movie in enumerate(movies, 1):
        console.print(f"{i}. {movie.title} ({movie.room_type})")
    
    try:
        selection = int(Prompt.ask("\nSeleccione una película", 
                                    choices=[str(i) for i in range(1, len(movies)+1)]))
        return movies[selection-1]
    except (ValueError, IndexError):
        console.print("[red]Selección inválida[/red]")
        return None

def _select_showtime(console, movie):
    console.print("\n[bold]Horarios disponibles:[/bold]")
    for i, showtime in enumerate(movie.showtimes, 1):
        console.print(f"{i}. {showtime['date']} {showtime['time']} ({showtime['session']})")
    
    try:
        selection = int(Prompt.ask("\nSeleccione un horario", 
                                    choices=[str(i) for i in range(1, len(movie.showtimes)+1)]))
        return movie.showtimes[selection-1]
    except (ValueError, IndexError):
        console.print("[red]Selección inválida[/red]")
        return None

def _select_seats(console, hall, showtime):
    console.clear()
    console.print(Panel.fit(f"Mapa de Asientos - {hall.hall_type} Sala", style="bold blue"))
    
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
        console.print(f"Fila {row}: {seats_str}")
    
    console.print("\n[green]Verde[/green] = Disponible")
    console.print("[red]Rojo[/red] = Ocupado/Reservado\n")
    
    selected_seats = []
    while len(selected_seats) < 10:  # Máximo 10 asientos por transacción
        seat = Prompt.ask(
            "Ingrese el número de asiento (ej: A1) o Enter para terminar",
            default="",
            show_default=False
        )
        
        if not seat:
            break
        
        if not hall.is_seat_available(seat):
            console.print("[red]Asiento no disponible. Intente otro.[/red]")
            continue
        
        if seat in selected_seats:
            console.print("[red]Ya ha seleccionado este asiento.[/red]")
            continue
        
        selected_seats.append(seat)
        console.print(f"[green]Asiento {seat} seleccionado[/green]")
    
    return selected_seats

def _select_ticket_type(console, hall, seat_number):
    seat_type = hall.get_seat_type(seat_number)
    
    console.print("\n[bold]Tipos de entrada:[/bold]")
    console.print("1. General ($18,000)")
    
    if seat_type == "preferential":
        console.print("2. Preferencial ($25,000)")
        choices = ["1", "2"]
        types = {"1": "general", "2": "preferential"}
    else:
        choices = ["1"]
        types = {"1": "general"}
    
    try:
        selection = Prompt.ask("Seleccione el tipo de entrada", choices=choices)
        return types[selection]
    except (ValueError, KeyError):
        console.print("[red]Selección inválida[/red]")
        return None

def _select_food_items(console, food_controller):
    food_items = []
    foods = food_controller.get_active_items()
    
    while True:
        console.clear()
        console.print(Panel.fit("🍿 MENÚ DE COMIDA", style="bold yellow"))
        
        if food_items:
            console.print("\n[bold]Items seleccionados:[/bold]")
            for item in food_items:
                food = food_controller.get_food_item(item['item_id'])
                console.print(f"- {food.product} x{item['quantity']}")
        
        console.print("\n[bold]Menú disponible:[/bold]")
        for i, item in enumerate(foods, 1):
            console.print(f"{i}. {item.product} - ${item.price:,.0f}")
        
        try:
            selection = Prompt.ask(
                "\nSeleccione un ítem (o Enter para terminar)", 
                choices=[str(i) for i in range(1, len(foods)+1)],
                default="",
                show_default=False
            )
            
            if not selection:
                break
            
            food = foods[int(selection)-1]
            quantity = int(Prompt.ask("Cantidad", default="1"))
            
            food_items.append({
                'item_id': food.item_id,
                'quantity': quantity,
                'unit_price': food.price
            })
        except (ValueError, IndexError):
            console.print("[red]Selección inválida[/red]")
            continue
    
    return food_items

def _select_payment_method(console):
    console.print("\n[bold]Métodos de pago:[/bold]")
    console.print("1. Efectivo")
    console.print("2. Tarjeta crédito/débito")
    console.print("3. Transferencia bancaria")
    
    while True:
        choice = Prompt.ask("Seleccione método de pago", choices=["1", "2", "3"])
        
        methods = {
            "1": "efectivo",
            "2": "tarjeta",
            "3": "transferencia"
        }
        return methods[choice]

def _show_purchase_summary(console, movie, showtime, seats, ticket_type, price, food_items, food_controller):
    console.print(Panel.fit("Resumen de Compra", style="bold green"))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item")
    table.add_column("Detalle")
    
    table.add_row("Película", movie.title)
    table.add_row("Horario", f"{showtime['date']} {showtime['time']}")
    table.add_row("Sala", f"{movie.room_type}")
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
    
    console.print(table)

def _show_reservation_summary(console, movie, showtime, seats):
    console.print(Panel.fit("Resumen de Reserva", style="bold green"))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item")
    table.add_column("Detalle")
    
    table.add_row("Película", movie.title)
    table.add_row("Horario", f"{showtime['date']} {showtime['time']}")
    table.add_row("Sala", f"{movie.room_type}")
    table.add_row("Asientos reservados", ", ".join(seats))
    table.add_row("Válido hasta", (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M"))
    
    console.print(table)

def _show_ticket(console, ticket, movie=None):
    console.print(Panel.fit("Entrada de Cine", style="bold blue"))
    
    table = Table(show_header=False)
    if movie:
        table.add_row("[bold]Película:[/bold]", movie.title)
    table.add_row("[bold]Horario:[/bold]", f"{ticket.showtime['date']} {ticket.showtime['time']}")
    table.add_row("[bold]Sala:[/bold]", f"{ticket.room_type} - Asiento {', '.join(ticket.seats)}")
    table.add_row("[bold]Tipo:[/bold]", ticket.ticket_type.capitalize())
    table.add_row("[bold]Precio:[/bold]", f"${ticket.price:,.0f}")
    table.add_row("[bold]N° Ticket:[/bold]", str(ticket.ticket_id))
    
    console.print(table)

def _show_reservation(console, reservation, movie=None):
    console.print(Panel.fit("Reservación de Cine", style="bold blue"))
    
    table = Table(show_header=False)
    if movie:
        table.add_row("[bold]Película:[/bold]", movie.title)
    table.add_row("[bold]Horario:[/bold]", f"{reservation.showtime['date']} {reservation.showtime['time']}")
    table.add_row("[bold]Sala:[/bold]", f"{reservation.room_type} - Asiento {', '.join(reservation.seats)}")
    table.add_row("[bold]Estado:[/bold]", reservation.status.capitalize())
    table.add_row("[bold]Reservado el:[/bold]", reservation.reservation_date)
    table.add_row("[bold]Válido hasta:[/bold]", reservation.expiry_date)
    table.add_row("[bold]N° Reservación:[/bold]", str(reservation.reservation_id))
    
    console.print(table)

def _show_purchase(console, purchase):
    console.print(Panel.fit(f"Compra #{purchase.purchase_id}", style="bold green"))
    
    for ticket in purchase.tickets:
        _show_ticket(console, ticket)
        console.print()  # Separador
    
    if purchase.food_items:
        console.print("[bold]Comida:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Item")
        table.add_column("Cantidad")
        table.add_column("Precio Unit.")
        table.add_column("Total")
        
        for item in purchase.food_items:
            table.add_row(
                item.product,
                str(item.quantity),
                f"${item.unit_price:,.0f}",
                f"${item.total_price:,.0f}"
            )
        
        console.print(table)
    
    console.print(f"\n[bold]Total compra: ${purchase.total_amount:,.0f}[/bold]")
    console.print(f"[bold]Método de pago:[/bold] {purchase.payment_method.capitalize()}")
    console.print("\n" + "-"*50 + "\n")