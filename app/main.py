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

# Configuración
from config import Config

class DDSMovieApp:
    """Clase principal de la aplicación."""
    
    def __init__(self):
        self.console = Console()
        self.running = True
        self.current_user = None
        self.is_admin = False
        
        # Configuración inicial
        Config.initialize_directories()
        
        # Inicializar base de datos
        self.db = Database(str(Config.DATA_DIR))
        
        # Cargar datos iniciales si no existen
        if not any(Config.get_data_file_path(key).exists() for key in Config.DATA_FILES):
            initial_data = create_initial_data()
            self.db.initialize_database(initial_data)
        
        # Inicializar servicios
        self.auth_service = AuthService(self.db)
        self.validation_service = ValidationService()
        
        # Inicializar controladores
        self.user_controller = UserController(self.db)
        self.movie_controller = MovieController(self.db)
        self.cinema_controller = CinemaController(self.db)
        self.food_controller = FoodController(self.db)
        self.ticket_controller = TicketController(self.db)
        self.reservation_controller = ReservationController(self.db)
        self.payment_controller = PaymentController(self.db)
        self.showtime_controller = ShowtimeController(self.db)
        
        # Inicializar vistas
        self.menu_view = MenuView()
        self.login_view = LoginView()
        self.user_view = UserView()
        self.movie_view = MovieView()
        self.ticket_view = TicketView()
        self.reservation_view = ReservationView()
        self.payment_view = PaymentView()
        self.food_view = FoodView()
        self.availability_view = AvailabilityView()
    
    def run(self):
        """Método principal que inicia la aplicación."""
        
        # Loop principal de la aplicación
        while self.running:
            if not self.auth_service.is_authenticated():
                self.handle_auth()
            else:
                self.current_user = self.auth_service.get_current_user()
                self.is_admin = self.auth_service.is_admin()
                self.handle_main_menu()
    
    def handle_auth(self):
        """Maneja el proceso de autenticación."""
        self.menu_view.show_welcome()
        self.console.print(Panel.fit("[bold]Inicio de Sesión[/]", border_style="blue"))

        # Menú de autenticación
        table = Table(box=box.ROUNDED, border_style="blue")
        table.add_column("ID", style="cyan")
        table.add_column("Opciones", style="magenta")

        table.add_row("1", "Iniciar sesión")
        table.add_row("2", "Registrarse")
        table.add_row("0", "Salir")

        self.console.print(table)

        while True:
            choice = Prompt.ask("Seleccione una ID [0/1/2] \nEscriba volver si desea regresar al menu").strip()

            if choice not in ["0", "1", "2"]:
                self.console.print("[red]Por favor seleccione una opción válida: 0, 1 o 2.[/]")
                continue
            break

        if choice == "1":
            username, password = self.login_view.show_login()

            if username == "volver" or password == "volver":
                self.menu_view.show_message("Inicio de sesión cancelado. Volviendo al menú...")
                return

            if username is None or password is None:
                self.menu_view.show_message("Se ha excedido el número de intentos. Intenta más tarde.", is_error=True)
                self.menu_view.press_enter_to_continue()
                return

            user = self.auth_service.login(username, password)

            if user:
                welcome_msg = f"Bienvenido, Administrador {user['name']}!" if user.get('is_admin', False) \
                            else f"Bienvenido, {user['name']}!"
                self.console.print(f"[green]{welcome_msg}[/]")
                self.current_user = user
                self.is_admin = user.get('is_admin', False)
            else:
                self.login_view.show_login_error()
                self.menu_view.press_enter_to_continue()

        elif choice == "2":
            user_data = self.login_view.show_register()

            if user_data is None or any(value == "volver" for value in user_data.values()):
                self.menu_view.show_message("Registro cancelado. Volviendo al menú...")
                return

            # Validar datos
            valid, msg = self.validation_service.validate_email(user_data['email'])
            if not valid:
                self.menu_view.show_message(msg, is_error=True)
                return

            valid, msg, date = self.validation_service.validate_date(user_data['birth_date'])
            if not valid:
                self.menu_view.show_message(msg, is_error=True)
                return

            if user_data['password'] != user_data['confirm_password']:
                self.menu_view.show_message("Las contraseñas no coinciden", is_error=True)
                return

            try:
                self.auth_service.register_user(
                    username=user_data['username'],
                    identification=user_data['identification'],
                    name=user_data['name'],
                    email=user_data['email'],
                    birth_date=date,
                    password=user_data['password']
                )
                self.login_view.show_register_success()
            except ValueError as e:
                self.menu_view.show_message(str(e), is_error=True)

            self.menu_view.press_enter_to_continue()

        elif choice == "0":
            self.console.print("[yellow]Saliendo del sistema...[/]")
            exit(0)
                    
    def handle_main_menu(self):
        """Maneja el menú principal según el tipo de usuario."""
        while True:
            self.menu_view.show_title()
            self.menu_view.show_main_menu(self.is_admin)
            options = ["1", "2", "3", "4", "5", "6", "0"] if not self.is_admin else ["1", "2", "3", "4", "5", "0"]
            choice = self.menu_view.get_user_choice(options)
            
            if choice == "0":
                self.auth_service.logout()
                break
                
            elif choice == "1":
                if self.is_admin:
                    self.handle_movie_management()
                else:
                    self.handle_movie_listing()
                
            elif choice == "2":
                if self.is_admin:
                    self.handle_user_management()
                else:
                    self.handle_ticket_purchase()
            
            elif choice == "3":
                if self.is_admin:
                    self.handle_food_management()
                else:
                    self.handle_reservation()
            
            elif choice == "4":
                if self.is_admin:
                    self.handle_reports()
                else:
                    self.handle_user_tickets()
            
            elif choice == "5":
                if self.is_admin:
                    self.handle_availability()
                else:
                    self.handle_food_menu()
            
            elif choice == "6" and not self.is_admin:
                self.handle_availability()
    
    def handle_movie_management(self):
        """Maneja la gestión de películas (admin)."""
        while True:

            choice = self.movie_view.show_movie_menu(is_admin=True)
            
            if choice == "1":  # Listar películas
                movies = self.movie_controller.list_movies()
                showtimes = self.showtime_controller.load_data("showtimes.json") 
                self.movie_view.show_movies(movies, showtimes)
                self.menu_view.press_enter_to_continue()
            
            elif choice == "2":  # Buscar película
                criteria = self.movie_view.get_movie_search_criteria()
                if criteria is None:
                    continue
                results = self.movie_controller.search_movies(**criteria)
                showtimes = self.showtime_controller.load_data("showtimes.json") 
                self.movie_view.show_movies(results, showtimes)
                self.menu_view.press_enter_to_continue()
            
            elif choice == "3":  # Agregar película
                movie_data = self.movie_view.get_movie_data()
                try:
                    new_movie = self.movie_controller.create_movie(**movie_data)
                    self.menu_view.show_message("Película creada con éxito!")
                except Exception as e:
                    self.menu_view.show_message(str(e), is_error=True)
                self.menu_view.press_enter_to_continue()
            
            elif choice == "4":  # Actualizar película
                movies = self.movie_controller.list_movies()
                self.movie_view.show_movies(movies)
                movie_id = int(self.console.input("Ingrese ID de la película a actualizar: "))
                
                movie_data = self.movie_view.get_movie_data()
                if self.movie_controller.update_movie(movie_id, **movie_data):
                    self.menu_view.show_message("Película actualizada con éxito!")
                else:
                    self.menu_view.show_message("Error al actualizar la película", is_error=True)
                self.menu_view.press_enter_to_continue()
            
            elif choice == "5":  # Desactivar película
                movies = self.movie_controller.list_movies()
                self.movie_view.show_movies(movies)
                movie_id = int(self.console.input("Ingrese ID de la película a desactivar: "))
                
                if self.movie_controller.delete_movie(movie_id):
                    self.menu_view.show_message("Película desactivada con éxito!")
                else:
                    self.menu_view.show_message("Error al desactivar la película", is_error=True)
                self.menu_view.press_enter_to_continue()

            elif choice == "0": #Volver al menu principal
                return
    
    def handle_user_management(self):
        """Maneja la gestión de usuarios (admin)."""
        while True:

            choice = self.user_view.show_user_menu()
            
            if choice == "1":  # Listar usuarios
                users = self.user_controller.list_users(active_only=False)
                self.user_view.show_users(users)
                self.menu_view.press_enter_to_continue()
            
            elif choice == "2":  # Buscar usuario
                criteria = self.user_view.get_user_search_criteria()
                if not criteria:
                    self.menu_view.show_message("Volviendo al menú anterior...", is_error=False)
                    return

                if 'id' in criteria:
                    user = self.user_controller.get_user_by_id(int(criteria['id']))
                    if user:
                        self.user_view.show_user_details(user)
                    else:
                        self.menu_view.show_message("Usuario no encontrado", is_error=True)
                elif 'username' in criteria:
                    user = self.user_controller.get_user_by_username(criteria['username'])
                    if user:
                        self.user_view.show_user_details(user)
                    else:
                        self.menu_view.show_message("Usuario no encontrado", is_error=True)
                else:
                    users = [u for u in self.user_controller.list_users(active_only=False) 
                            if criteria['name'].lower() in u['name'].lower()]
                    if users:
                        self.user_view.show_users(users)
                    else:
                        self.menu_view.show_message("No se encontraron usuarios", is_error=True)

                self.menu_view.press_enter_to_continue()
            
            elif choice == "3":  # Crear usuario
                user_data = self.user_view.get_user_data()

                if user_data is None:
                    self.menu_view.show_message("Operación cancelada. Volviendo al menú...")
                    return

                try:
                    # Convertir birth_date de string a datetime
                    from datetime import datetime
                    user_data['birth_date'] = datetime.strptime(user_data['birth_date'], "%Y-%m-%d")

                    new_user = self.user_controller.create_user(
                        username=user_data['username'],
                        identification=user_data['identification'],
                        name=user_data['name'],
                        email=user_data['email'],
                        birth_date=user_data['birth_date'],
                        password=user_data['password'],
                        is_admin=user_data['is_admin']
                    )
                    self.menu_view.show_message("Usuario creado con éxito!")
                except Exception as e:
                    self.menu_view.show_message(str(e), is_error=True)

                self.menu_view.press_enter_to_continue()

            elif choice == "4":  # Actualizar usuario
                users = self.user_controller.list_users(active_only=False)
                self.user_view.show_users(users)

                while True:
                    user_id_input = self.console.input("Ingrese ID del usuario a actualizar (escriba 'volver' para regresar al menú): ").strip()
                    if user_id_input.lower() == "volver":
                        return
                    if not user_id_input.isdigit():
                        self.menu_view.show_message("Por favor, ingrese un número válido de ID o 'volver'.", is_error=True)
                        continue
                    user_id = int(user_id_input)
                    break

                user_data = self.user_view.get_user_data(for_update=True)
                if user_data is None:
                    return 

                if self.user_controller.update_user(user_id, **user_data):
                    self.menu_view.show_message("Usuario actualizado con éxito!")
                else:
                    self.menu_view.show_message("Error al actualizar el usuario", is_error=True)

                self.menu_view.press_enter_to_continue()
            
            elif choice == "5":  # Desactivar usuario
                users = self.user_controller.list_users(active_only=False)
                self.user_view.show_users(users)

                while True:
                    user_id_input = self.console.input("Ingrese ID del usuario a desactivar (presione Enter para volver al menú): ").strip()
                    
                    # Si presiona solo Enter, vuelve al menú
                    if user_id_input == "":
                        return

                    if not user_id_input.isdigit():
                        self.menu_view.show_message("Por favor, ingrese un número de ID válido o presione Enter para volver.", is_error=True)
                        continue

                    user_id = int(user_id_input)
                    break

                if self.user_controller.delete_user(user_id):
                    self.menu_view.show_message("Usuario desactivado con éxito!")
                else:
                    self.menu_view.show_message("Error al desactivar el usuario", is_error=True)
                    
                self.menu_view.press_enter_to_continue()
        
    def handle_food_management(self):
        """Maneja la gestión del menú de comida (admin)."""
        choice = self.food_view.show_food_menu(is_admin=True)
        
        if choice == "1":  # Listar items
            items = self.food_controller.list_food_items()
            self.food_view.show_food_items(items)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "2":  # Buscar item
            name = self.console.input("Ingrese nombre o parte del nombre del producto: ")
            results = self.food_controller.search_food_items(name=name)
            self.food_view.show_food_items(results)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "3":  # Agregar item
            item_data = self.food_view.get_food_item_data()
            try:
                new_item = self.food_controller.create_food_item(**item_data)
                self.menu_view.show_message("Ítem agregado al menú con éxito!")
            except Exception as e:
                self.menu_view.show_message(str(e), is_error=True)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "4":  # Actualizar item
            items = self.food_controller.list_food_items()
            self.food_view.show_food_items(items)
            item_id = int(self.console.input("Ingrese ID del ítem a actualizar: "))
            
            item_data = self.food_view.get_food_item_data()
            if self.food_controller.update_food_item(item_id, **item_data):
                self.menu_view.show_message("Ítem actualizado con éxito!")
            else:
                self.menu_view.show_message("Error al actualizar el ítem", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "5":  # Desactivar item
            items = self.food_controller.list_food_items()
            self.food_view.show_food_items(items)
            item_id = int(self.console.input("Ingrese ID del ítem a desactivar: "))
            
            if self.food_controller.delete_food_item(item_id):
                self.menu_view.show_message("Ítem desactivado con éxito!")
            else:
                self.menu_view.show_message("Error al desactivar el ítem", is_error=True)
            self.menu_view.press_enter_to_continue()
    
    def handle_reports(self):
        """Maneja la generación de reportes (admin)."""
        self.console.print("\n[bold]Reportes y Estadísticas[/]")
        self.console.print("1. Reporte de ventas")
        self.console.print("2. Reporte por película")
        self.console.print("3. Reporte por usuario")
        self.console.print("0. Volver")
        
        choice = self.console.input(">> ")
        
        if choice == "1":
            start_date = self.console.input("Fecha inicial (YYYY-MM-DD, vacío para todas): ")
            end_date = self.console.input("Fecha final (YYYY-MM-DD, vacío para todas): ")
            
            # Lógica para generar reporte de ventas
            self.menu_view.show_message("Reporte de ventas generado")
        
        elif choice == "2":
            movies = self.movie_controller.list_movies()
            self.movie_view.show_movies(movies)
            movie_id = int(self.console.input("Ingrese ID de la película (vacío para todas): ") or 0)
            
            # Lógica para generar reporte por película
            self.menu_view.show_message("Reporte por película generado")
        
        elif choice == "3":
            users = self.user_controller.list_users()
            self.user_view.show_users(users)
            user_id = int(self.console.input("Ingrese ID del usuario (vacío para todos): ") or 0)
            
            # Lógica para generar reporte por usuario
            self.menu_view.show_message("Reporte por usuario generado")
        
        self.menu_view.press_enter_to_continue()
    
    def handle_movie_listing(self):
        """Maneja la visualización de la cartelera para clientes."""
        while True:
            
            choice = self.movie_view.show_movie_menu(is_admin=False)
            
            if choice == "0":
                break
                
            elif choice == "1":
                # Mostrar cartelera completa
                movies = self.movie_controller.list_movies()
                showtimes = self.showtime_controller.load_data("showtimes.json")
                
                if not movies:
                    self.menu_view.show_message("No hay películas disponibles", is_error=True)
                else:
                    self.movie_view.show_movies(movies, showtimes)
                
                self.menu_view.press_enter_to_continue()
                
            elif choice == "2":
                # Buscar película
                criteria = self.movie_view.get_movie_search_criteria()
                movies = self.movie_controller.search_movies(**criteria)
                
                if not movies:
                    self.menu_view.show_message("No se encontraron películas", is_error=True)
                else:
                    showtimes = self.showtime_controller.load_data("showtimes.json")
                    self.movie_view.show_movies(movies, showtimes)
                    
                    # Opción para ver detalles
                    movie_id = self.console.input("\nIngrese ID de la película para ver detalles (0 para volver): ")
                    if movie_id != "0":
                        try:
                            movie_id = int(movie_id)
                            movie = next((m for m in movies if m['movie_id'] == movie_id), None)
                            if movie:
                                self.movie_view.show_movie_details(movie)
                                movie_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
                                self.movie_view.show_showtimes(movie_showtimes)
                        except ValueError:
                            self.menu_view.show_message("ID debe ser un número", is_error=True)
                
                self.menu_view.press_enter_to_continue()
    
    def handle_ticket_purchase(self):
        """Maneja el proceso de compra de tickets con reservas para clientes."""
        choice = self.ticket_view.show_ticket_menu()
        
        if choice == "1":  # Comprar ticket
            try:
                # Listar películas y horarios disponibles
                movies = self.movie_controller.list_movies()
                showtimes = self.showtime_controller.load_data("showtimes.json")
                
                # Obtener datos de compra del usuario
                purchase_data = self.ticket_view.get_ticket_purchase_data(movies, showtimes)
                
                # Resto del código permanece igual...
                movie = self.movie_controller.get_movie_by_id(purchase_data['movie_id'])
                
                # Validar horario seleccionado
                selected_showtime = next(
                    (st for st in showtimes if st['movie_id'] == purchase_data['movie_id'] 
                    and st['showtime_id'] == purchase_data['showtime_id']),
                    None
                )
                
                if not selected_showtime:
                    self.menu_view.show_message("Horario no encontrado", is_error=True)
                    return
                
                # Validar sala asociada al horario
                if 'cinema_id' not in selected_showtime:
                    self.menu_view.show_message("Error: El horario no tiene sala asignada", is_error=True)
                    return
                    
                cinema = self.cinema_controller.get_cinema_by_id(selected_showtime['cinema_id'])
                if not cinema:
                    self.menu_view.show_message("Sala no encontrada", is_error=True)
                    return
                
                # Obtener asientos disponibles para el tipo seleccionado
                available_seats = self.cinema_controller.get_available_seats_by_type(
                    selected_showtime['cinema_id'],
                    purchase_data['seat_type']
                )
                
                if not available_seats:
                    self.menu_view.show_message("No hay asientos disponibles", is_error=True)
                    return
                
                # Seleccionar asiento específico
                seat_number = self.ticket_view.select_seat(available_seats)
                
                # Reserva TEMPORAL del asiento (bloqueo por 10 minutos)
                if not self.cinema_controller.temp_reserve_seat(
                    selected_showtime['cinema_id'],
                    purchase_data['seat_type'],
                    seat_number
                ):
                    self.menu_view.show_message("Error al reservar el asiento", is_error=True)
                    return
                
                try:
                    # Calcular precio con validación de fechas
                    user = self.user_controller.get_user_by_id(self.current_user['user_id'])
                    birth_date = datetime.strptime(user['birth_date'], "%Y-%m-%d").date()
                    
                    # Parseo seguro de fecha y hora del showtime
                    showtime_date_str = selected_showtime['date']
                    showtime_time_str = selected_showtime['start_time']
                    
                    # Convertir a objetos datetime/date/time
                    if isinstance(showtime_date_str, str):
                        try:
                            showtime_date = datetime.strptime(showtime_date_str, "%Y-%m-%d").date()
                        except ValueError:
                            showtime_date = datetime.strptime(showtime_date_str, "%Y-%m-%d %H:%M:%S").date()
                    elif hasattr(showtime_date_str, 'strftime'):  # Ya es date/datetime
                        showtime_date = showtime_date_str
                    else:
                        raise ValueError("Formato de fecha inválido")
                    
                    if isinstance(showtime_time_str, str):
                        try:
                            showtime_time = datetime.strptime(showtime_time_str, "%H:%M").time()
                        except ValueError:
                            showtime_time = datetime.strptime(showtime_time_str, "%H:%M:%S").time()
                    elif hasattr(showtime_time_str, 'strftime'):  # Ya es time
                        showtime_time = showtime_time_str
                    else:
                        raise ValueError("Formato de hora inválido")
                    
                    showtime_datetime = datetime.combine(showtime_date, showtime_time)
                    showtime_str = showtime_datetime.strftime("%Y-%m-%d %H:%M")  # Para mostrar al usuario

                    # Calcular precio final con posibles descuentos
                    price = TicketService.calculate_ticket_price(
                        room_type=movie['room_type'],
                        seat_type=purchase_data['seat_type'],
                        birth_date=birth_date,
                        showtime=showtime_datetime
                    )
                    
                    # Mostrar resumen de compra al usuario
                    ticket_summary = {
                        'movie_title': movie['title'],
                        'showtime': showtime_str,
                        'seat_number': seat_number,
                        'ticket_type': purchase_data['seat_type'],
                        'price': price * purchase_data['quantity']
                    }
                    
                    self.ticket_view.show_ticket_summary(ticket_summary)
                    
                    # Confirmación final del usuario
                    if not self.menu_view.confirm_action("Confirmar compra?"):
                        raise Exception("Compra cancelada por el usuario")
                    
                    # Procesar pago según método seleccionado
                    payment_method = self.ticket_view.get_payment_method()
                    payment_data = {
                        'user_id': self.current_user['user_id'],
                        'amount': ticket_summary['price'],
                        'payment_method': payment_method
                    }
                    
                    if payment_method == "1":  # Efectivo
                        cash = self.ticket_view.get_cash_amount(ticket_summary['price'])
                        change = cash - ticket_summary['price']
                        if change < 0:
                            raise ValueError("Monto insuficiente")
                        self.ticket_view.show_change(ticket_summary['price'], cash)
                    
                    # Crear registro del ticket (usando el datetime, no el string)
                    ticket_data = {
                        'user_id': self.current_user['user_id'],
                        'movie_id': purchase_data['movie_id'],
                        'showtime': showtime_datetime, 
                        'seat_number': seat_number,
                        'ticket_type': purchase_data['seat_type'],
                        'price': price
                    }
                    
                    new_ticket = self.ticket_controller.create_ticket(**ticket_data)
                    payment_data['ticket_id'] = new_ticket['ticket_id']
                    
                    # Registrar el pago
                    new_payment = self.payment_controller.create_payment(**payment_data)
                    
                    # Confirmar la reserva (convertir temporal a permanente)
                    if not self.cinema_controller.confirm_reservation(
                        selected_showtime['cinema_id'],
                        purchase_data['seat_type'],
                        seat_number
                    ):
                        raise Exception("Error al confirmar la reserva del asiento")
                    
                    # Mostrar confirmación final
                    self.payment_view.show_payment_summary(new_payment)
                    self.menu_view.show_message("Compra realizada con éxito!")
                    
                except ValueError as e:
                    # Liberar asiento SIEMPRE que haya error
                    self.cinema_controller.release_seat(
                        selected_showtime['cinema_id'],
                        purchase_data['seat_type'],
                        seat_number
                    )
                    self.menu_view.show_message(f"Error en formato de fecha/hora: {str(e)}", is_error=True)
                    return
                except Exception as e:
                    # Liberar asiento SIEMPRE que haya error
                    self.cinema_controller.release_seat(
                        selected_showtime['cinema_id'],
                        purchase_data['seat_type'],
                        seat_number
                    )
                    self.menu_view.show_message(f"Error al procesar la compra: {str(e)}", is_error=True)
                    return
                    
            except Exception as e:
                self.menu_view.show_message(f"Error inesperado: {str(e)}", is_error=True)
            
            self.menu_view.press_enter_to_continue()
        
        elif choice == "2":  # Ver mis tickets
            tickets = self.ticket_controller.get_tickets_by_user(self.current_user['user_id'])
            enriched_tickets = []
            for t in tickets:
                movie = self.movie_controller.get_movie_by_id(t['movie_id'])
                enriched_tickets.append({
                    **t,
                    'movie_title': movie['title'] if movie else "Película no disponible"
                })
            self.ticket_view.show_tickets(enriched_tickets)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "3":  # Cancelar ticket
            tickets = self.ticket_controller.get_tickets_by_user(self.current_user['user_id'])
            if not tickets:
                self.menu_view.show_message("No tienes tickets para cancelar", is_error=True)
                self.menu_view.press_enter_to_continue()
                return
            
            enriched_tickets = []
            for t in tickets:
                movie = self.movie_controller.get_movie_by_id(t['movie_id'])
                enriched_tickets.append({
                    **t,
                    'movie_title': movie['title'] if movie else "Película no disponible"
                })
            
            ticket_id = int(self.console.input("Ingrese ID del ticket a cancelar: "))
            if self.ticket_controller.cancel_ticket(ticket_id):
                self.menu_view.show_message("Ticket cancelado con éxito!")
            else:
                self.menu_view.show_message("Error al cancelar el ticket", is_error=True)
            self.menu_view.press_enter_to_continue()    
    
    def handle_reservation(self):
        """Maneja el proceso completo de reservación con manejo robusto de errores."""
        choice = self.reservation_view.show_reservation_menu()
        
        if choice == "1":  # Hacer reservación
            try:
                # Listar películas y horarios disponibles
                movies = self.movie_controller.list_movies()
                showtimes = self.showtime_controller.load_data("showtimes.json")
                self.movie_view.show_movies(movies, showtimes)
                
                # Obtener datos de reservación
                reservation_data = self.reservation_view.get_reservation_data(movies, showtimes)
                movie = self.movie_controller.get_movie_by_id(reservation_data['movie_id'])
                
                # Validar horario seleccionado
                selected_showtime = next(
                    (st for st in showtimes if st['movie_id'] == reservation_data['movie_id'] 
                    and st['showtime_id'] == reservation_data['showtime_id']),
                    None
                )
                
                if not selected_showtime:
                    self.menu_view.show_message("Horario no encontrado", is_error=True)
                    return
                
                showtime_id = selected_showtime['showtime_id']
                cinema_id = selected_showtime['cinema_id']
                
                # Validar sala
                cinema = self.cinema_controller.get_cinema_by_id(cinema_id)
                if not cinema:
                    self.menu_view.show_message("Sala no encontrada", is_error=True)
                    return
                    
                # Obtener asientos disponibles
                available_seats = self.showtime_controller.get_available_seats(
                    showtime_id,
                    reservation_data['seat_type']
                )
                
                if not available_seats:
                    self.menu_view.show_message("No hay asientos disponibles", is_error=True)
                    return
                    
                # Seleccionar asiento
                seat_number = self.reservation_view.select_seat(available_seats)
                
                # Reserva temporal del asiento
                if not self.cinema_controller.temp_reserve_seat(
                    cinema_id,
                    reservation_data['seat_type'],
                    seat_number
                ):
                    self.menu_view.show_message("Error al reservar el asiento", is_error=True)
                    return
                
                try:
                    # Calcular precio
                    user = self.user_controller.get_user_by_id(self.current_user['user_id'])
                    birth_date = datetime.strptime(user['birth_date'], "%Y-%m-%d").date()
                    
                    # Parseo de fecha/hora
                    showtime_date = selected_showtime['date']
                    showtime_time = selected_showtime['start_time']
                    
                    if isinstance(showtime_date, str):
                        showtime_date = datetime.strptime(showtime_date, "%Y-%m-%d").date()
                    if isinstance(showtime_time, str):
                        showtime_time = datetime.strptime(showtime_time, "%H:%M").time()
                    
                    showtime_datetime = datetime.combine(showtime_date, showtime_time)
                    
                    price = TicketService.calculate_ticket_price(
                        room_type=movie['room_type'],
                        seat_type=reservation_data['seat_type'],
                        birth_date=birth_date,
                        showtime=showtime_datetime
                    )
                    
                    # Mostrar resumen
                    reservation_summary = {
                        'movie_title': movie['title'],
                        'showtime': f"{showtime_date} {showtime_time}",
                        'seat_number': seat_number,
                        'ticket_type': reservation_data['seat_type'],
                        'price': price,
                        'expiration': (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
                    }
                    
                    self.reservation_view.show_reservation_summary(reservation_summary)
                    
                    # Confirmar reserva
                    if not self.menu_view.confirm_action("Confirmar reserva?"):
                        raise Exception("Reserva cancelada por el usuario")
                    
                    # Crear reserva en el sistema
                    new_reservation = self.reservation_controller.create_reservation(
                        user_id=self.current_user['user_id'],
                        movie_id=reservation_data['movie_id'],
                        showtime=f"{showtime_date} {showtime_time}",
                        seat_number=seat_number,
                        ticket_type=reservation_data['seat_type'],
                        price=price,
                        showtime_id=showtime_id,
                        expiration_date=(datetime.now() + timedelta(hours=24)).isoformat()
                    )                
    
                                        
                    # Confirmar reserva del asiento
                    self.cinema_controller.confirm_reservation(
                        cinema_id,
                        reservation_data['seat_type'],
                        seat_number
                    )
                    
                    self.menu_view.show_message("✅ Reserva realizada con éxito! Válida por 24 horas.")
                    
                except Exception as e:
                    # Liberar asiento si hay error
                    self.cinema_controller.release_seat(
                        cinema_id,
                        reservation_data['seat_type'],
                        seat_number
                    )
                    raise e
                    
            except ValueError as e:
                self.menu_view.show_message(f"Error de datos: {str(e)}", is_error=True)
            except Exception as e:
                self.menu_view.show_message(f"Error inesperado: {str(e)}", is_error=True)
            
            self.menu_view.press_enter_to_continue()
        
        elif choice == "2":  # Ver mis reservas
            reservations = self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
            enriched_reservations = []
            for r in reservations:
                movie = self.movie_controller.get_movie_by_id(r['movie_id'])
                enriched_reservations.append({
                    **r,
                    'movie_title': movie['title'] if movie else "Película no disponible",
                    'showtime': r.get('showtime', 'Horario no disponible')
                })
            self.reservation_view.show_reservations(enriched_reservations)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "3":  # Cancelar reserva
            reservations = self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
            if not reservations:
                self.menu_view.show_message("No tienes reservas activas para cancelar", is_error=True)
                self.menu_view.press_enter_to_continue()
                return
            
            reservation_id = self.reservation_view.select_reservation_to_cancel([
                {**r, 'movie_title': self.movie_controller.get_movie_by_id(r['movie_id'])['title']} 
                for r in reservations
            ])
            
            if reservation_id and self.reservation_controller.cancel_reservation(reservation_id):
                self.menu_view.show_message("✅ Reserva cancelada con éxito!")
            else:
                self.menu_view.show_message("Error al cancelar la reserva", is_error=True)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "4":  # Convertir reserva a ticket
            active_reservations = [
                r for r in self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
                if r['status'] == 'activo'
            ]
            
            if not active_reservations:
                self.menu_view.show_message("No tienes reservas activas para convertir", is_error=True)
                self.menu_view.press_enter_to_continue()
                return
            
            reservation_id = self.reservation_view.select_reservation_to_convert([
                {**r, 'movie_title': self.movie_controller.get_movie_by_id(r['movie_id'])['title']} 
                for r in active_reservations
            ])
            
            if reservation_id:
                try:
                    ticket = self.reservation_controller.convert_reservation_to_ticket(reservation_id)
                    if ticket:
                        self.menu_view.show_message("✅ Reserva convertida a ticket con éxito!")
                    else:
                        self.menu_view.show_message("Error al convertir la reserva", is_error=True)
                except Exception as e:
                    self.menu_view.show_message(f"Error: {str(e)}", is_error=True)
            
            self.menu_view.press_enter_to_continue()    
    
    def handle_user_tickets(self):
        """Muestra los tickets y reservas del usuario (cliente)."""
        tickets = self.ticket_controller.get_tickets_by_user(self.current_user['user_id'])
        enriched_tickets = []
        for t in tickets:
            movie = self.movie_controller.get_movie_by_id(t['movie_id'])
            enriched_tickets.append({
                **t,
                'movie_title': movie['title'] if movie else "Película no disponible"
            })
        
        reservations = self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
        enriched_reservations = []
        for r in reservations:
            movie = self.movie_controller.get_movie_by_id(r['movie_id'])
            enriched_reservations.append({
                **r,
                'movie_title': movie['title'] if movie else "Película no disponible"
            })
        
        self.console.print("\n[bold]Mis Tickets y Reservas[/]")
        self.ticket_view.show_tickets(enriched_tickets)
        self.reservation_view.show_reservations(enriched_reservations)
        self.menu_view.press_enter_to_continue()
    
    def handle_food_menu(self):
        """Muestra el menú de comida y permite realizar pedidos (cliente)."""
        choice = self.food_view.show_food_menu(is_admin=False)
        
        if choice == "1":  # Ver menú completo
            items = self.food_controller.list_food_items()
            self.food_view.show_food_items(items)
            self.menu_view.press_enter_to_continue()
        
        elif choice == "2":  # Buscar por categoría
            items = self.food_controller.list_food_items()
            self.food_view.show_food_items(items, by_category=True)
            self.menu_view.press_enter_to_continue()
    
    def handle_availability(self):
        """Muestra la disponibilidad de asientos."""
        try:
            # Obtener películas y showtimes
            movies = self.movie_controller.list_movies()
            showtimes = self.showtime_controller.load_data("showtimes.json")
            
            # Mostrar cartelera con horarios
            self.movie_view.show_movies(movies, showtimes)
            
            # Seleccionar película
            movie_id = int(self.console.input("Ingrese ID de la película: "))
            movie = next((m for m in movies if m['movie_id'] == movie_id), None)
            
            if not movie:
                self.menu_view.show_message("Película no encontrada", is_error=True)
                return
            
            # Mostrar horarios específicos
            movie_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
            self.movie_view.show_showtimes(movie_showtimes)
            
            # Seleccionar horario
            showtime_id = int(self.console.input("Ingrese ID del horario: "))
            showtime = next((st for st in movie_showtimes if st['showtime_id'] == showtime_id), None)
            
            if not showtime:
                self.menu_view.show_message("Horario no encontrado", is_error=True)
                return
            
            # Mostrar disponibilidad
            cinema = next((c for c in self.cinema_controller.list_cinemas() 
                            if c['room_type'] == movie['room_type']), None)
            
            if cinema:
                self.availability_view.show_availability(
                    showtime_id=showtime['showtime_id'],  # Nuevo parámetro
                    cinema_id=cinema['cinema_id'],
                    cinema_name=cinema['name'],
                    movie_title=movie['title'],
                    showtime_str=f"{showtime['date']} {showtime['start_time']}"
                )
            
            self.menu_view.press_enter_to_continue()
            
        except ValueError:
            self.menu_view.show_message("ID debe ser un número", is_error=True)

if __name__ == "__main__":
    try:
        app = DDSMovieApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicación finalizada por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)