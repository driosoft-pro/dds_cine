from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import pyfiglet

from views.login_view import display_login
from services.auth_service import AuthService
from data.database import Database

def main():
    """Función principal que inicia la aplicación."""
    console = Console()
    
    # Inicializar la base de datos
    db = Database()
    db.initialize()
    
    # Mostrar título de la aplicación
    title = pyfiglet.figlet_format("CINEMA SYSTEM", font="slant")
    console.print(Panel.fit(Text(title, style="bold blue"), 
                    style="bold yellow"))
    
    # Mostrar menú de login
    auth_service = AuthService(db)
    display_login(console, auth_service)

if __name__ == "__main__":
    main()