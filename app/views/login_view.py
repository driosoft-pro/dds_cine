from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from getpass import getpass

class LoginView:
    """Vista para el proceso de login y registro de usuarios."""
    
    def __init__(self):
        self.console = Console()
    
    def show_login(self):
        """Muestra el formulario de login."""
        self.console.print(Panel.fit("[bold]Iniciar Sesión[/]", border_style="blue"))
        username = Prompt.ask("[cyan]Usuario[/]")
        self.console.print("[cyan]Contraseña:[/]", end=" ")
        password = getpass("")
        return username, password
    
    def show_register(self):
        """Muestra el formulario de registro."""
        self.console.print(Panel.fit("[bold]Registro de Nuevo Usuario[/]", border_style="blue"))
        username = Prompt.ask("[cyan]Nombre de usuario[/]")
        identification = Prompt.ask("[cyan]Número de identificación[/]")
        name = Prompt.ask("[cyan]Nombre completo[/]")
        email = Prompt.ask("[cyan]Correo electrónico[/]")
        birth_date = Prompt.ask("[cyan]Fecha de nacimiento (YYYY-MM-DD)[/]")
        self.console.print("[cyan]Contraseña:[/]", end=" ")
        password = getpass("")
        self.console.print("[cyan]Confirmar contraseña:[/]", end=" ")
        confirm_password = getpass("")
        
        return {
            'username': username,
            'identification': identification,
            'name': name,
            'email': email,
            'birth_date': birth_date,
            'password': password,
            'confirm_password': confirm_password
        }
    
    def show_login_success(self, username: str):
        """Muestra mensaje de login exitoso."""
        self.console.print(f"[green]Bienvenido, {username}![/]")
    
    def show_login_error(self):
        """Muestra mensaje de error en login."""
        self.console.print("[red]Usuario o contraseña incorrectos.[/]")
    
    def show_register_success(self):
        """Muestra mensaje de registro exitoso."""
        self.console.print("[green]Registro completado con éxito![/]")