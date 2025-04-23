def handle_availability(self):
    """Muestra la disponibilidad de asientos."""
    try:
        movies = self.movie_controller.list_movies()
        showtimes = self.showtime_controller.load_data("showtimes.json")
        self.movie_view.show_movies(movies, showtimes)
        movie_id = int(self.console.input("Ingrese ID de la película: "))
        movie = next((m for m in movies if m['movie_id'] == movie_id), None)
        if not movie:
            self.menu_view.show_message("Película no encontrada", is_error=True)
            return
        movie_showtimes = [st for st in showtimes if st['movie_id'] == movie_id]
        self.movie_view.show_showtimes(movie_showtimes)
        showtime_id = int(self.console.input("Ingrese ID del horario: "))
        showtime = next((st for st in movie_showtimes if st['showtime_id'] == showtime_id), None)
        if not showtime:
            self.menu_view.show_message("Horario no encontrado", is_error=True)
            return
        cinema = next((c for c in self.cinema_controller.list_cinemas()
                        if c['room_type'] == movie['room_type']), None)
        if cinema:
            self.availability_view.show_availability(
                showtime_id=showtime['showtime_id'],
                cinema_id=cinema['cinema_id'],
                cinema_name=cinema['name'],
                movie_title=movie['title'],
                showtime_str=f"{showtime['date']} {showtime['start_time']}"
            )
        self.menu_view.press_enter_to_continue()
    except ValueError:
        self.menu_view.show_message("ID debe ser un número", is_error=True)