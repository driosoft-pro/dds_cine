def handle_ticket_purchase(self):
    """Maneja el proceso de compra de tickets con múltiples asientos."""
    choice = self.ticket_view.show_ticket_menu()
    if choice == "1":  # Comprar ticket
        try:
            # 1. Películas y showtimes
            movies = self.movie_controller.list_movies()
            showtimes = self.showtime_controller.load_data("showtimes.json")
            # 2. Datos de compra
            purchase_data = self.ticket_view.get_ticket_purchase_data(movies, showtimes)
            movie = self.movie_controller.get_movie_by_id(purchase_data['movie_id'])
            # 3. Validar showtime
            selected_showtime = next((
                st for st in showtimes
                if st['movie_id'] == purchase_data['movie_id']
                and st['showtime_id'] == purchase_data['showtime_id']
            ), None)
            if not selected_showtime:
                self.menu_view.show_message("Horario no encontrado", is_error=True)
                return
            # 4. Validar sala
            cinema = self.cinema_controller.get_cinema_by_id(selected_showtime['cinema_id'])
            if not cinema:
                self.menu_view.show_message("Sala no encontrada", is_error=True)
                return
            # 5. Asientos disponibles
            available_seats = self.cinema_controller.get_available_seats_by_type(
                selected_showtime['cinema_id'],
                purchase_data['seat_type']
            )
            if not available_seats:
                self.menu_view.show_message("No hay asientos disponibles", is_error=True)
                return
            # 6. Selección de N asientos
            qty = purchase_data['quantity']
            if qty > 1:
                seats = self.ticket_view.select_multiple_seats(available_seats, qty)
            else:
                seats = [self.ticket_view.select_seat(available_seats)]
            # 7. Reserva TEMPORAL
            for seat in seats:
                if not self.cinema_controller.temp_reserve_seat(
                    selected_showtime['cinema_id'],
                    purchase_data['seat_type'],
                    seat
                ):
                    self.menu_view.show_message("Error al reservar el asiento", is_error=True)
                    return
            try:
                # 8. Calcular precio
                user = self.user_controller.get_user_by_id(self.current_user['user_id'])
                birth_date = datetime.strptime(user['birth_date'], "%Y-%m-%d").date()
                dt = safe_parse_datetime(
                    selected_showtime['date'],
                    selected_showtime['start_time']
                )
                price_per_ticket = TicketService.calculate_ticket_price(
                    room_type=movie['room_type'],
                    seat_type=purchase_data['seat_type'],
                    birth_date=birth_date,
                    showtime=dt
                )
                total_price = price_per_ticket * qty
                # 9. Mostrar resumen
                ticket_summary = {
                    'movie_title': movie['title'],
                    'showtime': dt.strftime("%Y-%m-%d %H:%M"),
                    'seat_number': ", ".join(seats),
                    'ticket_type': purchase_data['seat_type'],
                    'price': total_price
                }
                self.ticket_view.show_ticket_summary(ticket_summary)
                # 10. Confirmación
                if not self.menu_view.confirm_action("Confirmar compra?"):
                    raise Exception("Compra cancelada por el usuario")
                # 11. Procesar pago
                payment_method = self.ticket_view.get_payment_method()
                if payment_method == "1":  # Efectivo
                    cash = self.ticket_view.get_cash_amount(total_price)
                    self.ticket_view.show_change(total_price, cash)
                # 12. Crear tickets y pagos
                created_tickets = []
                for seat in seats:
                    ticket_data = {
                        'user_id': self.current_user['user_id'],
                        'movie_id': purchase_data['movie_id'],
                        'showtime': dt,
                        'seat_number': seat,
                        'ticket_type': purchase_data['seat_type'],
                        'price': price_per_ticket
                    }
                    new_ticket = self.ticket_controller.create_ticket(**ticket_data)
                    created_tickets.append(new_ticket)
                    # Un pago POR CADA ticket
                    pay = self.payment_controller.create_payment(
                        user_id=self.current_user['user_id'],
                        amount=price_per_ticket,
                        payment_method=payment_method,
                        ticket_id=new_ticket['ticket_id']
                    )
                    self.payment_view.show_payment_summary(pay)
                # 13. Confirmar asiento definitivo
                for seat in seats:
                    self.cinema_controller.confirm_reservation(
                        selected_showtime['cinema_id'],
                        purchase_data['seat_type'],
                        seat
                    )
                self.menu_view.show_message("✅ Compra realizada con éxito!")
            except Exception as e:
                # Liberar todos los asientos temporales
                for seat in seats:
                    self.cinema_controller.release_seat(
                        selected_showtime['cinema_id'],
                        purchase_data['seat_type'],
                        seat
                    )
                self.menu_view.show_message(f"Error al procesar la compra: {e}", is_error=True)
        except Exception as e:
            self.menu_view.show_message(f"Error inesperado: {e}", is_error=True)
        finally:
            self.menu_view.press_enter_to_continue()
    elif choice == "2":  # Ver mis tickets
        tickets = self.ticket_controller.get_tickets_by_user(self.current_user['user_id'])
        enriched = []
        for t in tickets:
            movie = self.movie_controller.get_movie_by_id(t['movie_id'])
            enriched.append({**t, 'movie_title': movie['title'] if movie else "N/D"})
        self.ticket_view.show_tickets(enriched)
        self.menu_view.press_enter_to_continue()
    elif choice == "3":  # Cancelar ticket
        tickets = self.ticket_controller.get_tickets_by_user(self.current_user['user_id'])
        if not tickets:
            self.menu_view.show_message("No tienes tickets para cancelar", is_error=True)
        else:
            ticket_id = int(self.console.input("Ingrese ID del ticket a cancelar: "))
            ok = self.ticket_controller.cancel_ticket(ticket_id)
            msg = "Ticket cancelado con éxito!" if ok else "Error al cancelar el ticket"
            self.menu_view.show_message(msg, is_error=not ok)
        self.menu_view.press_enter_to_continue()
    elif choice == "0":  # Volver
        return