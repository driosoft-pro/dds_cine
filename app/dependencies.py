# Rich
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box

# Fechas
from datetime import datetime, timedelta

# Configuración y base de datos
from config import Config
from core.database import Database
from core.initial_data import create_initial_data

# Servicios
from services.auth_service import AuthService
from services.validation_service import ValidationService
from services.ticket_service import TicketService

# Controladores
from controllers.user_controller import UserController
from controllers.movie_controller import MovieController
from controllers.cinema_controller import CinemaController
from controllers.food_controller import FoodController
from controllers.ticket_controller import TicketController
from controllers.reservation_controller import ReservationController
from controllers.payment_controller import PaymentController
from controllers.showtime_controller import ShowtimeController

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