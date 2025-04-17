from typing import Dict, List, Optional
from controllers.cinema_controller import CinemaController
from controllers.showtime_controller import ShowtimeController
from core.database import Database

class SeatService:
    """Servicio para manejar la disponibilidad de asientos."""
    
    def __init__(self, db: Database):
        self.cinema_controller = CinemaController(db)
        self.showtime_controller = ShowtimeController(db)
    
    def get_available_seats(self, cinema_id: int, showtime_id: int) -> Dict[str, int]:
        """Obtiene los asientos disponibles para una función específica."""
        cinema = self.cinema_controller.get_cinema_by_id(cinema_id)
        showtime = self.showtime_controller.get_showtime_by_id(showtime_id)
        
        if not cinema or not showtime:
            return {}
        
        # Obtener el mínimo entre los asientos disponibles en la sala y en la función
        available_seats = {}
        for seat_type in cinema['available_seats']:
            cinema_seats = cinema['available_seats'].get(seat_type, 0)
            showtime_seats = showtime['available_seats'].get(seat_type, 0)
            available_seats[seat_type] = min(cinema_seats, showtime_seats)
        
        return available_seats
    
    def reserve_seat(self, cinema_id: int, showtime_id: int, 
                    seat_type: str, quantity: int = 1) -> bool:
        """Reserva uno o más asientos de un tipo específico."""
        # Actualizar disponibilidad en la sala
        cinema_updated = self.cinema_controller.update_available_seats(
            cinema_id, seat_type, -quantity)
        
        # Actualizar disponibilidad en la función
        showtime_updated = self.showtime_controller.update_available_seats(
            showtime_id, seat_type, -quantity)
        
        return cinema_updated and showtime_updated
    
    def release_seat(self, cinema_id: int, showtime_id: int, 
                    seat_type: str, quantity: int = 1) -> bool:
        """Libera uno o más asientos previamente reservados."""
        # Actualizar disponibilidad en la sala
        cinema_updated = self.cinema_controller.update_available_seats(
            cinema_id, seat_type, quantity)
        
        # Actualizar disponibilidad en la función
        showtime_updated = self.showtime_controller.update_available_seats(
            showtime_id, seat_type, quantity)
        
        return cinema_updated and showtime_updated
    
    def generate_seat_numbers(self, seat_type: str, quantity: int) -> List[str]:
        """Genera números de asiento para un tipo específico."""
        prefix = {
            'general': 'G',
            'preferencial': 'P'
        }.get(seat_type, 'S')
        
        return [f"{prefix}{i+1:03d}" for i in range(quantity)]