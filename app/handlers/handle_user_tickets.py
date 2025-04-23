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