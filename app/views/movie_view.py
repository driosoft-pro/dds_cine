from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from datetime import datetime

# Importando recursos necesarios
from core.database import Database
from controllers.cinema_controller import CinemaController

# Configuración
from config import Config

class MovieView:
    """Vista para gestión de películas."""
    
    def __init__(self):
        self.db = Database(str(Config.DATA_DIR))
        self.console = Console()
        self.cinema_controller = CinemaController(self.db)
    

    def show_movie_menu(self, is_admin: bool):
        """Muestra el menú de películas según el tipo de usuario con estilo uniforme."""
        titulo = "Gestión de Películas" if is_admin else "Cartelera"
        table = Table(
            title=titulo,
            border_style="magenta",
            box=box.ROUNDED,
        )
        table.add_column("ID", justify="center")
        table.add_column("Descripción")

        if is_admin:
            opciones = [
                ("1", "Listar películas"),
                ("2", "Buscar película"),
                ("3", "Agregar película"),
                ("4", "Actualizar película"),
                ("5", "Desactivar película"),
                ("0", "Volver al menú principal"),
            ]
            valid_choices = ["1", "2", "3", "4", "5", "0"]
        else:
            opciones = [
                ("1", "Ver cartelera completa"),
                ("2", "Buscar por categoría"),
                ("0", "Volver al menú principal"),
            ]
            valid_choices = ["1", "2", "3", "0"]

        for id, descripcion in opciones:
            table.add_row(id, descripcion)

        self.console.print(table)

        while True:
            opcion = Prompt.ask("Seleccione una ID \no escriba 'volver' para regresar al menu").strip()
            if opcion in valid_choices:
                return opcion
            else:
                self.console.print("[red]ID inválida. Intente nuevamente.[/]")

    def show_movies(self, movies: list, showtimes: list = None):
        """Muestra una lista de películas con sus horarios."""
        if not movies:
            self.console.print("[yellow]No hay películas disponibles[/]")
            return
        
        table = Table(title="[bold]Cartelera[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Título", style="magenta")
        table.add_column("Duración", style="white")
        table.add_column("Categoria", style="cyan")	
        table.add_column("Clasificación", style="white")
        table.add_column("Idioma", style="magenta")
        table.add_column("Sala", style="blue")
        table.add_column("Horarios", style="yellow")
        table.add_column("Precio", style="yellow")
        
        for movie in movies:
            # Filtrar horarios para esta película
            movie_showtimes = []
            if showtimes:
                movie_showtimes = [st for st in showtimes if st.get('movie_id') == movie.get('movie_id')]
            
            # Formatear horarios para mostrar
            showtimes_str = "Sin horarios"
            if movie_showtimes:
                showtimes_str = "\n".join(
                    f"{st.get('date', 'N/D')} {st.get('start_time', 'N/D')} ({st.get('jornada', 'N/D')})"
                    #for st in sorted(movie_showtimes,  # Mostrar todos los horarios
                    for st in sorted(movie_showtimes[:3],  # Mostrar máximo 3 horarios
                                    key=lambda x: (x.get('date', ''), x.get('start_time', '')))
                )
            
            table.add_row(
                str(movie.get('movie_id', 'N/D')),
                movie.get('title', 'N/D'),
                f"{movie.get('duration', 0)} min",
                movie.get('category', 'N/D'),
                movie.get('age_rating', 'N/D'),
                movie.get('language', 'N/D'),
                movie.get('room_type', 'N/D'),
                showtimes_str,
                f"${movie.get('ticket_price', 0):,.0f}"
            )
        
        self.console.print(table)
        
    def show_movie_details(self, movie: dict):
        """Muestra los detalles de una película."""
        panel = Panel.fit(
            f"[bold]{movie['title']}[/] ({movie['release_year']})\n"
            f"Director: [cyan]{movie['director']}[/]\n"
            f"Duración: [white]{movie['duration']} min[/] | "
            f"Clasificación: [green]{movie['age_rating']}[/]\n"
            f"Sala: [blue]{movie['room_type']}[/] | "
            f"Precio: [yellow]${movie['ticket_price']:,.0f}[/]\n\n"
            f"[bold]Sinopsis:[/]\n[white]{movie['synopsis']}[/]",
            title="Detalles de la Película",
            border_style="blue"
        )
        self.console.print(panel)
    
    def get_movie_search_criteria(self):
        """Obtiene criterios de búsqueda de película o vuelve al menú si se presiona Enter."""
        self.console.print("\n[bold]Buscar Película[/]")
        self.console.print("1. Por título")
        self.console.print("2. Por categoría")
        self.console.print("[dim]Presione Enter sin escribir nada para volver.[/]\n")

        while True:
            choice = Prompt.ask("Seleccione criterio (1-2)").strip()
            if choice == "":
                self.console.print("[yellow]Volviendo al menú...[/]")
                return None 
            elif choice == "1":
                titulo = Prompt.ask("Ingrese título o parte del título").strip()
                return {'title': titulo}
            elif choice == "2":
                categoria = Prompt.ask("Ingrese categoría").strip()
                return {'category': categoria}
            else:
                self.console.print("[red]Opción inválida. Intente nuevamente.[/]")
        
    def get_movie_data(self):
        """Obtiene datos para crear/actualizar una película con validaciones y opción de volver."""

        def cancelar_si_volver(valor):
            return valor.strip().lower() == 'volver'

        # Título
        while True:
            title = Prompt.ask("Título de la película").strip()
            if cancelar_si_volver(title):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not title:
                self.console.print("[yellow]Debes ingresar un título válido.[/]")
            else:
                break

        # Director
        while True:
            director = Prompt.ask("Director").strip()
            if cancelar_si_volver(director):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not director:
                self.console.print("[yellow]Debes ingresar un director válido.[/]")
            else:
                break

        # Año de lanzamiento
        while True:
            release_year_input = Prompt.ask("Año de lanzamiento").strip()
            if cancelar_si_volver(release_year_input):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not release_year_input.isdigit():
                self.console.print("[yellow]Ingresa un año válido.[/]")
            else:
                release_year = int(release_year_input)
                break

        # Categoría
        category_list = ["Acción", "Comedia", "Drama", "Documental", "Terror", "Animación"]
        self.console.print("\n[bold]Categorías disponibles:[/]")
        for i, cat in enumerate(category_list, start=1):
            self.console.print(f"{i}. {cat}")
        while True:
            opcion = Prompt.ask("Ingresa el número de la categoría").strip()
            if cancelar_si_volver(opcion):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not opcion.isdigit() or not (1 <= int(opcion) <= len(category_list)):
                self.console.print("[yellow]Número de categoría inválido.[/]")
            else:
                category = category_list[int(opcion) - 1]
                break

        # Sinopsis
        while True:
            synopsis = Prompt.ask("Sinopsis").strip()
            if cancelar_si_volver(synopsis):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not synopsis:
                self.console.print("[yellow]Debes ingresar una sinopsis válida.[/]")
            else:
                break

        # Duración
        while True:
            duration_input = Prompt.ask("Duración (minutos)").strip()
            if cancelar_si_volver(duration_input):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not duration_input.isdigit():
                self.console.print("[yellow]Duración no válida.[/]")
            else:
                duration = int(duration_input)
                break

        # Clasificación
        clasificaciones = [("G", "Apta para todo público"), ("PG", "Supervisión de los padres sugerida"),
                        ("PG-13", "No recomendada para menores de 13 años"), ("R", "Restringida a menores de 17 años"),
                        ("C", "Solo para adultos")]
        self.console.print("\n[bold]Clasificaciones disponibles:[/]")
        for i, (clave, descripcion) in enumerate(clasificaciones, start=1):
            self.console.print(f"{i}. [cyan]{clave}[/] - {descripcion}")
        while True:
            opcion = Prompt.ask("Ingresa el número de la clasificación").strip()
            if cancelar_si_volver(opcion):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not opcion.isdigit() or not (1 <= int(opcion) <= len(clasificaciones)):
                self.console.print("[yellow]Número no válido.[/]")
            else:
                age_rating = clasificaciones[int(opcion) - 1][0]
                break

        # Idioma
        idiomas = [("Esp", "Español"), ("Ing", "Inglés")]
        self.console.print("\n[bold]Idiomas disponibles:[/]")
        for i, (clave, nombre) in enumerate(idiomas, start=1):
            self.console.print(f"{i}. [cyan]{clave}[/] - {nombre}")
        while True:
            idioma_opcion = Prompt.ask("Ingresa el número del idioma").strip()
            if cancelar_si_volver(idioma_opcion):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not idioma_opcion.isdigit() or not (1 <= int(idioma_opcion) <= len(idiomas)):
                self.console.print("[yellow]Número no válido.[/]")
            else:
                language = idiomas[int(idioma_opcion) - 1][0]
                break

        # País de origen
        while True:
            origin = Prompt.ask("País de origen").strip()
            if cancelar_si_volver(origin):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not origin:
                self.console.print("[yellow]Debes ingresar un país de origen válido.[/]")
            else:
                break

        # Tipo de sala
        tipos_sala = [("2D", "Proyección en dos dimensiones"), ("3D", "Proyección en tres dimensiones")]
        self.console.print("\n[bold]Tipos de sala disponibles:[/]")
        for i, (clave, descripcion) in enumerate(tipos_sala, start=1):
            self.console.print(f"{i}. [cyan]{clave}[/] - {descripcion}")
        while True:
            sala_opcion = Prompt.ask("Ingresa el número del tipo de sala").strip()
            if cancelar_si_volver(sala_opcion):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not sala_opcion.isdigit() or not (1 <= int(sala_opcion) <= len(tipos_sala)):
                self.console.print("[yellow]Número no válido.[/]")
            else:
                room_type = tipos_sala[int(sala_opcion) - 1][0]
                break

        # Tipo de hall
        tipos_hall = [("regular", "Sala regular"), ("preferencial", "Sala preferencial")]
        self.console.print("\n[bold]Tipos de hall disponibles:[/]")
        for i, (clave, descripcion) in enumerate(tipos_hall, start=1):
            self.console.print(f"{i}. [cyan]{clave.capitalize()}[/] - {descripcion}")
        while True:
            hall_opcion = Prompt.ask("Ingresa el número del tipo de sala (hall)").strip()
            if cancelar_si_volver(hall_opcion):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not hall_opcion.isdigit() or not (1 <= int(hall_opcion) <= len(tipos_hall)):
                self.console.print("[yellow]Número no válido.[/]")
            else:
                hall = tipos_hall[int(hall_opcion) - 1][0]
                break

        # Precio ticket
        while True:
            ticket_input = Prompt.ask("Precio base del ticket").strip()
            if cancelar_si_volver(ticket_input):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            try:
                ticket_price = float(ticket_input)
                break
            except ValueError:
                self.console.print("[yellow]Precio no válido.[/]")

        # Asientos generales
        while True:
            general_input = Prompt.ask("Cantidad de asientos generales disponibles").strip()
            if cancelar_si_volver(general_input):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if general_input.isdigit():
                general_seats = int(general_input)
                break
            else:
                self.console.print("[yellow]Número inválido para asientos generales.[/]")

        # Asientos preferenciales
        while True:
            pref_input = Prompt.ask("Cantidad de asientos preferenciales disponibles").strip()
            if cancelar_si_volver(pref_input):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if pref_input.isdigit():
                pref_seats = int(pref_input)
                break
            else:
                self.console.print("[yellow]Número inválido para asientos preferenciales.[/]")

        # Horarios
        showtimes = []
        self.console.print("\n[bold]Agregar horarios (máximo 3, escribe 'volver' o deja vacío para terminar):[/]")
        for i in range(3):
            date = Prompt.ask(f"Fecha del horario #{i+1} (YYYY-MM-DD, vacío para salir)", default="").strip()
            if cancelar_si_volver(date):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            if not date:
                break
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.console.print("[yellow]Formato de fecha inválido. Usa YYYY-MM-DD.[/]")
                break

            start_time = Prompt.ask("Hora de inicio (HH:MM)").strip()
            if cancelar_si_volver(start_time):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            try:
                datetime.strptime(start_time, "%H:%M")
            except ValueError:
                self.console.print("[yellow]Formato de hora inválido. Usa HH:MM.[/]")
                break

            end_time = Prompt.ask("Hora de fin (HH:MM)").strip()
            if cancelar_si_volver(end_time):
                self.console.print("[red]Operación cancelada.[/]")
                return None
            try:
                datetime.strptime(end_time, "%H:%M")
            except ValueError:
                self.console.print("[yellow]Formato de hora inválido. Usa HH:MM.[/]")
                break

            jornada = Prompt.ask("Jornada (mañana/tarde/noche)", choices=["mañana", "tarde", "noche"]).strip()
            if cancelar_si_volver(jornada):
                self.console.print("[red]Operación cancelada.[/]")
                return None

            showtimes.append({
                "showtime_id": i + 1,
                "movie_id": 0,
                "cinema_id": 0,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "jornada": jornada,
                "available_seats": {
                    "general": general_seats,
                    "preferencial": pref_seats
                }
            })

        # Resultado final
        return {
            'title': title,
            'director': director,
            'release_year': release_year,
            'category': category,
            'synopsis': synopsis,
            'duration': duration,
            'age_rating': age_rating,
            'language': language,
            'origin': origin,
            'room_type': room_type,
            'hall': hall,
            'ticket_price': ticket_price,
            'showtimes': showtimes,
            'available_seats': {
                'general': general_seats,
                'preferencial': pref_seats
            },
        }

    def show_showtimes(self, showtimes: list):
        """Muestra los horarios disponibles para una película."""
        if not showtimes:
            self.console.print("[yellow]No hay horarios disponibles para esta película[/]")
            return
        
        table = Table(title="[bold]Horarios Disponibles[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Fecha", style="magenta")
        table.add_column("Hora", style="white")
        table.add_column("Jornada", style="green")
        table.add_column("Disponibilidad", style="yellow")
        
        for st in showtimes:
            available = sum(st.get('available_seats', {}).values())
            table.add_row(
                str(st.get('showtime_id', '')),
                st.get('date', ''),
                f"{st.get('start_time', '')}-{st.get('end_time', '')}",
                st.get('jornada', ''),
                f"{available} Boletas" if available > 0 else "Sin Boletas"
            )
        
        self.console.print(table)
        
    def show_showtimes(self, showtimes: list):
        """Muestra los horarios disponibles para una película."""
        if not showtimes:
            self.console.print("[yellow]No hay horarios disponibles para esta película[/]")
            return
        
        table = Table(title="[bold]Horarios Disponibles[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Fecha", style="magenta")
        table.add_column("Hora", style="white")
        table.add_column("Jornada", style="green")
        table.add_column("Disponibilidad", style="yellow")
        
        for st in showtimes:
            # Obtener el cine correspondiente para la capacidad total
            cinema = self.cinema_controller.get_cinema_by_id(st['cinema_id'])
            if not cinema:
                continue
                
            # Calcular disponibilidad
            total_capacity = sum(cinema['capacity'].values())
            available_seats = st.get('available_seats', {})
            current_available = sum(available_seats.values()) if available_seats else total_capacity
            
            # Mostrar "100 Boletas" si está completo, o el valor real si hay reservas
            disponibilidad = f"{current_available} Boletas" if current_available < total_capacity else f"{total_capacity} Boletas"
            
            table.add_row(
                str(st['showtime_id']),
                st['date'],
                f"{st['start_time']}-{st['end_time']}",
                st['jornada'],
                disponibilidad
            )
        
        self.console.print(table)