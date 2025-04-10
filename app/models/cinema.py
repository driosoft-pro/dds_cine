from typing import Dict, List, Literal, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from .movie import Movie
from .ticket import Ticket, Reservation

class SeatType(Enum):
    STANDARD = "standard"
    PREFERENTIAL = "preferential"

class SeatStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"

@dataclass
class Seat:
    number: str
    seat_type: SeatType
    status: SeatStatus = SeatStatus.AVAILABLE
    reservation_id: Optional[str] = None
    ticket_id: Optional[str] = None

    def is_available(self) -> bool:
        return self.status == SeatStatus.AVAILABLE

    def occupy(self, ticket_id: str) -> bool:
        if self.is_available():
            self.status = SeatStatus.OCCUPIED
            self.ticket_id = ticket_id
            return True
        return False

    def reserve(self, reservation_id: str) -> bool:
        if self.is_available():
            self.status = SeatStatus.RESERVED
            self.reservation_id = reservation_id
            return True
        return False

    def release(self) -> bool:
        if not self.is_available():
            self.status = SeatStatus.AVAILABLE
            self.reservation_id = None
            self.ticket_id = None
            return True
        return False

class CinemaHall:
    def __init__(self, hall_id: str, hall_type: Literal['2D', '3D'], capacity: int = 100):
        self.hall_id = hall_id
        self.hall_type = hall_type
        self.seats: Dict[str, Seat] = self._initialize_seats(capacity)
        self.movie_schedule: Dict[str, List[Movie]] = {}  # {date: [movies]}

    def _initialize_seats(self, capacity: int) -> Dict[str, Seat]:
        seats = {}
        # Sala 2D solo tiene asientos estándar
        if self.hall_type == '2D':
            for i in range(1, capacity + 1):
                seat_num = f"S{i:02d}"
                seats[seat_num] = Seat(seat_num, SeatType.STANDARD)
        # Sala 3D tiene 80 estándar y 20 preferenciales
        else:
            for i in range(1, 81):
                seat_num = f"S{i:02d}"
                seats[seat_num] = Seat(seat_num, SeatType.STANDARD)
            for i in range(81, 101):
                seat_num = f"P{i-80:02d}"
                seats[seat_num] = Seat(seat_num, SeatType.PREFERENTIAL)
        return seats

    def get_available_seats(self, showtime: dict) -> List[Seat]:
        """Obtiene asientos disponibles para una función específica"""
        return [seat for seat in self.seats.values() if seat.is_available()]

    def assign_seat_for_ticket(self, ticket: Ticket) -> bool:
        """Asigna asientos para un ticket de compra"""
        for seat_num in ticket.seats:
            if seat_num not in self.seats or not self.seats[seat_num].is_available():
                return False
            self.seats[seat_num].occupy(ticket.ticket_id)
        return True

    def assign_seat_for_reservation(self, reservation: Reservation) -> bool:
        """Asigna asientos para una reservación"""
        for seat_num in reservation.seats:
            if seat_num not in self.seats or not self.seats[seat_num].is_available():
                return False
            self.seats[seat_num].reserve(reservation.reservation_id)
        return True

    def release_seats(self, seat_numbers: List[str]) -> bool:
        """Libera asientos (para cancelaciones)"""
        for seat_num in seat_numbers:
            if seat_num in self.seats:
                self.seats[seat_num].release()
        return True

    def schedule_movie(self, movie: Movie, date: str) -> bool:
        """Programa una película en esta sala"""
        if movie.room_type != self.hall_type:
            return False
        
        if date not in self.movie_schedule:
            self.movie_schedule[date] = []
        
        self.movie_schedule[date].append(movie)
        return True