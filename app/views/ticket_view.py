from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime, timedelta

def display_ticket_menu(console: Console, ticket_controller, user, movie_controller, food_controller):
    """Menú principal de tickets y compras"""
    while True:
        console.clear()
        console.print(Panel.fit("🎟️ COMPRAS Y RESERVACIONES", style="bold blue"))
        
        console.print("\n1. Comprar entradas")
        console.print("2. Reservar entradas")
        console.print("3. Ver mis compras")
        console.print("4. Ver mis reservaciones")
        console.print("5. Volver\n")
        
        option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"])
        
        if option == "1":
            handle_purchase_tickets(console, ticket_controller, user, movie_controller, food_controller)
        elif option == "2":
            handle_reserve_tickets(console, ticket_controller, user, movie_controller)
        elif option == "3":
            display_user_purchases(console, ticket_controller, user)
        elif option == "4":
            display_user_reservations(console, ticket_controller, user)
        elif option == "5":
            return

def handle_purchase_tickets(console: Console, ticket_controller, user, movie_controller, food_controller):
    """Proceso de compra de tickets"""
    console.clear()
    console.print(Panel.fit("🎬 COMPRAR ENTRADAS", style="bold green"))
    
    # Seleccionar película
    movies = movie_controller.get_active_movies()
    if not movies:
        console.print("[red]No hay películas disponibles[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    console.print("\n[bold]Películas disponibles:[/bold]")
    for i, movie in enumerate(movies, 1):
        console.print(f"{i}. {movie.title} ({movie.room_type})")
    
    while True:
        try:
            selection = Prompt.ask("\nSeleccione una película", choices=[str(i) for i in range(1, len(movies)+1)])
            movie = movies[int(selection)-1]
            break
        except (ValueError, IndexError):
            console.print("[red]Error: Selección inválida. Intente nuevamente.[/red]")
    
    # Seleccionar función
    console.print("\n[bold]Horarios disponibles:[/bold]")
    for i, showtime in enumerate(movie.showtimes, 1):
        console.print(f"{i}. {showtime['date']} {showtime['time']} ({showtime['session']})")
    
    while True:
        try:
            selection = Prompt.ask("\nSeleccione un horario", choices=[str(i) for i in range(1, len(movie.showtimes)+1)])
            showtime = movie.showtimes[int(selection)-1]
            break
        except (ValueError, IndexError):
            console.print("[red]Error: Selección inválida. Intente nuevamente.[/red]")
    
    # Seleccionar sillas (implementar lógica de asientos)
    seats = ["A1", "A2"]  # Ejemplo simplificado
    
    # Seleccionar tipo de ticket
    console.print("\n[bold]Tipos de entrada:[/bold]")
    console.print("1. General ($18,000)")
    console.print("2. Preferencial ($25,000)")
    while True:
        try:
            ticket_type_choice = Prompt.ask("Seleccione el tipo de entrada", choices=["1", "2"])
            ticket_type = "general" if ticket_type_choice == "1" else "preferential"
            break
        except ValueError:
            console.print("[red]Error: Selección inválida. Intente nuevamente.[/red]")
    
    # Calcular precio
    price = 18000 if ticket_type == "general" else 25000
    if movie.room_type == "3D":
        price += 5000
    
    # Seleccionar comida
    food_items = []
    if Confirm.ask("\n¿Desea agregar comida a su compra?"):
        foods = food_controller.get_active_items()
        while True:
            console.print("\n[bold]Menú disponible:[/bold]")
            for i, item in enumerate(foods, 1):
                console.print(f"{i}. {item.product} - ${item.price:,.0f}")
            
            try:
                selection = Prompt.ask("\nSeleccione un ítem (o Enter para terminar)", 
                                        choices=[str(i) for i in range(1, len(foods)+1)], 
                                        default="", show_default=False)
                if not selection:
                    break
                
                item = foods[int(selection)-1]
                quantity = int(Prompt.ask("Cantidad", default="1"))
                
                food_items.append({
                    'item_id': item.item_id,
                    'quantity': quantity,
                    'unit_price': item.price
                })
            except (ValueError, IndexError):
                console.print("[red]Error: Selección inválida. Intente nuevamente.[/red]")
    
    # Método de pago
    console.print("\n[bold]Métodos de pago disponibles:[/bold]")
    console.print("1. Efectivo")
    console.print("2. Tarjeta")
    console.print("3. Transferencia")
    while True:
        try:
            payment_method_choice = Prompt.ask("Seleccione el método de pago", choices=["1", "2", "3"])
            payment_method = "efectivo" if payment_method_choice == "1" else "tarjeta" if payment_method_choice == "2" else "transferencia"
            break
        except ValueError:
            console.print("[red]Error: Selección inválida. Intente nuevamente.[/red]")
    
    # Confirmar compra
    console.print("\n[bold]Resumen de compra:[/bold]")
    console.print(f"Película: {movie.title}")
    console.print(f"Horario: {showtime['date']} {showtime['time']}")
    console.print(f"sillas: {', '.join(seats)}")
    console.print(f"Tipo: {ticket_type} (${price:,.0f})")
    
    if food_items:
        console.print("\n[bold]Comida:[/bold]")
        for item in food_items:
            food = food_controller.get_food_item(item['item_id'])
            console.print(f"- {food.product} x{item['quantity']}: ${item['quantity']*food.price:,.0f}")
    
    total = price + sum(item['quantity']*item['unit_price'] for item in food_items)
    console.print(f"\n[bold]Total: ${total:,.0f}[/bold]")
    
    if Confirm.ask("\n¿Confirmar compra?"):
        # Crear ticket
        ticket = ticket_controller.create_ticket(
            user_id=user.user_id,
            movie_id=movie.movie_id,
            showtime=showtime,
            room_type=movie.room_type,
            seats=seats,
            ticket_type=ticket_type,
            price=price
        )
        
        if ticket:
            # Crear purchase
            purchase = ticket_controller.create_purchase(
                user_id=user.user_id,
                tickets=[ticket],
                food_items=food_items,
                payment_method=payment_method
            )
            
            if purchase:
                console.print("\n[green]¡Compra realizada con éxito![/green]")
                console.print(f"N° de compra: {purchase.purchase_id}")
            else:
                console.print("\n[red]Error al registrar la compra[/red]")
        else:
            console.print("\n[red]Error al crear el ticket[/red]")
    
    Prompt.ask("\nPresione Enter para continuar...")

#  funcion para reservaciones
def handle_reserve_tickets(console: Console, ticket_controller, user, movie_controller):
    """Proceso de reserva de tickets"""
    console.clear()
    console.print(Panel.fit("🎬 RESERVAR ENTRADAS", style="bold green"))
    
    # Seleccionar película
    movies = movie_controller.get_active_movies()
    if not movies:
        console.print("[red]No hay películas disponibles[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    console.print("\n[bold]Películas disponibles:[/bold]")
    for i, movie in enumerate(movies, 1):
        console.print(f"{i}. {movie.title} ({movie.room_type})")
    
    selection = Prompt.ask("\nSeleccione una película", choices=[str(i) for i in range(1, len(movies)+1)])
    movie = movies[int(selection)-1]
    
    # Seleccionar función
    console.print("\n[bold]Horarios disponibles:[/bold]")
    for i, showtime in enumerate(movie.showtimes, 1):
        console.print(f"{i}. {showtime['date']} {showtime['time']} ({showtime['session']})")
    
    selection = Prompt.ask("\nSeleccione un horario", choices=[str(i) for i in range(1, len(movie.showtimes)+1)])
    showtime = movie.showtimes[int(selection)-1]
    
    # Seleccionar sillas (implementar lógica de asientos)
    seats = ["A1", "A2"]  # Ejemplo simplificado
    
    # Confirmar reserva
    console.print("\n[bold]Resumen de reserva:[/bold]")
    console.print(f"Película: {movie.title}")
    console.print(f"Horario: {showtime['date']} {showtime['time']}")
    console.print(f"sillas: {', '.join(seats)}")
    
    if Confirm.ask("\n¿Confirmar reserva?"):
        # Crear reservación
        reservation = ticket_controller.create_reservation(
            user_id=user.user_id,
            movie_id=movie.movie_id,
            showtime=showtime,
            seats=seats
        )
        
        if reservation:
            console.print("\n[green]¡Reservación realizada con éxito![/green]")
            console.print(f"N° de reservación: {reservation.reservation_id}")
        else:
            console.print("\n[red]Error al crear la reservación[/red]") 
            
# funciones para visualización tickets y reservaciones
def display_user_purchases(console: Console, ticket_controller, user):
    """Mostrar compras del usuario"""
    console.clear()
    console.print(Panel.fit("🛍️ MIS COMPRAS", style="bold green"))
    
    purchases = ticket_controller.get_user_purchases(user.user_id)
    
    if not purchases:
        console.print("[red]No tiene compras registradas[/red]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    table = Table(title="Mis Compras", show_header=True, header_style="bold magenta")
    table.add_column("N° de compra", style="dim")
    table.add_column("Fecha", justify="right")
    table.add_column("Total", justify="right")
    
    for purchase in purchases:
        table.add_row(str(purchase.purchase_id), purchase.purchase_date, f"${purchase.total_amount:,.0f}")
    
    console.print(table)
    Prompt.ask("\nPresione Enter para continuar...")