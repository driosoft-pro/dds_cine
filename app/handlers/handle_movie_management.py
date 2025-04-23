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
            if movie_data is not None:
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
            
            current = self.movie_controller.get_movie_by_id(movie_id)
            if not current:
                self.menu_view.show_message("Película no encontrada", is_error=True)
                continue

            # Pedir datos en modo update, mostrando defaults
            movie_data = self.movie_view.get_movie_data(
                for_update=True,
                current_data=current
            )
            if movie_data is None:
                # El usuario decidió cancelar
                continue

            updated = self.movie_controller.update_movie(movie_id, **movie_data)
            if updated:
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