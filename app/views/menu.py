from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from models.user import User, Admin
from views.movie_view import display_movie_management
from views.food_menu_view import display_food_menu_management

def display_main_menu(console: Console, auth_service, user: User):
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
            # Menú para administradores
            console.print("\n1. Gestión de Películas")
            console.print("2. Gestión de Menú de Comidas")
            console.print("3. Gestión de Usuarios")
            console.print("4. Reportes y Estadísticas")
            console.print("5. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=True)
            elif option == "2":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_menu_controller, is_admin=True)
            elif option == "5":
                console.print("\n[bold green]Sesión cerrada correctamente[/bold green]")
                Prompt.ask("\nPresione Enter para continuar...")
                return
            else:
                console.print("\n[bold yellow]Opción en desarrollo...[/bold yellow]")
                Prompt.ask("\nPresione Enter para continuar...")
        else:
            # Menú para clientes
            console.print("\n1. Ver Cartelera")
            console.print("2. Comprar Entradas")
            console.print("3. Menú de Comidas")
            console.print("4. Mis Reservaciones")
            console.print("5. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5"])
            
            if option == "1":
                from views.movie_view import display_movie_management
                display_movie_management(console, movie_controller, is_admin=False)
            elif option == "3":
                from views.food_menu_view import display_food_menu_management
                display_food_menu_management(console, food_menu_controller, is_admin=False)
            elif option == "5":
                console.print("\n[bold green]Sesión cerrada correctamente[/bold green]")
                Prompt.ask("\nPresione Enter para continuar...")
                return
            else:
                console.print("\n[bold yellow]Opción en desarrollo...[/bold yellow]")
                Prompt.ask("\nPresione Enter para continuar...")