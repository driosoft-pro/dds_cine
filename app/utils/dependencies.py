import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from datetime import datetime, timedelta

# Importaciones de core
from core.database import Database
from core.initial_data import create_initial_data

# Importaciones de servicios
from services.auth_service import AuthService
from services.validation_service import ValidationService
from services.ticket_service import TicketService

# Importaciones de controladores
from controllers.user_controller import UserController
from controllers.movie_controller import MovieController
from controllers.cinema_controller import CinemaController
from controllers.food_controller import FoodController
from controllers.ticket_controller import TicketController
from controllers.reservation_controller import ReservationController
from controllers.payment_controller import PaymentController
from controllers.showtime_controller import ShowtimeController

# Importaciones de vistas
from views.menu_view import MenuView
from views.login_view import LoginView
from views.user_view import UserView
from views.movie_view import MovieView
from views.ticket_view import TicketView
from views.reservation_view import ReservationView
from views.payment_view import PaymentView
from views.food_view import FoodView
from views.availability_view import AvailabilityView

# Importaciones de utilidades
from utils.date_utils import safe_parse_datetime

# Configuración
from config import Config