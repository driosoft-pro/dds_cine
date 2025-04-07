from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from models.user import User, Admin
from views.movie_view import display_movie_management

def display_main_menu(console: Console, auth_service, user: User):
    """
    Muestra el menú principal según el tipo de usuario.
    """
    from controllers.movie_controller import MovieController
    movie_controller = MovieController(auth_service.user_controller.db)
    
    while True:
        console.clear()
        console.print(Panel.fit(f"BIENVENIDO {user.name.upper()}", 
                            style="bold blue"))
        
        if isinstance(user, Admin):
            # Menú para administradores
            console.print("\n1. Gestión de Películas")
            console.print("2. Gestión de Usuarios")
            console.print("3. Reportes y Estadísticas")
            console.print("4. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
            
            if option == "1":
                display_movie_management(console, movie_controller, is_admin=True)
            elif option == "4":
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
            console.print("3. Mis Reservaciones")
            console.print("4. Cerrar sesión\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4"])
            
            if option == "1":
                display_movie_management(console, movie_controller, is_admin=False)
            elif option == "4":
                console.print("\n[bold green]Sesión cerrada correctamente[/bold green]")
                Prompt.ask("\nPresione Enter para continuar...")
                return
            else:
                console.print("\n[bold yellow]Opción en desarrollo...[/bold yellow]")
                Prompt.ask("\nPresione Enter para continuar...")