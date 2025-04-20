from datetime import datetime
from typing import Optional

class Reservation:
    def __init__(self, reservation_id: int, user_id: int, movie_id: int, 
                    showtime: str, seat_number: str, ticket_type: str, 
                    price: float, status: str = "activo",
                    reservation_code: Optional[str] = None,
                    created_at: Optional[str] = None,
                    expiration_date: Optional[str] = None,
                    cancelled_at: Optional[str] = None,
                    **kwargs):  # Acepta argumentos adicionales sin errores
        """
        Modelo simplificado de reservación.
        """
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime = showtime
        self.seat_number = seat_number
        self.ticket_type = ticket_type
        self.price = price
        self.status = status
        self.reservation_code = reservation_code or self._generate_code()
        self.created_at = created_at or datetime.now().isoformat()
        self.expiration_date = expiration_date or (datetime.now() + datetime.timedelta(hours=24)).isoformat()
        self.cancelled_at = cancelled_at
        
        # Maneja cualquier parámetro adicional (como showtime_id)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _generate_code(self) -> str:
        """Genera un código de reserva único."""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def to_dict(self) -> dict:
        """Convierte todos los atributos a diccionario."""
        return vars(self)