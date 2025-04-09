from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from models.user import User, Admin
from views.movie_view import display_movie_management
from views.food_menu_view import display_food_menu_management

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
    
    while True:
        console.clear()
        console.print(Panel.fit(f"BIENVENIDO {user.name.upper()}", 
                            style="bold blue"))
        
        if isinstance(user, Admin):
            console.print("\n1. Gestión de Películas")
            console.print("2. Gestión de Menú")
            console.print("3. Gestión de Usuarios")
            console.print("4. Reportes")
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
            console.print("2. Menú de Comidas")
            console.print("3. Mi Perfil")
            console.print("4. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=False)
            elif option == "2":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_menu_controller, is_admin=False)
            elif option == "3":
                from views.user_view import display_user_management
                display_user_management(console, user_controller, user)
            elif option == "4":
                return