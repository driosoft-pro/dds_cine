from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from datetime import datetime
import pwinput

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
        return Prompt.ask("Seleccione una ID:", choice=["1", "2", "0"])
        
    def show_login(self):
        """Muestra el formulario de login con límite de intentos y opción de 'volver'."""
        self.console.print(Panel.fit("[bold]Iniciar Sesión[/]", border_style="blue"))
        
        for attempt in range(self.max_attempts):
            username = Prompt.ask("[cyan]Usuario[/]").strip()
            
            if username.lower() == "volver":
                return "volver", "volver"

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
                    password = pwinput.pwinput(prompt="", mask="*").strip()

                    if password.lower() == "volver":
                        return "volver", "volver"

                    if password == "":
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
        """Muestra el formulario de registro y devuelve los datos del usuario."""
        self.console.print(Panel.fit("[bold]Registro de Nuevo Usuario[/]", border_style="blue"))

        username = self._ask_with_validation("[cyan]Nombre de usuario[/]", "usuario123", 3)
        if username == "volver": return None

        identification = self._ask_digits("[cyan]Número de identificación[/]", "12345678")
        if identification == "volver": return None

        name = self._ask_required("[cyan]Nombre completo[/]", "Juan Pérez")
        if name == "volver": return None

        email = self._ask_email()
        if email == "volver": return None

        birth_date = self._ask_birth_date()
        if birth_date == "volver": return None

        while True:
            try:
                self.console.print("[cyan]Contraseña:[/]", end=" ")
                password = pwinput.pwinput(prompt="", mask="*")
                if password.strip().lower() == "volver":
                    return None
                if password.strip() == "":
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
                self.console.print("[cyan]Confirmar Contraseña:[/]", end=" ")
                confirm_password = pwinput.pwinput(prompt="", mask="*")
                if confirm_password.strip().lower() == "volver":
                    return None
                if confirm_password.strip() == "":
                    self.console.print("[red]Error: La confirmación no puede estar vacía.[/]")
                    continue
                if confirm_password != password:
                    self.console.print("[red]Error: Las contraseñas no coinciden.[/]")
                else:
                    break
            except Exception as e:
                self.console.print(f"[red]Error al confirmar la contraseña: {e}[/]")

        return {
            'username': username,
            'identification': identification,
            'name': name,
            'email': email,
            'birth_date': birth_date,
            'password': password,
            'confirm_password': confirm_password
        }

    def _ask_required(self, prompt, example):
        while True:
            value = Prompt.ask(prompt)
            if value.strip().lower() == "volver":
                return "volver"
            if value.strip() == "":
                self.console.print(f"[red]Error: Este campo no puede estar vacío.[/]")
                self.console.print(f"[cyan]Ejemplo: {example}[/]")
            else:
                return value

    def _ask_with_validation(self, prompt, example, min_len):
        while True:
            value = Prompt.ask(prompt)
            if value.strip().lower() == "volver":
                return "volver"
            if value.strip() == "":
                self.console.print("[red]Error: Este campo no puede estar vacío.[/]")
            elif len(value) < min_len:
                self.console.print(f"[red]Error: Debe tener al menos {min_len} caracteres.[/]")
            else:
                return value

    def _ask_digits(self, prompt, example):
        while True:
            value = Prompt.ask(prompt)
            if value.strip().lower() == "volver":
                return "volver"
            if value.strip() == "":
                self.console.print("[red]Error: Este campo no puede estar vacío.[/]")
            elif not value.isdigit():
                self.console.print("[red]Error: Debe ser un número.[/]")
            else:
                return value

    def _ask_email(self):
        while True:
            email = Prompt.ask("[cyan]Correo electrónico[/]")
            if email.strip().lower() == "volver":
                return "volver"
            if email.strip() == "":
                self.console.print("[red]Error: El correo electrónico no puede estar vacío.[/]")
            elif "@" not in email:
                self.console.print("[red]Error: Debe contener el símbolo @.[/]")
            else:
                return email

    def _ask_birth_date(self):
        while True:
            birth_date = Prompt.ask("[cyan]Fecha de nacimiento (YYYY-MM-DD)[/]")
            if birth_date.strip().lower() == "volver":
                return "volver"
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
                return birth_date
            except ValueError:
                self.console.print("[red]Error: Formato incorrecto (YYYY-MM-DD)[/]")

    def show_login_success(self):
        """Muestra mensaje de login exitoso."""
        self.console.print(f"\n[green]✓ Conexión exitosa...[/]")

    def show_login_error(self):
        """Muestra mensaje de error en login."""
        self.console.print("[red]Usuario o contraseña incorrectos.[/]")

    def show_register_success(self):
        """Muestra mensaje de registro exitoso."""
        self.console.print("[green]Registro completado con éxito![/]")
