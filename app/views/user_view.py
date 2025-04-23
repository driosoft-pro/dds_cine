import pwinput
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from datetime import datetime
from rich import box
from typing import Optional

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
    
    def get_user_data(self,for_update: bool = False,current_data: Optional[dict] = None) -> Optional[dict]:
            """
            Si for_update=True y current_data provisto, muestra los defaults.
            Devuelve None si el usuario escribe 'volver'.
            """
            def ask(field_label: str, key: str, password: bool = False, optional: bool = False):
                """
                Prompt con default=current_data[key] cuando corresponda.
                """
                default_val = None
                if for_update and current_data and key in current_data:
                    default_val = str(current_data[key])

                if password:
                    prompt_text = f"{field_label}"
                    self.console.print(f"[cyan]{prompt_text}[/] ", end="")
                    val = pwinput.pwinput(prompt="", mask="*").strip() or default_val or ""
                else:
                    prompt_text = f"{field_label}"
                    if default_val:
                        prompt_text += f" [{default_val}]"
                    val = Prompt.ask(prompt_text, default=default_val).strip()

                # Cancelación
                if val.lower() == "volver":
                    return None
                if not optional and val == "":
                    # Re-llamar a sí mismo hasta que no sea vacío
                    self.console.print("[red]Este campo no puede estar vacío.[/]")
                    return ask(field_label, key, password, optional)
                return val

            data = {}

            # Sólo solicitamos usuario/clave en modo creación
            if not for_update:
                username = ask("Nombre de usuario", "username", password=False)
                if username is None: return None
                password = ask("Contraseña", "password", password=True)
                if password is None: return None
                data["username"] = username
                data["password"] = password

            # Para actualización o creación, pedimos siempre estos campos, usando defaults si for_update
            identification = ask("Número de identificación", "identification")
            if identification is None: return None

            name = ask("Nombre completo", "name")
            if name is None: return None

            email = ask("Correo electrónico", "email")
            if email is None: return None

            # Fecha de nacimiento
            while True:
                bd_str = ask("Fecha de nacimiento (YYYY-MM-DD)", "birth_date")
                if bd_str is None: return None
                try:
                    # permitimos default en modo update
                    bd = datetime.strptime(bd_str, "%Y-%m-%d")
                    data["birth_date"] = bd.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    self.console.print("[red]Formato inválido. Use YYYY-MM-DD[/]")

            # Sólo admins pueden setear is_admin
            if for_update:
                # En modo update, si current_data tiene is_admin, lo usamos como default
                default_admin = current_data.get("is_admin", False) if current_data else False
                is_admin_str = Prompt.ask(
                    f"¿Es administrador? [s/n] [{ 's' if default_admin else 'n' }]",
                    choices=["s", "n"],
                    default="s" if default_admin else "n"
                ).strip()
                is_admin = is_admin_str.lower() == "s"
            else:
                is_admin = False

            data.update({
                "identification": identification,
                "name": name,
                "email": email,
                "is_admin": is_admin
            })

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