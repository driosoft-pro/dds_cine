from datetime import datetime
from typing import Optional

class Reservation:
    """
    Clase que representa una reservación de entradas.
    
    Attributes:
        reservation_id (int): Identificador único de la reserva.
        user_id (int): ID del usuario que hizo la reserva.
        movie_id (int): ID de la película asociada.
        showtime (datetime): Fecha y hora de la función.
        seat_number (str): Número/Nombre del asiento.
        ticket_type (str): Tipo de ticket (general/preferencial).
        price (float): Precio a pagar.
        status (str): Estado de la reserva (activo/inactivo).
    """
    
    def __init__(self, reservation_id: int, user_id: int, movie_id: int, 
                    showtime: datetime, seat_number: str, ticket_type: str, 
                    price: float, status: str = "activo"):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime = showtime
        self.seat_number = seat_number
        self.ticket_type = ticket_type
        self.price = price
        self.status = status
    
    def to_dict(self) -> dict:
        """Convierte el objeto Reservation a un diccionario."""
        return {
            "reservation_id": self.reservation_id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "showtime": self.showtime.strftime("%Y-%m-%d %H:%M"),
            "seat_number": self.seat_number,
            "ticket_type": self.ticket_type,
            "price": self.price,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reservation':
        """Crea un objeto Reservation desde un diccionario."""
        return cls(
            reservation_id=data["reservation_id"],
            user_id=data["user_id"],
            movie_id=data["movie_id"],
            showtime=datetime.strptime(data["showtime"], "%Y-%m-%d %H:%M"),
            seat_number=data["seat_number"],
            ticket_type=data["ticket_type"],
            price=data["price"],
            status=data.get("status", "activo")
        )