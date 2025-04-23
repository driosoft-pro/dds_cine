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