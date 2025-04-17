from datetime import datetime
from typing import Dict, List, Optional
from models.reservation import Reservation
from core.database import Database

class ReservationController:
    """Controlador para manejar operaciones relacionadas con reservaciones."""
    
    def __init__(self, db: Database):
        self.db = db
        self.reservations_file = "reservations.json"
    
    def create_reservation(self, user_id: int, movie_id: int, showtime: datetime, 
                            seat_number: str, ticket_type: str, price: float) -> Dict:
        """Crea una nueva reservación."""
        reservations = self.db.load_data(self.reservations_file)
        reservation_id = self.db.get_next_id(self.reservations_file)
        
        new_reservation = Reservation(
            reservation_id=reservation_id,
            user_id=user_id,
            movie_id=movie_id,
            showtime=showtime,
            seat_number=seat_number,
            ticket_type=ticket_type,
            price=price
        )
        
        reservations.append(new_reservation.to_dict())
        self.db.save_data(self.reservations_file, reservations)
        return new_reservation.to_dict()
    
    def get_reservation_by_id(self, reservation_id: int) -> Optional[Dict]:
        """Obtiene una reservación por su ID."""
        reservations = self.db.load_data(self.reservations_file)
        for reservation in reservations:
            if reservation['reservation_id'] == reservation_id:
                return reservation
        return None
    
    def get_reservations_by_user(self, user_id: int) -> List[Dict]:
        """Obtiene todas las reservaciones de un usuario."""
        reservations = self.db.load_data(self.reservations_file)
        return [r for r in reservations if r['user_id'] == user_id and r['status'] == 'activo']
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        """Cancela una reservación (cambia su estado a inactivo)."""
        reservations = self.db.load_data(self.reservations_file)
        for i, reservation in enumerate(reservations):
            if reservation['reservation_id'] == reservation_id:
                reservations[i]['status'] = 'inactivo'
                self.db.save_data(self.reservations_file, reservations)
                return True
        return False
    
    def list_reservations(self, active_only: bool = True) -> List[Dict]:
        """Lista todas las reservaciones."""
        reservations = self.db.load_data(self.reservations_file)
        if active_only:
            return [r for r in reservations if r['status'] == 'activo']
        return reservations
    
    def convert_reservation_to_ticket(self, reservation_id: int) -> Optional[Dict]:
        """Convierte una reservación en un ticket."""
        reservation = self.get_reservation_by_id(reservation_id)
        if not reservation or reservation['status'] != 'activo':
            return None
        
        ticket_controller = TicketController(self.db)
        new_ticket = ticket_controller.create_ticket(
            user_id=reservation['user_id'],
            movie_id=reservation['movie_id'],
            showtime=reservation['showtime'],
            seat_number=reservation['seat_number'],
            ticket_type=reservation['ticket_type'],
            price=reservation['price']
        )
        
        if new_ticket:
            self.cancel_reservation(reservation_id)
            return new_ticket
        return None