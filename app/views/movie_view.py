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
        self.console = Console()
        self.db = Database(str(Config.DATA_DIR))
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
            valid_choices = ["1", "2", "0"]

        for id, descripcion in opciones:
            table.add_row(id, descripcion)

        self.console.print(table)

        while True:
            opcion = Prompt.ask("Escriba 0 o 'volver' para regresar al menú \nSeleccione una ID ").strip()
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
        
    def get_movie_data(self,for_update: bool = False,
                        current_data: dict = None) -> dict | None:
        """
        Pide los datos de la película.
        - Si for_update=False, se comporta como antes.
        - Si for_update=True y current_data tiene datos,
            muestra cada campo con su valor actual como default
            y, si el usuario pulsa Enter, conserva current_data[field].
        """
        def ask_text(label: str, key: str) -> str:
            # valor por defecto
            default = current_data.get(key, "") if (for_update and current_data) else None
            prompt = f"{label}"
            if default:
                prompt += f" [{default}]"
            # Prompt.ask devuelve default si user no escribe nada
            return Prompt.ask(prompt, default=str(default) if default is not None else None).strip()

        def ask_int(label: str, key: str) -> int:
            while True:
                val = ask_text(label, key)
                try:
                    return int(val)
                except (TypeError, ValueError):
                    self.console.print("[yellow]Por favor ingresa un número válido.[/]")

        def ask_choice(label: str, key: str, options: list[str]) -> str:
            default = current_data.get(key) if (for_update and current_data) else None
            # Presentamos las opciones con índices automáticos
            self.console.print(f"\n[bold]{label}[/]")
            for idx, opt in enumerate(options, start=1):
                self.console.print(f"{idx}. {opt}")
            while True:
                choice = Prompt.ask(f"Elige (1-{len(options)})",
                                    choices=[str(i) for i in range(1, len(options)+1)],
                                    default=str(options.index(default)+1) if default in options else None).strip()
                # convertir a índice
                i = int(choice) - 1
                return options[i]

        # 1) Título
        title = ask_text("Título de la película", "title")
        if not title and not for_update: return None

        # 2) Director
        director = ask_text("Director", "director")
        if not director and not for_update: return None

        # 3) Año de lanzamiento
        release_year = ask_int("Año de lanzamiento", "release_year")

        # 4) Categoría de ejemplo
        categorias = ["Acción","Comedia","Drama","Documental","Terror","Animación","Aventura"]
        category = ask_choice("Categoría", "category", categorias)

        # 5) Sinopsis
        synopsis = ask_text("Sinopsis", "synopsis")

        # 6) Duración
        duration = ask_int("Duración (minutos)", "duration")

        # 7) Clasificación (age_rating)
        clasificaciones = ["G","PG","PG-13","R","C"]
        age_rating = ask_choice("Clasificación", "age_rating", clasificaciones)

        # 8) Idioma
        idiomas = ["Español","Inglés"]
        language = ask_choice("Idioma", "language", idiomas)

        # 9) Sala (room_type)
        salas = ["2D","3D"]
        room_type = ask_choice("Tipo de sala", "room_type", salas)

        # 10) Sala (hall)
        halls = ["regular","preferencial"]
        hall = ask_choice("Tipo de hall", "hall", halls)

        # 11) Precio
        ticket_price = float(ask_text("Precio base del ticket", "ticket_price"))

        # 12) Asientos disponibles
        general = int(ask_text("Asientos generales disponibles", "available_seats.general"))
        preferenciales = int(ask_text("Asientos preferenciales disponibles", "available_seats.preferencial"))

        # 13) Horarios (este lo dejaría igual que antes, o implementarlo con defaults similares)...

        return {
            "title": title,
            "director": director,
            "release_year": release_year,
            "category": category,
            "synopsis": synopsis,
            "duration": duration,
            "age_rating": age_rating,
            "language": language,
            "origin": ask_text("País de origen", "origin"),
            "room_type": room_type,
            "hall": hall,
            "ticket_price": ticket_price,
            "showtimes": current_data.get("showtimes", []) if for_update else [],
            "available_seats": {
                "general": general,
                "preferencial": preferenciales
            }
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
        """Muestra los horarios disponibles con disponibilidad real."""
        if not showtimes:
            self.console.print("[yellow]No hay horarios disponibles para esta película[/]")
            return

        # Cargo tickets y reservas para calcular ocupación
        tickets = self.db.load_data("tickets.json")
        reservations = self.db.load_data("reservations.json")

        table = Table(title="[bold]Horarios Disponibles[/]", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Fecha", style="magenta")
        table.add_column("Hora", style="white")
        table.add_column("Jornada", style="green")
        table.add_column("Disponibilidad", style="yellow")

        for st in showtimes:
            st_id = st["showtime_id"]
            dt_str = f"{st['date']} {st['start_time']}"

            # capacidad original por tipos
            capacidad = sum(st.get("available_seats", {}).values())

            # ocupados activos en tickets + reservas
            occ_tickets = sum(
                1 for t in tickets
                if t.get("showtime") == dt_str and t.get("status") == "activo"
            )
            occ_res = sum(
                1 for r in reservations
                if r.get("showtime_id") == st_id and r.get("status") == "activo"
            )
            ocupados = occ_tickets + occ_res

            disponibles = capacidad - ocupados

            # formateo: si no hubo ocupación muestro "X Boletas", si no "Y/X Boletas"
            if ocupados == 0:
                disp_text = f"{capacidad} Boletas"
            else:
                disp_text = f"{disponibles}/{capacidad} Boletas"

            table.add_row(
                str(st_id),
                st["date"],
                f"{st['start_time']}-{st['end_time']}",
                st["jornada"],
                disp_text
            )

        self.console.print(table)