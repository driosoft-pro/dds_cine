from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
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
        return Prompt.ask("Seleccione una ID", choices=[id for id, _ in opciones])
    
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
    
    def get_user_search_criteria(self):
        """Obtiene criterios de búsqueda de usuario."""
        self.console.print("\n[bold]Buscar Usuario[/]")
        self.console.print("1. Por ID")
        self.console.print("2. Por nombre de usuario")
        self.console.print("3. Por nombre")
        choice = Prompt.ask("Seleccione criterio", choices=["1", "2", "3"])
        
        if choice == "1":
            return {'id': Prompt.ask("Ingrese ID del usuario")}
        elif choice == "2":
            return {'username': Prompt.ask("Ingrese nombre de usuario")}
        else:
            return {'name': Prompt.ask("Ingrese nombre del usuario")}
    
    def get_user_data(self, for_update: bool = False):
        """Obtiene datos de usuario para creación/actualización."""
        data = {}
        if not for_update:
            data['username'] = Prompt.ask("Nombre de usuario")
            data['password'] = Prompt.ask("Contraseña", password=True)
        
        data['identification'] = Prompt.ask("Número de identificación")
        data['name'] = Prompt.ask("Nombre completo")
        data['email'] = Prompt.ask("Correo electrónico")
        data['birth_date'] = Prompt.ask("Fecha de nacimiento (YYYY-MM-DD)")
        data['is_admin'] = Prompt.ask("Es administrador? (s/n)", choices=["s", "n"]) == "s"
        
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