from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from getpass import getpass
from datetime import datetime

# Importando recursos necesarios
from core.database import Database
from controllers.user_controller import UserController

# Configuración
from config import Config

class LoginView:
    """Vista para el proceso de login y registro de usuarios."""
    
    def __init__(self):
        self.console = Console()
        self.user_controller = UserController(Database(str(Config.DATA_DIR)))
        self.max_attempts = 3  # Máximo de intentos permitidos
    
    def show_login_menu(self):
        """Muestra el menú de login."""
        self.console.print("[bold]Inicio de Sesión[/]")
        self.console.print("1. Iniciar sesión")
        self.console.print("2. Registrarse")
        self.console.print("0. Salir")
        return Prompt.ask("Seleccione una ID:",choice=["1", "2", "0"])
        
    def show_login(self):
        """Muestra el formulario de login con límite de intentos."""
        self.console.print(Panel.fit("[bold]Iniciar Sesión[/]", border_style="blue"))
        
        for attempt in range(self.max_attempts):
            username = Prompt.ask("[cyan]Usuario[/]").strip()
            
            if not username:
                self.console.print("[red]Error: El usuario no puede estar vacío[/]")
                continue
                
            if not self.user_controller.exists_user(username):
                remaining = self.max_attempts - (attempt + 1)
                self.console.print(f"[red]Error: El usuario no existe. Intentos restantes: {remaining}[/]")
                if remaining == 0:
                    break
                continue
                
            for pwd_attempt in range(self.max_attempts):
                try:
                    self.console.print("[cyan]Contraseña:[/]", end=" ")
                    password = getpass("")
                    if password is None or password.strip() == "":
                        raise ValueError("La contraseña no puede estar vacía")
                        
                    if self.user_controller.check_password_user(username, password):
                        self.show_login_success()
                        return username, password
                        
                    remaining = self.max_attempts - (pwd_attempt + 1)
                    if remaining > 0:
                        self.console.print(f"[red]Contraseña incorrecta. Intentos restantes: {remaining}[/]")
                        
                except (EOFError, KeyboardInterrupt):
                    self.console.print("\n[red]Entrada interrumpida. Abortando proceso de login.[/]")
                    return None, None
                except Exception as e:
                    self.console.print(f"[red]Error al ingresar la contraseña: {e}[/]")
                    break
                    
            if (attempt + 1) < self.max_attempts:
                self.console.print(f"[yellow]Intento {attempt + 1} de {self.max_attempts} fallido. Intente nuevamente.[/]")
        
        self.console.print("[red]Ha excedido el número máximo de intentos. Volviendo al menú principal...[/]")
        return None, None

    def show_register(self):
        """Muestra el formulario de registro."""
        self.console.print(Panel.fit("[bold]Registro de Nuevo Usuario[/]", border_style="blue"))

        while True:
            username = Prompt.ask("[cyan]Nombre de usuario[/]")
            if username.strip() == "":
                self.console.print("[red]Error: El nombre de usuario no puede estar vacío.[/]")
                self.console.print("[cyan]Ejemplo: usuario123[/]")
            elif len(username) < 3:
                self.console.print("[red]Error: El nombre de usuario debe tener al menos 3 caracteres.[/]")
                self.console.print("[cyan]Ejemplo: usuario123[/]")
            else:
                break

        while True:
            identification = Prompt.ask("[cyan]Número de identificación[/]")
            if identification.strip() == "":
                self.console.print("[red]Error: El número de identificación no puede estar vacío.[/]")
                self.console.print("[cyan]Ejemplo: 12345678[/]")
            elif not identification.isdigit():
                self.console.print("[red]Error: El número de identificación debe ser un número.[/]")
                self.console.print("[cyan]Ejemplo: 12345678[/]")
            else:
                break

        while True:
            name = Prompt.ask("[cyan]Nombre completo[/]")
            if name.strip() == "":
                self.console.print("[red]Error: El nombre completo no puede estar vacío.[/]")
                self.console.print("[cyan]Ejemplo: Juan Pérez[/]")
            else:
                break

        while True:
            email = Prompt.ask("[cyan]Correo electrónico[/]")
            if email.strip() == "":
                self.console.print("[red]Error: El correo electrónico no puede estar vacío.[/]")
                self.console.print("[cyan]Ejemplo: ejemplo@dds.com[/]")
            elif "@" not in email:
                self.console.print("[red]Error: El correo electrónico debe contener el símbolo @.[/]")
                self.console.print("[cyan]Ejemplo: ejemplo@dds.com[/]")
            else:
                break

        while True:
            birth_date = Prompt.ask("[cyan]Fecha de nacimiento (YYYY-MM-DD)[/]")
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
                break
            except ValueError:
                self.console.print("[red]Error: La fecha de nacimiento debe estar en el formato YYYY-MM-DD.[/]")
                self.console.print("[cyan]Ejemplo: 1990-01-01[/]")

        while True:
            try:
                self.console.print("[cyan]Contraseña:[/]", end=" ")
                password = getpass("")
                if password is None or password.strip() == "":
                    self.console.print("[red]Error: La contraseña no puede estar vacía.[/]")
                    continue
                elif len(password) < 8:
                    self.console.print("[red]Error: La contraseña debe tener al menos 8 caracteres.[/]")
                    continue
                break
            except Exception as e:
                self.console.print(f"[red]Error al leer la contraseña: {e}[/]")

        while True:
            try:
                confirm_password = getpass("[cyan]Confirmar contraseña:[/]")
                if confirm_password is None or confirm_password.strip() == "":
                    self.console.print("[red]Error: La confirmación de la contraseña no puede estar vacía.[/]")
                    continue
                if confirm_password != password:
                    self.console.print("[red]Error: Las contraseñas no coinciden.[/]")
                else:
                    break
            except Exception as e:
                self.console.print(f"[red]Error al confirmar la contraseña: {e}[/]")

        self.show_register_success()
        # Aquí iría el llamado para guardar el nuevo usuario

    def show_login_success(self):
        """Muestra mensaje de login exitoso."""
        self.console.print(f"\n[green]✓ Conexión exitosa...")

    def show_login_error(self):
        """Muestra mensaje de error en login."""
        self.console.print("[red]Usuario o contraseña incorrectos.[/]")

    def show_register_success(self):
        """Muestra mensaje de registro exitoso."""
        self.console.print("[green]Registro completado con éxito![/]")
