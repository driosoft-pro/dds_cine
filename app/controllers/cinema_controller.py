from typing import Dict, List, Optional
from datetime import datetime
from models.cinema import CinemaHall, Seat
from models.ticket import Ticket, Reservation
from models.movie import Movie
from services.ticket_pricing import calculate_ticket_price

class CinemaController:
    def __init__(self):
        self.halls: Dict[str, CinemaHall] = {
            '2D-1': CinemaHall('2D-1', '2D'),
            '3D-1': CinemaHall('3D-1', '3D')
        }
        self.tickets: Dict[str, Ticket] = {}
        self.reservations: Dict[str, Reservation] = {}

    def get_hall_for_movie(self, movie: Movie, showtime: dict) -> Optional[CinemaHall]:
        """Obtiene la sala adecuada para una película y horario"""
        for hall in self.halls.values():
            if hall.hall_type == movie.room_type:
                # Verificar disponibilidad en el horario
                if self._check_schedule_availability(hall, movie, showtime):
                    return hall
        return None

    def _check_schedule_availability(self, hall: CinemaHall, movie: Movie, showtime: dict) -> bool:
        """Verifica disponibilidad en el horario"""
        # Aquí se podría implementar lógica más compleja de horarios
        return True

    def purchase_ticket(self, user_id: int, movie: Movie, showtime: dict, 
                        seat_numbers: List[str], ticket_type: str) -> Optional[Ticket]:
        """Procesa la compra de un ticket"""
        hall = self.get_hall_for_movie(movie, showtime)
        if not hall:
            return None

        # Verificar que los asientos estén disponibles
        for seat_num in seat_numbers:
            if seat_num not in hall.seats or not hall.seats[seat_num].is_available():
                return None

        # Crear el ticket
        ticket_id = f"TKT-{datetime.now().timestamp()}"
        price = calculate_ticket_price(
            ticket_type=ticket_type,
            seat_type=hall.seats[seat_numbers[0]].seat_type.value,
            showtime=showtime
        )

        ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            movie_id=movie.movie_id,
            showtime=showtime,
            room_type=hall.hall_type,
            seats=seat_numbers,
            ticket_type=ticket_type,
            price=price,
            purchase_date=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        # Asignar asientos
        if hall.assign_seat_for_ticket(ticket):
            self.tickets[ticket_id] = ticket
            return ticket
        return None

    def make_reservation(self, user_id: int, movie: Movie, showtime: dict, 
                        seat_numbers: List[str]) -> Optional[Reservation]:
        """Crea una reservación"""
        hall = self.get_hall_for_movie(movie, showtime)
        if not hall:
            return None

        # Verificar asientos
        for seat_num in seat_numbers:
            if seat_num not in hall.seats or not hall.seats[seat_num].is_available():
                return None

        # Crear reservación
        reservation_id = f"RSV-{datetime.now().timestamp()}"
        reservation = Reservation(
            reservation_id=reservation_id,
            user_id=user_id,
            movie_id=movie.movie_id,
            showtime=showtime,
            seats=seat_numbers,
            reservation_date=datetime.now().strftime("%Y-%m-%d"),
            expiry_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            status='pending'
        )

        if hall.assign_seat_for_reservation(reservation):
            self.reservations[reservation_id] = reservation
            return reservation
        return None

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancela una reservación"""
        if reservation_id not in self.reservations:
            return False

        reservation = self.reservations[reservation_id]
        hall = next((h for h in self.halls.values() if h.hall_type == reservation.room_type), None)
        if not hall:
            return False

        if hall.release_seats(reservation.seats):
            reservation.status = 'cancelled'
            return True
        return False

    def confirm_reservation(self, reservation_id: str) -> Optional[Ticket]:
        """Convierte una reservación en ticket"""
        if reservation_id not in self.reservations:
            return None

        reservation = self.reservations[reservation_id]
        hall = next((h for h in self.halls.values() if h.hall_type == reservation.room_type), None)
        if not hall:
            return None

        # Crear ticket a partir de la reservación
        ticket = self.purchase_ticket(
            user_id=reservation.user_id,
            movie=reservation.movie,
            showtime=reservation.showtime,
            seat_numbers=reservation.seats,
            ticket_type='general'  # o se podría especificar
        )

        if ticket:
            reservation.status = 'confirmed'
            return ticket
        return None