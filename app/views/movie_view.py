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
            opcion = Prompt.ask("Seleccione una ID").strip()
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
        self.console.print("3. Por fecha")
        self.console.print("[dim]Presione Enter sin escribir nada para volver.[/]\n")

        while True:
            choice = Prompt.ask("Seleccione criterio (1-3)").strip()
            if choice == "":
                self.console.print("[yellow]Volviendo al menú...[/]")
                return None 
            elif choice == "1":
                titulo = Prompt.ask("Ingrese título o parte del título").strip()
                return {'title': titulo}
            elif choice == "2":
                categoria = Prompt.ask("Ingrese categoría").strip()
                return {'category': categoria}
            elif choice == "3":
                fecha = Prompt.ask("Ingrese fecha (YYYY-MM-DD)").strip()
                return {'date': fecha}
            else:
                self.console.print("[red]Opción inválida. Intente nuevamente.[/]")
        
    def get_movie_data(self):
        """Obtiene datos para crear/actualizar una película."""

        title = Prompt.ask("Título de la película")
        if not title.strip():
            self.console.print("[yellow]Ingresa un título válido.[/]")
            return

        director = Prompt.ask("Director")
        if not director.strip():
            self.console.print("[yellow]Ingresa un director válido.[/]")
            return

        release_year_input = Prompt.ask("Año de lanzamiento")
        if not release_year_input.strip().isdigit():
            print("[yellow]Ingresa un año válido.[/]")
            return

        release_year = int(release_year_input)

        category_list = ["Acción", "Comedia", "Drama", "Documental", "Terror", "Animación"]

        self.console.print("\n[bold]Categorías disponibles:[/]")
        for i, cat in enumerate(category_list, start=1):
            self.console.print(f"{i}. {cat}")

        opcion = Prompt.ask("Ingresa el número de la categoría")

        if not opcion.isdigit() or not (1 <= int(opcion) <= len(category_list)):
            self.console.print("[yellow]Ingresa un número válido correspondiente a una categoría.[/]")
            return

        category = category_list[int(opcion) - 1]

        synopsis = Prompt.ask("Sinopsis")
        if not synopsis.strip():
            self.console.print("[yellow]Ingresa una sinopsis válida.[/]")
            return

        duration_input = Prompt.ask("Duración (minutos)")
        if not duration_input.strip().isdigit():
            print("[yellow]Ingresa una duración válida en minutos.[/]")
            return

        duration = int(duration_input)

        clasificaciones = [
            ("G", "Apta para todo público"),
            ("PG", "Supervisión de los padres sugerida"),
            ("PG-13", "No recomendada para menores de 13 años"),
            ("R", "Restringida a menores de 17 años sin acompañante adulto"),
            ("C", "Solo para adultos")
        ]

        self.console.print("\n[bold]Clasificaciones disponibles:[/]")
        for i, (clave, descripcion) in enumerate(clasificaciones, start=1):
            self.console.print(f"{i}. [cyan]{clave}[/] - {descripcion}")

        while True:
            opcion = Prompt.ask("Ingresa el número de la clasificación")
            if opcion.isdigit() and 1 <= int(opcion) <= len(clasificaciones):
                age_rating = clasificaciones[int(opcion) - 1][0]
                break
            self.console.print("[yellow]Número no válido. Elige una opción del 1 al 5.[/]")

        self.console.print(f"[green]Has seleccionado: {age_rating}[/]")

        idiomas = [("Esp", "Español"), ("Ing", "Inglés")]

        self.console.print("\n[bold]Idiomas disponibles:[/]")
        for i, (clave, nombre) in enumerate(idiomas, start=1):
            self.console.print(f"{i}. [cyan]{clave}[/] - {nombre}")

        while True:
            idioma_opcion = Prompt.ask("Ingresa el número del idioma")
            if idioma_opcion.isdigit() and 1 <= int(idioma_opcion) <= len(idiomas):
                language = idiomas[int(idioma_opcion) - 1][0]
                break
            self.console.print("[yellow]Número no válido. Elige una opción del 1 al 2.[/]")

        while True:
            origin = Prompt.ask("País de origen")
            if origin and origin.strip():
                break
            self.console.print("[yellow]Ingresa un país de origen válido.[/]")

        tipos_sala = [("2D", "Proyección en dos dimensiones"), ("3D", "Proyección en tres dimensiones")]

        self.console.print("\n[bold]Tipos de sala disponibles:[/]")
        for i, (clave, descripcion) in enumerate(tipos_sala, start=1):
            self.console.print(f"{i}. [cyan]{clave}[/] - {descripcion}")

        while True:
            sala_opcion = Prompt.ask("Ingresa el número del tipo de sala")
            if sala_opcion.isdigit() and 1 <= int(sala_opcion) <= len(tipos_sala):
                room_type = tipos_sala[int(sala_opcion) - 1][0]
                break
            self.console.print("[yellow]Número no válido. Elige una opción del 1 al 2.[/]")

        tipos_hall = [("regular", "Sala regular"), ("preferencial", "Sala preferencial (mayor comodidad)")]

        self.console.print("\n[bold]Tipos de sala disponibles para seleccionar hall:[/]")
        for i, (clave, descripcion) in enumerate(tipos_hall, start=1):
            self.console.print(f"{i}. [cyan]{clave.capitalize()}[/] - {descripcion}")

        while True:
            hall_opcion = Prompt.ask("Ingresa el número del tipo de sala (hall)")
            if hall_opcion.isdigit() and 1 <= int(hall_opcion) <= len(tipos_hall):
                hall = tipos_hall[int(hall_opcion) - 1][0]
                break
            self.console.print("[yellow]Número no válido. Elige una opción del 1 al 2.[/]")

        try:
            ticket_price = float(Prompt.ask("Precio base del ticket"))
        except ValueError:
            self.console.print("[yellow]Ingresa un precio válido.[/]")
            return

        while True:
            general_input = Prompt.ask("Cantidad de asientos generales disponibles")
            if general_input.isdigit():
                general_seats = int(general_input)
                break
            self.console.print("[yellow]Ingresa un número válido para asientos generales.[/]")

        while True:
            pref_input = Prompt.ask("Cantidad de asientos preferenciales disponibles")
            if pref_input.isdigit():
                pref_seats = int(pref_input)
                break
            self.console.print("[yellow]Ingresa un número válido para asientos preferenciales.[/]")

        showtimes = []
        self.console.print("\n[bold]Agregar horarios (máximo 3, deja vacío para terminar):[/]")
        for i in range(3):
            date = Prompt.ask(f"Fecha del horario #{i+1} (YYYY-MM-DD, vacío para salir)", default="")
            if not date.strip():
                break
            start_time = Prompt.ask("Hora de inicio (HH:MM)")
            end_time = Prompt.ask("Hora de fin (HH:MM)")
            jornada = Prompt.ask("Jornada (mañana/tarde/noche)", choices=["mañana", "tarde", "noche"])

            showtimes.append({
                "showtime_id": i + 1,
                "movie_id": 0,  # se asignará luego
                "cinema_id": 0,  # opcional o editable luego
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "jornada": jornada,
                "available_seats": {
                    "general": general_seats,
                    "preferencial": pref_seats
                }
            })

        data = {
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