from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from datetime import datetime, timedelta
from typing import List, Optional

from models.movie import Movie, TwoDMovie, ThreeDMovie
from controllers.movie_controller import MovieController

def display_movie_management(console: Console, movie_controller: MovieController, is_admin: bool):
    """
    Muestra el menú de gestión de películas según el tipo de usuario.
    """
    while True:
        console.clear()
        console.print(Panel.fit("GESTIÓN DE PELÍCULAS", style="bold blue"))
        
        if is_admin:
            console.print("\n1. Agregar nueva película")
            console.print("2. Editar película existente")
            console.print("3. Cambiar estado de película")
            console.print("4. Ver todas las películas")
            console.print("5. Buscar películas")
            console.print("6. Volver al menú principal\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6"])
            
            if option == "1":
                handle_add_movie(console, movie_controller)
            elif option == "2":
                handle_edit_movie(console, movie_controller)
            elif option == "3":
                handle_change_movie_status(console, movie_controller)
            elif option == "4":
                display_all_movies(console, movie_controller, is_admin)
            elif option == "5":
                handle_search_movies(console, movie_controller, is_admin)
            elif option == "6":
                return
        else:
            console.print("\n1. Ver cartelera")
            console.print("2. Buscar películas")
            console.print("3. Volver al menú principal\n")
            
            option = Prompt.ask("Seleccione una opción", choices=["1", "2", "3"])
            
            if option == "1":
                display_all_movies(console, movie_controller, is_admin)
            elif option == "2":
                handle_search_movies(console, movie_controller, is_admin)
            elif option == "3":
                return

def handle_add_movie(console: Console, movie_controller: MovieController):
    """
    Maneja el proceso de agregar una nueva película con interfaz mejorada.
    """
    console.clear()
    console.print(Panel.fit("AGREGAR NUEVA PELÍCULA", style="bold green"))
    
    movie_data = {}
    
    # Tipo de película con opciones numeradas
    console.print("\n[bold]Tipo de película:[/bold]")
    console.print("1: 2D (Estándar)")
    console.print("2: 3D (Efectos especiales)")
    movie_type = Prompt.ask("Seleccione el tipo", choices=["1", "2"])
    movie_type = "2d" if movie_type == "1" else "3d"  # Cambiado a minúsculas para coincidir con el controlador
    
    # Título
    movie_data['title'] = Prompt.ask("\nTítulo de la película")

    # Año de lanzamiento con validación
    current_year = datetime.now().year
    while True:
        try:
            release_year = int(Prompt.ask(
                f"\nAño de lanzamiento (1900-{current_year})",
                default=str(current_year)
            ))
            if 1900 <= release_year <= current_year:
                movie_data['release_year'] = release_year
                break
            console.print(f"[red]Error: Ingrese un año entre 1900 y {current_year}[/red]")
        except ValueError:
            console.print("[red]Error: Ingrese un año válido[/red]")

    # Director
    movie_data['director'] = Prompt.ask("\nDirector")

    # Género con sugerencias
    common_genders = ["Acción", "Comedia", "Drama", "Romance", "Ciencia Ficción", 
                    "Terror", "Animación", "Aventura", "Documental"]
    console.print("\n[dim]Sugerencias: " + ", ".join(common_genders) + "[/dim]")
    movie_data['gender'] = Prompt.ask("Género")  # Cambiado a 'gender'

    # Sinopsis
    movie_data['synopsis'] = Prompt.ask("\nSinopsis (resumen de la trama)")

    # Duración en minutos con explicación
    while True:
        try:
            duration = int(Prompt.ask(
                "\nDuración [bold](en minutos)[/bold]. Ejemplo: 120 para 2 horas",
                default="120"
            ))
            if duration > 0:
                movie_data['duration'] = duration
                break
            console.print("[red]Error: La duración debe ser mayor a 0[/red]")
        except ValueError:
            console.print("[red]Error: Ingrese un número válido[/red]")

    # Clasificación con opciones numeradas y explicación
    console.print("\n[bold]Clasificación por edades:[/bold]")
    console.print("1: G - Para todos los públicos")
    console.print("2: PG - Sugerencia guía parental")
    console.print("3: PG-13 - Mayores de 13 años")
    console.print("4: R - Mayores de 17 años con acompañante")
    console.print("5: NC-17 - Solo adultos")
    rating_choice = Prompt.ask("Seleccione la clasificación", choices=["1", "2", "3", "4", "5"])
    rating_map = {"1": "G", "2": "PG", "3": "PG-13", "4": "R", "5": "NC-17"}
    movie_data['rating'] = rating_map[rating_choice]

    # Idioma y origen
    movie_data['language'] = Prompt.ask("\nIdioma original", default="Español")
    movie_data['origin'] = Prompt.ask("País de origen", default="Colombia")

    # Tipo de sala (hall) con validación según el tipo de película
    console.print("\n[bold]Tipo de sala:[/bold]")
    if movie_type == "2d":
        console.print("1: Regular (única opción para películas 2D)")
        hall_choice = "1"  # Forzamos la selección de "Regular" para películas 2D
    else:
        console.print("1: Regular")
        console.print("2: Premium")
        hall_choice = Prompt.ask("Seleccione el tipo de sala", choices=["1", "2"])
    
    movie_data['hall'] = "Regular" if hall_choice == "1" else "Premium"

    # Horarios con opciones mejoradas
    movie_data['showtimes'] = []
    console.print("\n[bold underline]Horarios de presentación:[/bold underline]")
    
    while True:
        showtime = {}
        
        # Fecha con validación
        default_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        while True:
            date = Prompt.ask("\nFecha (YYYY-MM-DD)", default=default_date)
            try:
                datetime.strptime(date, "%Y-%m-%d")
                showtime['date'] = date
                break
            except ValueError:
                console.print("[red]Error: Formato inválido. Use YYYY-MM-DD[/red]")
        
        # Hora con validación
        while True:
            time = Prompt.ask("Hora (HH:MM)", default="19:00")
            try:
                datetime.strptime(time, "%H:%M")
                showtime['time'] = time
                break
            except ValueError:
                console.print("[red]Error: Formato inválido. Use HH:MM[/red]")
        
        # Sesión con opciones numeradas
        console.print("\n[bold]Sesión:[/bold]")
        console.print("1: Mañana")
        console.print("2: Tarde")
        console.print("3: Noche")
        session_choice = Prompt.ask("Seleccione la sesión", choices=["1", "2", "3"])
        session_map = {"1": "mañana", "2": "tarde", "3": "noche"}
        showtime['session'] = session_map[session_choice]
        
        movie_data['showtimes'].append(showtime)
        
        if not Confirm.ask("\n¿Desea agregar otro horario?", default=False):
            break
    
    # Crear la película
    movie = movie_controller.create_movie(movie_data, movie_type)
    
    if movie:
        console.print(f"\n[bold green]¡Película '{movie.title}' agregada exitosamente![/bold green]")
    else:
        console.print("\n[bold red]Error: No se pudo agregar la película[/bold red]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def display_all_movies(console: Console, movie_controller: MovieController, is_admin: bool):
    """
    Muestra todas las películas en formato de tabla, incluyendo el tipo de sala (Premium o Regular)
    y los horarios de las películas con fecha, hora y sesión.
    """
    console.clear()
    movies = movie_controller.get_all_movies()
    
    if not movies:
        console.print("[bold yellow]No hay películas registradas[/bold yellow]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    table = Table(title="🎬 CARTELERA DE PELÍCULAS", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Título", min_width=20)
    table.add_column("Género", min_width=12)
    table.add_column("Duración", justify="right")
    table.add_column("Clasificación", justify="center")
    table.add_column("Sala", justify="center")
    table.add_column("Tipo Sala", justify="center")  # Nueva columna para el tipo de sala
    table.add_column("Horario", justify="center")  # Nueva columna para los horarios
    table.add_column("Estado", justify="center")
    
    for movie in movies:
        status = "[green]✔[/green]" if movie.status == 'active' else "[red]✖[/red]"
        # Iterar sobre los horarios de la película
        for showtime in movie.showtimes:
            formatted_showtime = f"{showtime['date']} {showtime['time']} ({showtime['session']})"  # Formatear horario
            table.add_row(
                str(movie.movie_id),
                movie.title,
                movie.gender,
                f"{movie.duration} min",
                movie.rating,
                movie.room_type,  
                movie.hall,  
                formatted_showtime,  
                status
            )
    
    console.print(table)
    
    if is_admin:
        console.print("\n[dim]Nota: ✔ = Activa, ✖ = Inactiva[/dim]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def handle_edit_movie(console: Console, movie_controller: MovieController):
    """
    Maneja el proceso de edición de una película existente.
    """
    console.clear()
    console.print(Panel.fit("EDITAR PELÍCULA", style="bold green"))
    
    # Mostrar lista de películas para selección
    movies = movie_controller.get_all_movies()
    if not movies:
        console.print("[bold yellow]No hay películas registradas para editar[/bold yellow]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    display_movies_compact(console, movies)
    
    # Seleccionar película a editar
    while True:
        try:
            movie_id = int(Prompt.ask("Ingrese el ID de la película a editar"))
            selected_movie = movie_controller.get_movie(movie_id)
            if selected_movie:
                break
            console.print("[bold red]Error: ID de película no válido[/bold red]")
        except ValueError:
            console.print("[bold red]Error: Ingrese un número válido[/bold red]")
    
    console.print(f"\nEditando: [bold]{selected_movie.title}[/bold]")
    
    # Campos editables con valores actuales como defaults
    update_data = {}
    
    # Título
    new_title = Prompt.ask("Título", default=selected_movie.title)
    if new_title != selected_movie.title:
        update_data['title'] = new_title
    
    # Género (cambiado a 'gender')
    new_gender = Prompt.ask("Género", default=selected_movie.gender)
    if new_gender != selected_movie.gender:
        update_data['gender'] = new_gender
    
    # Sinopsis
    new_synopsis = Prompt.ask("Sinopsis", default=selected_movie.synopsis)
    if new_synopsis != selected_movie.synopsis:
        update_data['synopsis'] = new_synopsis
    
    # Rating
    while True:
        new_rating = Prompt.ask("Clasificación (G, PG, PG-13, R, NC-17)", 
                                choices=["G", "PG", "PG-13", "R", "NC-17"],
                                default=selected_movie.rating)
        if Movie.validate_rating(new_rating):
            if new_rating != selected_movie.rating:
                update_data['rating'] = new_rating
            break
    
    # Tipo de sala (hall)
    console.print("\n[bold]Tipo de sala actual:[/bold] " + selected_movie.hall)
    if Confirm.ask("¿Desea cambiar el tipo de sala?"):
        console.print("\n1: Regular")
        console.print("2: Premium")
        hall_choice = Prompt.ask("Seleccione el tipo de sala", choices=["1", "2"])
        update_data['hall'] = "Regular" if hall_choice == "1" else "Premium"
    
    # Horarios
    if Confirm.ask("\n¿Desea modificar los horarios de presentación?"):
        new_showtimes = []
        console.print("\n[bold]Horarios actuales:[/bold]")
        for i, showtime in enumerate(selected_movie.showtimes, 1):
            console.print(f"{i}. {showtime['date']} {showtime['time']} ({showtime['session']})")
        
        console.print("\n[bold]Nuevos horarios:[/bold]")
        while True:
            showtime = {}
            
            # Fecha
            while True:
                date = Prompt.ask("Fecha (YYYY-MM-DD)")
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    showtime['date'] = date
                    break
                except ValueError:
                    console.print("[bold red]Error: Formato de fecha inválido (YYYY-MM-DD)[/bold red]")
            
            # Hora
            while True:
                time = Prompt.ask("Hora (HH:MM)", default="19:00")
                try:
                    datetime.strptime(time, "%H:%M")
                    showtime['time'] = time
                    break
                except ValueError:
                    console.print("[bold red]Error: Formato de hora inválido (HH:MM)[/bold red]")
            
            # Sesión
            showtime['session'] = Prompt.ask("Sesión (mañana, tarde, noche)", 
                                            choices=["mañana", "tarde", "noche"])
            
            new_showtimes.append(showtime)
            
            if not Confirm.ask("¿Desea agregar otro horario?"):
                break
        
        update_data['showtimes'] = new_showtimes
    
    # Aplicar cambios si hay actualizaciones
    if update_data:
        updated_movie = movie_controller.update_movie(selected_movie.movie_id, update_data)
        if updated_movie:
            console.print(f"\n[bold green]¡Película '{updated_movie.title}' actualizada exitosamente![/bold green]")
        else:
            console.print("\n[bold red]Error: No se pudo actualizar la película[/bold red]")
    else:
        console.print("\n[bold yellow]No se realizaron cambios[/bold yellow]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def handle_change_movie_status(console: Console, movie_controller: MovieController):
    """
    Maneja el cambio de estado (activo/inactivo) de una película.
    """
    console.clear()
    console.print(Panel.fit("CAMBIAR ESTADO DE PELÍCULA", style="bold green"))
    
    # Mostrar solo películas activas
    active_movies = [m for m in movie_controller.get_all_movies() if m.status == 'active']
    inactive_movies = [m for m in movie_controller.get_all_movies() if m.status == 'inactive']
    
    if not active_movies and not inactive_movies:
        console.print("[bold yellow]No hay películas registradas[/bold yellow]")
        Prompt.ask("\nPresione Enter para continuar...")
        return
    
    # Mostrar películas activas
    if active_movies:
        console.print("\n[bold]Películas activas:[/bold]")
        display_movies_compact(console, active_movies)
    
    # Mostrar películas inactivas
    if inactive_movies:
        console.print("\n[bold]Películas inactivas:[/bold]")
        display_movies_compact(console, inactive_movies)
    
    # Seleccionar película
    while True:
        try:
            movie_id = int(Prompt.ask("\nIngrese el ID de la película a cambiar estado"))
            selected_movie = movie_controller.get_movie(movie_id)
            if selected_movie:
                break
            console.print("[bold red]Error: ID de película no válido[/bold red]")
        except ValueError:
            console.print("[bold red]Error: Ingrese un número válido[/bold red]")
    
    # Determinar acción (activar/desactivar)
    new_status = 'inactive' if selected_movie.status == 'active' else 'active'
    action = "desactivar" if new_status == 'inactive' else "activar"
    
    # Confirmar acción
    if Confirm.ask(f"\n¿Está seguro que desea {action} '{selected_movie.title}'?"):
        success = movie_controller.change_movie_status(selected_movie.movie_id, new_status)
        if success:
            console.print(f"\n[bold green]¡Película {action}da exitosamente![/bold green]")
        else:
            console.print("\n[bold red]Error: No se pudo cambiar el estado[/bold red]")
    else:
        console.print("\n[bold yellow]Operación cancelada[/bold yellow]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def handle_search_movies(console: Console, movie_controller: MovieController, is_admin: bool):
    """
    Maneja la búsqueda de películas por diferentes criterios.
    """
    console.clear()
    console.print(Panel.fit("BUSCAR PELÍCULAS", style="bold green"))
    
    console.print("\n1. Por título")
    console.print("2. Por género")
    console.print("3. Por clasificación")
    console.print("4. Por tipo de sala (2D/3D)")
    console.print("5. Volver\n")
    
    option = Prompt.ask("Seleccione un criterio de búsqueda", choices=["1", "2", "3", "4", "5"])
    
    if option == "5":
        return
    
    search_term = None
    movies = []
    
    if option == "1":
        search_term = Prompt.ask("Ingrese título o parte del título")
        movies = [m for m in movie_controller.get_all_movies() 
                    if search_term.lower() in m.title.lower()]
    elif option == "2":
        search_term = Prompt.ask("Ingrese género")
        movies = [m for m in movie_controller.get_all_movies() 
                    if search_term.lower() in m.gender.lower()]
    elif option == "3":
        search_term = Prompt.ask("Ingrese clasificación (G, PG, PG-13, R, NC-17)", 
                                choices=["G", "PG", "PG-13", "R", "NC-17"])
        movies = [m for m in movie_controller.get_all_movies() 
                    if m.rating == search_term]
    elif option == "4":
        search_term = Prompt.ask("Ingrese tipo de sala (2D/3D)", choices=["2D", "3D"])
        movies = [m for m in movie_controller.get_all_movies() 
                    if m.room_type == search_term]
    
    console.clear()
    if search_term:
        console.print(Panel.fit(f"RESULTADOS DE BÚSQUEDA: {search_term.upper()}", 
                                style="bold blue"))
    
    if movies:
        if is_admin:
            display_all_movies(console, movie_controller, is_admin)
        else:
            display_movies_for_customers(console, movies)
    else:
        console.print("\n[bold yellow]No se encontraron películas con ese criterio[/bold yellow]")
    
    Prompt.ask("\nPresione Enter para continuar...")

def display_movies_compact(console: Console, movies: List[Movie]):
    """
    Muestra una lista compacta de películas para selección.
    """
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Título", min_width=20)
    table.add_column("Tipo", justify="center")
    table.add_column("Estado", justify="center")
    
    for movie in movies:
        status = "[green]✔[/green]" if movie.status == 'active' else "[red]✖[/red]"
        table.add_row(
            str(movie.movie_id),
            movie.title,
            movie.room_type,
            status
        )
    
    console.print(table)

def display_movies_for_customers(console: Console, movies: List[Movie]):
    """
    Muestra películas con formato especial para clientes.
    """
    table = Table(title="🎬 CARTELERA", show_header=True, header_style="bold magenta")
    table.add_column("Título", min_width=20)
    table.add_column("Género", min_width=12)
    table.add_column("Duración", justify="right")
    table.add_column("Clasificación", justify="center")
    table.add_column("Horarios", min_width=30)
    
    for movie in sorted(movies, key=lambda x: x.title):
        # Formatear horarios para mostrar
        showtimes_str = "\n".join(
            f"{st['date']} {st['time']} ({st['session']})" 
            for st in movie.showtimes
        )
        
        table.add_row(
            movie.title,
            movie.gender,
            f"{movie.duration} min",
            movie.rating,
            showtimes_str
        )
    
    console.print(table)
    console.print("\n[dim]Seleccione una película para ver más detalles o comprar entradas[/dim]")