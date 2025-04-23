def handle_reservation(self):
    """Maneja el proceso completo de reservación, incluyendo selección de varios asientos."""
    choice = self.reservation_view.show_reservation_menu()
    
    if choice == "1":  # Hacer reservación
        try:
            # 1. Listar películas y horarios
            movies = self.movie_controller.list_movies()
            showtimes = self.showtime_controller.load_data("showtimes.json")
            self.movie_view.show_movies(movies, showtimes)
            
            # 2. Obtener datos de reservación
            reservation_data = self.reservation_view.get_reservation_data(movies, showtimes)
            movie = self.movie_controller.get_movie_by_id(reservation_data['movie_id'])
            
            # 3. Validar horario y sala
            selected_showtime = next(
                (st for st in showtimes
                    if st['movie_id'] == reservation_data['movie_id']
                    and st['showtime_id'] == reservation_data['showtime_id']),
                None
            )
            if not selected_showtime:
                self.menu_view.show_message("Horario no encontrado", is_error=True)
                return
            cinema_id = selected_showtime['cinema_id']
            cinema = self.cinema_controller.get_cinema_by_id(cinema_id)
            if not cinema:
                self.menu_view.show_message("Sala no encontrada", is_error=True)
                return
            
            # 4. Obtener y reservar temporalmente N asientos
            available_seats = self.showtime_controller.get_available_seats(
                selected_showtime['showtime_id'],
                reservation_data['seat_type']
            )
            qty = reservation_data['quantity']
            if qty > 1:
                seats = self.reservation_view.select_multiple_seats(available_seats, qty)
            else:
                seats = [self.reservation_view.select_seat(available_seats)]
            
            for seat in seats:
                if not self.cinema_controller.temp_reserve_seat(
                    cinema_id, reservation_data['seat_type'], seat
                ):
                    self.menu_view.show_message("Error al reservar el asiento", is_error=True)
                    return
            
            try:
                # 5. Calcular precio y generar resumen
                user = self.user_controller.get_user_by_id(self.current_user['user_id'])
                birth_date = datetime.strptime(user['birth_date'], "%Y-%m-%d").date()
                dt = safe_parse_datetime(
                    selected_showtime['date'],
                    selected_showtime['start_time']
                )
                price_per_ticket = TicketService.calculate_ticket_price(
                    room_type=movie['room_type'],
                    seat_type=reservation_data['seat_type'],
                    birth_date=birth_date,
                    showtime=dt
                )
                total_price = price_per_ticket * qty
                
                reservation_summary = {
                    'movie_title': movie['title'],
                    'showtime': dt.strftime("%Y-%m-%d %H:%M"),
                    'seat_number': ", ".join(seats),
                    'ticket_type': reservation_data['seat_type'],
                    'price': total_price,
                    'expiration': (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
                }
                self.reservation_view.show_reservation_summary(reservation_summary)
                
                # 6. Confirmar reserva
                if not self.menu_view.confirm_action("Confirmar reserva?"):
                    raise Exception("Reserva cancelada por el usuario")
                
                # 7. Crear reservas permanentes y confirmar asientos
                created = []
                for seat in seats:
                    res = self.reservation_controller.create_reservation(
                        user_id=self.current_user['user_id'],
                        movie_id=reservation_data['movie_id'],
                        showtime=dt.strftime("%Y-%m-%d %H:%M"),
                        seat_number=seat,
                        ticket_type=reservation_data['seat_type'],
                        price=price_per_ticket,
                        showtime_id=selected_showtime['showtime_id'],
                        expiration_date=(datetime.now() + timedelta(hours=24)).isoformat()
                    )
                    created.append(res)
                    self.cinema_controller.confirm_reservation(
                        cinema_id, reservation_data['seat_type'], seat
                    )
                
                self.menu_view.show_message("✅ Reserva realizada con éxito! Válida por 24 horas.")
            
            except Exception as e:
                # Liberar todos los asientos temporales si hay error
                for seat in seats:
                    self.cinema_controller.release_seat(
                        cinema_id, reservation_data['ticket_type'], seat
                    )
                self.menu_view.show_message(f"Error en la reserva: {e}", is_error=True)
                return
        
        except Exception as e:
            self.menu_view.show_message(f"Error inesperado: {e}", is_error=True)
        
        self.menu_view.press_enter_to_continue()
    
    elif choice == "2":  # Ver mis reservas
        reservations = self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
        enriched_reservations = []
        for r in reservations:
            movie = self.movie_controller.get_movie_by_id(r['movie_id'])
            enriched_reservations.append({
                **r,
                'movie_title': movie['title'] if movie else "Película no disponible",
                'showtime': r.get('showtime', 'Horario no disponible')
            })
        self.reservation_view.show_reservations(enriched_reservations)
        self.menu_view.press_enter_to_continue()
    
    elif choice == "3":  # Cancelar reserva
        reservations = self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
        if not reservations:
            self.menu_view.show_message("No tienes reservas activas para cancelar", is_error=True)
            self.menu_view.press_enter_to_continue()
            return
        
        reservation_id = self.reservation_view.select_reservation_to_cancel([
            {**r, 'movie_title': self.movie_controller.get_movie_by_id(r['movie_id'])['title']} 
            for r in reservations
        ])
        
        if reservation_id and self.reservation_controller.cancel_reservation(reservation_id):
            self.menu_view.show_message("✅ Reserva cancelada con éxito!")
        else:
            self.menu_view.show_message("Error al cancelar la reserva", is_error=True)
        self.menu_view.press_enter_to_continue()
    
    elif choice == "4":  # Convertir reserva a ticket
        active_reservations = [
            r for r in self.reservation_controller.get_reservations_by_user(self.current_user['user_id'])
            if r['status'] == 'activo'
        ]
        
        if not active_reservations:
            self.menu_view.show_message("No tienes reservas activas para convertir", is_error=True)
            self.menu_view.press_enter_to_continue()
            return
        
        reservation_id = self.reservation_view.select_reservation_to_convert([
            {**r, 'movie_title': self.movie_controller.get_movie_by_id(r['movie_id'])['title']} 
            for r in active_reservations
        ])
        
        if reservation_id:
            try:
                ticket = self.reservation_controller.convert_reservation_to_ticket(reservation_id)
                if ticket:
                    self.menu_view.show_message("✅ Reserva convertida a ticket con éxito!")
                else:
                    self.menu_view.show_message("Error al convertir la reserva", is_error=True)
            except Exception as e:
                self.menu_view.show_message(f"Error: {str(e)}", is_error=True)
        
        self.menu_view.press_enter_to_continue() 