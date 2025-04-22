from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

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
        else:
            opciones = [
                ("1", "Ver cartelera completa"),
                ("2", "Buscar por categoría"),
                ("3", "Buscar por fecha"),
                ("0", "Volver al menú principal"),
            ]

        for id, descripcion in opciones:
            table.add_row(id, descripcion)

        self.console.print(table)
        return Prompt.ask("Seleccione una ID", choices=[id for id, _ in opciones])
        
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
        """Obtiene criterios de búsqueda de película."""
        self.console.print("\n[bold]Buscar Película[/]")
        self.console.print("1. Por título")
        self.console.print("2. Por categoría")
        self.console.print("3. Por fecha")
        choice = Prompt.ask("Seleccione criterio", choices=["1", "2", "3"])
        
        if choice == "1":
            return {'title': Prompt.ask("Ingrese título o parte del título")}
        elif choice == "2":
            return {'category': Prompt.ask("Ingrese categoría")}
        else:
            return {'date': Prompt.ask("Ingrese fecha (YYYY-MM-DD)")}
    
    def get_movie_data(self):
        """Obtiene datos para crear/actualizar una película."""
        data = {
            'title': Prompt.ask("Título de la película"),
            'director': Prompt.ask("Director"),
            'release_year': int(Prompt.ask("Año de lanzamiento")),
            'category': Prompt.ask("Categoría"),
            'synopsis': Prompt.ask("Sinopsis"),
            'duration': int(Prompt.ask("Duración (minutos)")),
            'age_rating': Prompt.ask("Clasificación (G, PG, PG-13, R, C)", choices=["G", "PG", "PG-13", "R", "C"]),
            'language': Prompt.ask("Idioma (Esp/Ing)", choices=["Esp", "Ing"]),
            'origin': Prompt.ask("País de origen"),
            'room_type': Prompt.ask("Tipo de sala (2D/3D)", choices=["2D", "3D"]),
            'hall': Prompt.ask("Tipo de sala (regular/premium)", choices=["regular", "premium"]),
            'ticket_price': float(Prompt.ask("Precio base del ticket"))
        }
        
        return data
    
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