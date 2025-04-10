from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from models.user import User, Admin
from controllers.user_controller import UserController
from controllers.movie_controller import MovieController
from controllers.food_menu_controller import FoodMenuController
from controllers.ticket_controller import TicketController
from controllers.cinema_controller import CinemaController
from datetime import datetime

def display_main_menu(console: Console, auth_service, user: User):
    # Inicializar controladores
    user_controller = UserController(auth_service.user_controller.db)
    movie_controller = MovieController(auth_service.user_controller.db)
    food_controller = FoodMenuController(auth_service.user_controller.db)
    cinema_controller = CinemaController()
    ticket_controller = TicketController(auth_service.user_controller.db, cinema_controller)

    while True:
        console.clear()
        console.print(Panel.fit(f"BIENVENIDO {user.name.upper()}", 
                                style="bold blue"))
        
        if isinstance(user, Admin):
            # Menú de administrador
            console.print("\n1. Gestión de Películas")
            console.print("2. Gestión de Menú de Comida")
            console.print("3. Gestión de Usuarios")
            console.print("4. Reportes de Ventas")
            console.print("5. Gestión de Salas")
            console.print("6. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", 
                                choices=["1", "2", "3", "4", "5", "6"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=True)
            elif option == "2":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_controller, is_admin=True)
            elif option == "3":
                from views.user_view import display_user_management
                display_user_management(console, user_controller, user)
            elif option == "4":
                from views.ticket_view import display_sales_report
                display_sales_report(console, ticket_controller)
            elif option == "5":
                from views.cinema_view import display_cinema_management
                display_cinema_management(console, cinema_controller)
            elif option == "6":
                return
        else:
            # Menú de cliente
            console.print("\n1. Ver Cartelera")
            console.print("2. Comprar Entradas")
            console.print("3. Reservar Entradas")
            console.print("4. Menú de Comidas")
            console.print("5. Mis Compras y Reservaciones")
            console.print("6. Mi Perfil")
            console.print("7. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", 
                                choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=False)
            elif option == "2":
                from views.ticket_menu import handle_purchase
                handle_purchase(console, ticket_controller, user, movie_controller, food_controller)
            elif option == "3":
                from views.ticket_menu import handle_reservation
                handle_reservation(console, ticket_controller, user, movie_controller)
            elif option == "4":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_controller, is_admin=False)
            elif option == "5":
                from views.ticket_menu import display_user_tickets
                display_user_tickets(console, ticket_controller, user)
            elif option == "6":
                from views.user_view import display_user_management
                display_user_management(console, user_controller, user)
            elif option == "7":
                return