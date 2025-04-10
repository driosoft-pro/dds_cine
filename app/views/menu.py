from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from models.user import User, Admin
from views.movie_view import display_movie_management
from views.food_menu_view import display_food_menu_management
from views.user_view import display_user_management
from views.ticket_view import display_ticket_menu, display_user_purchases   


def display_main_menu(console: Console, auth_service, user: User):
    # controlador de usuarios
    from controllers.user_controller import UserController
    user_controller = UserController(auth_service.user_controller.db)   
    
    # Controlador de peliculas
    from controllers.movie_controller import MovieController
    movie_controller = MovieController(auth_service.user_controller.db)
    
    # Controlador de comida
    from controllers.food_menu_controller import FoodMenuController
    food_menu_controller = FoodMenuController(auth_service.user_controller.db)    

    # Controlador de tickets
    from controllers.ticket_controller import TicketController
    ticket_controller = TicketController(auth_service.user_controller.db)
        
    while True:
        console.clear()
        console.print(Panel.fit(f"BIENVENIDO {user.name.upper()}", 
                            style="bold blue"))
        
        if isinstance(user, Admin):
            console.print("\n1. Gestión de Películas")
            console.print("2. Gestión de Menú")
            console.print("3. Gestión de Usuarios")
            console.print("4. Reportes de Ventas")
            console.print("5. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=True)
            elif option == "2":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_menu_controller, is_admin=True)
            elif option == "3":
                from views.user_view import display_user_management
                display_user_management(console, user_controller, user)
            elif option == "5":
                return
        else:
            console.print("\n1. Cartelera")
            console.print("2. Comprar Entradas")
            console.print("3. Menú de Comidas")
            console.print("4. Mis Compras")
            console.print("5. Mi Perfil")
            console.print("6. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=False)
            if option == "2":
                from views.ticket_view import display_ticket_menu
                display_ticket_menu(console, ticket_controller, user, movie_controller, food_menu_controller)
            elif option == "3":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_menu_controller, is_admin=False)
            elif option == "4":
                from views.ticket_view import display_user_purchases
                display_user_purchases(console, ticket_controller, user)
            elif option == "5":
                from views.user_view import display_user_management
                display_user_management(console, user_controller, user)
            elif option == "6":
                return