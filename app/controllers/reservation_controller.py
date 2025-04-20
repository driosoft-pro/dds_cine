from datetime import datetime
from typing import Dict, List, Optional, Union
from models.reservation import Reservation
from core.database import Database

class ReservationController:
    def __init__(self, db: Database):
        self.db = db
        self.reservations_file = "reservations.json"
    
    def create_reservation(self, user_id: int, movie_id: int, 
                            showtime: str, seat_number: str, 
                            ticket_type: str, price: float, 
                            **extra_fields) -> Dict:
        """
        Crea reserva con los campos esenciales + cualquier campo adicional.
        """
        reservations = self.db.load_data(self.reservations_file)
        
        new_reservation = Reservation(
            reservation_id=self.db.get_next_id(self.reservations_file),
            user_id=user_id,
            movie_id=movie_id,
            showtime=showtime,
            seat_number=seat_number,
            ticket_type=ticket_type,
            price=price,
            **extra_fields  # Pasa cualquier campo adicional
        )
        
        reservations.append(new_reservation.to_dict())
        self.db.save_data(self.reservations_file, reservations)
        return new_reservation.to_dict()
    def _parse_datetime(self, dt: Union[datetime, str]) -> str:
        """Convierte datetime a string ISO o valida formato."""
        if isinstance(dt, datetime):
            return dt.isoformat()
        elif isinstance(dt, str):
            try:
                datetime.fromisoformat(dt)  # Validar formato
                return dt
            except ValueError:
                raise ValueError("Formato de fecha inválido. Use ISO (YYYY-MM-DD HH:MM:SS)")
        raise ValueError("Fecha debe ser datetime o string ISO")

    def get_reservation_by_id(self, reservation_id: int) -> Optional[Dict]:
        """Obtiene una reservación por su ID."""
        if not isinstance(reservation_id, int) or reservation_id <= 0:
            raise ValueError("ID de reserva inválido")
            
        reservations = self.db.load_data(self.reservations_file)
        return next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    
    def get_reservations_by_user(self, user_id: int, active_only: bool = True) -> List[Dict]:
        """Obtiene reservaciones de un usuario, con filtro por estado."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("ID de usuario inválido")
            
        reservations = self.db.load_data(self.reservations_file)
        if active_only:
            return [r for r in reservations 
                    if r['user_id'] == user_id and r['status'] == 'activo']
        return [r for r in reservations if r['user_id'] == user_id]
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        """Cancela una reservación si no ha expirado."""
        reservations = self.db.load_data(self.reservations_file)
        for i, r in enumerate(reservations):
            if r['reservation_id'] == reservation_id:
                # Verificar si ya está cancelada
                if r['status'] == 'inactivo':
                    return False
                    
                # Verificar expiración
                exp_date = datetime.fromisoformat(r['expiration_date'])
                if datetime.now() > exp_date:
                    raise ValueError("No se puede cancelar una reserva expirada")
                
                reservations[i]['status'] = 'inactivo'
                reservations[i]['cancelled_at'] = datetime.now().isoformat()
                self.db.save_data(self.reservations_file, reservations)
                return True
        return False
    
    def convert_reservation_to_ticket(self, reservation_id: int) -> Optional[Dict]:
        """Convierte una reserva activa y válida en ticket."""
        from controllers.ticket_controller import TicketController  # Importación local
        
        reservation = self.get_reservation_by_id(reservation_id)
        if not reservation or reservation['status'] != 'activo':
            return None
            
        # Verificar que no haya expirado
        if datetime.fromisoformat(reservation['expiration_date']) < datetime.now():
            raise ValueError("La reserva ha expirado y no puede convertirse")
        
        try:
            ticket_controller = TicketController(self.db)
            
            # Asegurar que showtime sea un objeto datetime
            showtime_str = reservation['showtime']
            try:
                showtime = datetime.fromisoformat(showtime_str)
            except ValueError:
                # Si el formato no es ISO, intentar otro formato común
                showtime = datetime.strptime(showtime_str, "%Y-%m-%d %H:%M:%S")
            
            new_ticket = ticket_controller.create_ticket(
                user_id=reservation['user_id'],
                movie_id=reservation['movie_id'],
                showtime=showtime,  # datetime object
                seat_number=reservation['seat_number'],
                ticket_type=reservation['ticket_type'],
                price=reservation['price']
            )
            
            if new_ticket:
                self.cancel_reservation(reservation_id)
                return new_ticket
        except Exception as e:
            raise ValueError(f"Error al convertir reserva: {str(e)}")
        
        return None
    
    def validate_reservation_code(self, code: str) -> bool:
        """Valida que un código de reserva exista y esté activo."""
        reservations = self.db.load_data(self.reservations_file)
        return any(r['reservation_code'] == code and r['status'] == 'activo' 
                    for r in reservations)