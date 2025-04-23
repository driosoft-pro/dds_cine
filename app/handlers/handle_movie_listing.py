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