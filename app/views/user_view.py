import pwinput
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from datetime import datetime
class UserView:
    """Vista para gestión de usuarios."""
    
    def __init__(self):
        self.console = Console()
    
    def show_user_menu(self):
        """Muestra el menú de gestión de usuarios con estilo uniforme."""
        table = Table(
            title="Gestión de Usuarios",
            border_style="magenta",
            box=box.ROUNDED,
        )
        table.add_column("ID", justify="center")
        table.add_column("Descripción")

        opciones = [
            ("1", "Listar usuarios"),
            ("2", "Buscar usuario"),
            ("3", "Crear usuario"),
            ("4", "Actualizar usuario"),
            ("5", "Desactivar usuario"),
            ("0", "Volver al menú principal"),
        ]

        for id, descripcion in opciones:
            table.add_row(id, descripcion)

        self.console.print(table)

        opciones_validas = [id for id, _ in opciones]
        
        while True:
            opcion = Prompt.ask("Seleccione una opción \nEscriba 'volver' para regresar al menú", default="0")
            if opcion in opciones_validas:
                return opcion
            else:
                self.console.print("[red]Opción inválida. Por favor seleccione una opción del menú.[/red]")
    
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

    def show_user_details(self, user: dict):
        """Muestra los detalles de un usuario."""
        self.console.print("\n[bold]Detalles del Usuario[/]")
        self.console.print(f"ID: [cyan]{user['user_id']}[/]")
        self.console.print(f"Usuario: [magenta]{user['username']}[/]")
        self.console.print(f"Nombre: [white]{user['name']}[/]")
        self.console.print(f"Email: [blue]{user['email']}[/]")
        self.console.print(f"Tipo: [green]{'Admin' if user.get('is_admin') else 'Cliente'}[/]")
        self.console.print(f"Estado: [red]{'Activo' if user['status'] == 'activo' else 'Inactivo'}[/]")