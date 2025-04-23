import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from datetime import datetime

class MenuView:
    """Vista principal del sistema con menús para cliente y administrador."""
    
    def __init__(self):
        self.console = Console()

    def show_title(self):
        """Muestra el título del sistema."""
        title = pyfiglet.figlet_format("DDS-CINE", font="slant")
        self.console.print(title)
        
    def show_welcome(self):
        """Muestra la pantalla de bienvenida."""
        self.console.clear()
        self.show_title()
        self.console.print(
            Panel.fit(
                "[bold cyan]DDS-CINE[/] - Sistema de Gestión de Cine",
                subtitle=f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
                border_style="blue"
            )
        )
    
    def show_main_menu(self, is_admin: bool = False):
        """Muestra el menú principal según el tipo de usuario."""
        menu = Table(title="[bold]Menú Principal[/]", box=box.ROUNDED, border_style="blue")
        menu.add_column("ID", style="cyan")
        menu.add_column("Descripción", style="white")
        
        if is_admin:
            menu.add_row("1", "Gestión de Películas")
            menu.add_row("2", "Gestión de Usuarios")
            menu.add_row("3", "Gestión de Menú de Comida")
            menu.add_row("4", "Reportes y Estadísticas")
            menu.add_row("5", "Consultar Disponibilidad")
            menu.add_row("0", "Salir")
        else:
            menu.add_row("1", "Cartelera de Películas")
            menu.add_row("2", "Comprar Entrada")
            menu.add_row("3", "Reservar Entrada")
            menu.add_row("4", "Mis Tickets/Reservas")
            menu.add_row("5", "Menú de Comida")
            menu.add_row("6", "Consultar Disponibilidad")
            menu.add_row("7", "Mi Perfil")
            menu.add_row("0", "Salir")
        
        self.console.print(menu)
    
    def get_user_choice(self, options: list) -> str:
        """Obtiene la ID seleccionada por el usuario."""
        while True:
            choice = self.console.input("[bold cyan]>> Seleccione una ID: [/]")
            if choice in options:
                return choice
            self.console.print("[red]ID inválida. Intente nuevamente.[/]")
    
    def show_message(self, message: str, is_error: bool = False):
        """Muestra un mensaje al usuario."""
        if is_error:
            self.console.print(f"[red]Error: {message}[/]")
        else:
            self.console.print(f"[green]{message}[/]")
    
    def confirm_action(self, message: str) -> bool:
        """Pide confirmación para una acción."""
        response = self.console.input(f"[yellow]? {message} (s/n): [/]").lower()
        return response == 's'
    
    def press_enter_to_continue(self):
        """Espera que el usuario presione Enter para continuar."""
        self.console.input("\n[dim]Presione Enter para volver al menú...[/]")