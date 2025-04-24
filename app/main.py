import sys
from rich.console import Console

# Configuración
from config import Config

# Core
from core.database import Database
from core.initial_data import create_initial_data

# Servicios
from services.auth_service import AuthService
from services.validation_service import ValidationService

# Controladores
from controllers.user_controller import UserController
from controllers.movie_controller import MovieController
from controllers.cinema_controller import CinemaController
from controllers.food_controller import FoodController
from controllers.ticket_controller import TicketController
from controllers.reservation_controller import ReservationController
from controllers.payment_controller import PaymentController
from controllers.showtime_controller import ShowtimeController
from controllers.report_controller import ReportController

# Vistas
from views.menu_view import MenuView
from views.login_view import LoginView
from views.user_view import UserView
from views.movie_view import MovieView
from views.ticket_view import TicketView
from views.reservation_view import ReservationView
from views.payment_view import PaymentView
from views.food_view import FoodView
from views.availability_view import AvailabilityView
from views.report_view import ReportView

# Handlers
from handlers.handle_auth import handle_auth
from handlers.handle_main_menu import handle_main_menu


class DDSMovieApp:
    """Clase principal de la aplicación."""
    
    def __init__(self):
        # Consola y estado
        self.console = Console()
        self.running = True
        self.current_user = None
        self.is_admin = False
        
        # Setup inicial: directorios y base de datos
        Config.initialize_directories()
        self.db = Database(str(Config.DATA_DIR))
        if not any(Config.get_data_file_path(k).exists() for k in Config.DATA_FILES):
            self.db.initialize_database(create_initial_data())
        
        # Servicios
        self.auth_service = AuthService(self.db)
        self.validation_service = ValidationService()
        
        # Controladores
        self.user_controller        = UserController(self.db)
        self.movie_controller       = MovieController(self.db)
        self.cinema_controller      = CinemaController(self.db)
        self.food_controller        = FoodController(self.db)
        self.ticket_controller      = TicketController(self.db)
        self.reservation_controller = ReservationController(self.db)
        self.payment_controller     = PaymentController(self.db)
        self.showtime_controller    = ShowtimeController(self.db)
        self.report_controller      = ReportController(self.db)
        
        # Vistas
        self.menu_view        = MenuView()
        self.login_view       = LoginView()
        self.user_view        = UserView()
        self.movie_view       = MovieView()
        self.ticket_view      = TicketView()
        self.reservation_view = ReservationView()
        self.payment_view     = PaymentView()
        self.food_view        = FoodView()
        self.availability_view= AvailabilityView()
        self.report_view      = ReportView()
    
    def run(self):
        """Método principal que inicia la aplicación."""
        while self.running:
            # Si no está autenticado → handler de auth
            if not self.auth_service.is_authenticated():
                handle_auth(self)
            else:
                # Ya autenticado → actualizar usuario y despachar menú principal
                self.current_user = self.auth_service.get_current_user()
                self.is_admin      = self.auth_service.is_admin()
                handle_main_menu(self)


if __name__ == "__main__":
    try:
        app = DDSMovieApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicación finalizada por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)