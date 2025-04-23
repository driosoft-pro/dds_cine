import pwinput
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from datetime import datetime
from rich import box

# Importando recursos necesarios
from core.database import Database
from controllers.user_controller import UserController

# Configuración
from config import Config

class UserView:
    """Vista para gestión de usuarios."""
    
    def __init__(self):
        self.console = Console()
        self.db = Database(str(Config.DATA_DIR))
        self.user_controller = UserController(self.db)
        
    def show_user_menu(self, is_admin: bool):
        """Muestra el menú de gestión de usuarios con estilo uniforme."""
        titulo = "Gestión de Usuarios" if is_admin else "Mi Perfil"
        table = Table(
            title=titulo,
            border_style="magenta",
            box=box.ROUNDED,
        )
        table.add_column("ID", justify="center")
        table.add_column("Descripción")
        if is_admin:
            opciones = [
                ("1", "Listar usuarios"),
                ("2", "Buscar usuario"),
                ("3", "Crear usuario"),
                ("4", "Actualizar usuario"),
                ("5", "Desactivar usuario"),
                ("0", "Volver al menú principal"),
            ]
            valid_choices = ["1", "2", "3", "4", "5", "0"]
        else:
            opciones = [
                ("1", "Mi Perfil"),
                ("2", "Actualizar mi perfil"),
                ("3", "Cambiar contraseña"),
                ("4", "Desactivar mi cuenta"),
                ("0", "Volver al menú principal"),
            ]
            valid_choices = ["1", "2", "0"]
            
        for id, descripcion in opciones:
            table.add_row(id, descripcion)

        self.console.print(table)

        while True:
            opcion = Prompt.ask("Escriba 0 o 'volver' para regresar al menú \nSeleccione una ID ").strip()
            if opcion in valid_choices:
                return opcion
            else:
                self.console.print("[red]ID inválida. Intente nuevamente.[/]")
    
    def show_users(self, users: list):
        """Muestra una lista de usuarios en formato de tabla."""
        table = Table(title="[bold]Lista de Usuarios[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Usuario", style="magenta")
        table.add_column("Nombre", style="white")
        table.add_column("Email", style="blue")
        table.add_column("Tipo", style="green")
        table.add_column("Estado", style="red")
        
        for user in users:
            user_type = "Admin" if user.get('is_admin') else "Cliente"
            status = "Activo" if user['status'] == 'activo' else "Inactivo"
            table.add_row(
                str(user['user_id']),
                user['username'],
                user['name'],
                user['email'],
                user_type,
                status
            )
        
        self.console.print(table)
    
    def get_user_data(self, for_update: bool = False):
            """Obtiene datos de usuario para creación/actualización. Escriba 'volver' en cualquier campo para cancelar y regresar al menú principal."""

            def pedir_campo(nombre, password=False, opcionales=False):
                while True:
                    if password:
                        self.console.print(f"[cyan]{nombre}:[/]", end=" ")
                        valor = pwinput.pwinput(prompt="", mask="*").strip()
                    else:
                        valor = Prompt.ask(f"[cyan]{nombre}[/]").strip()
                    
                    if valor.lower() == "volver":
                        return "volver"
                    if valor == "" and not opcionales:
                        self.console.print("[red]Este campo no puede estar vacío.[/red]")
                    else:
                        return valor

            data = {}

            if not for_update:
                username = pedir_campo("Nombre de usuario")
                if username == "volver": return None

                password = pedir_campo("Contraseña", password=True)
                if password == "volver": return None

                data['username'] = username
                data['password'] = password

            identification = pedir_campo("Número de identificación")
            if identification == "volver": return None

            name = pedir_campo("Nombre completo")
            if name == "volver": return None

            email = pedir_campo("Correo electrónico")
            if email == "volver": return None

            # Fecha de nacimiento validada
            while True:
                birth_date_str = pedir_campo("Fecha de nacimiento (YYYY-MM-DD)")
                if birth_date_str == "volver": return None
                try:
                    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                    data['birth_date'] = birth_date.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    self.console.print("[red]Formato de fecha inválido. Use YYYY-MM-DD.[/red]")

            is_admin_str = Prompt.ask(
                "[cyan]¿Es administrador?[/] — escriba 'volver' para regresar al menú", 
                choices=["s", "n"], 
                default="n"
            )
            if is_admin_str.lower() == "volver": return None
            is_admin = is_admin_str.lower() == "s"

            data['identification'] = identification
            data['name'] = name
            data['email'] = email
            data['is_admin'] = is_admin

            return data

    def show_user_details(self, user: dict, is_admin: bool):
        """Muestra los detalles de un usuario con el estilo de tabla Rich."""
        if is_admin:
            table = Table(title="[bold blue]Detalles del Usuario[/]", box=box.ROUNDED)
            table.add_column("[bold magenta]Info[/]")
            table.add_column("[bold green]Datos[/]")

            table.add_row("[cyan]ID[/]", f"{user.get('user_id', 'N/A')}")
            table.add_row("[cyan]Usuario[/]", f"[magenta]{user.get('username', 'N/A')}[/]")
            table.add_row("[cyan]Nombre[/]", f"[white]{user.get('name', 'N/A')}[/]")
            table.add_row("[cyan]Email[/]", f"[blue]{user.get('email', 'N/A')}[/]")
            table.add_row("[cyan]Tipo[/]", f"[green]{'Admin' if user.get('is_admin') else 'Cliente'}[/]")
            table.add_row("[cyan]Estado[/]", f"[red]{'Activo' if user.get('status') == 'activo' else 'Inactivo'}[/]")
        else:
            table = Table(title="[bold blue]Detalles del Usuario[/]", box=box.ROUNDED)
            table.add_column("[bold magenta]Info[/]")
            table.add_column("[bold green]Datos[/]")

            table.add_row("[cyan]Usuario[/]", f"[magenta]{user.get('username', 'N/A')}[/]")
            table.add_row("[cyan]Nombre[/]", f"[white]{user.get('name', 'N/A')}[/]")
            table.add_row("[cyan]Email[/]", f"[blue]{user.get('email', 'N/A')}[/]")
            table.add_row("[cyan]Tipo[/]", f"[green]{'Admin' if user.get('is_admin') else 'Cliente'}[/]")
            table.add_row("[cyan]Estado[/]", f"[red]{'Activo' if user.get('status') == 'activo' else 'Inactivo'}[/]")

        self.console.print(table)
        
    def get_user_search_criteria(self):
            """Obtiene criterios de búsqueda de usuario o vuelve al menú si se presiona Enter."""
            self.console.print("\n[bold]Buscar Usuario[/]")
            self.console.print("1. Por ID")
            self.console.print("2. Por username")
            self.console.print("3. Por nombre")
            self.console.print("[dim]Presione Enter sin escribir nada para volver.[/]\n")

            while True:
                choice = Prompt.ask("Seleccione criterio (1-3)").strip()
                if choice == "":
                    self.console.print("[yellow]Volviendo al menú...[/]")
                    return None
                elif choice == "1":
                    user_id = Prompt.ask("Ingrese ID de usuario").strip()
                    return {"id": user_id} if user_id else {}
                elif choice == "2":
                    username = Prompt.ask("Ingrese username").strip()
                    return {"username": username} if username else {}
                elif choice == "3":
                    name_part = Prompt.ask("Ingrese parte del nombre").strip()
                    return {"name": name_part} if name_part else {}
                else:
                    self.console.print("[red]Opción inválida. Intente nuevamente.[/]")