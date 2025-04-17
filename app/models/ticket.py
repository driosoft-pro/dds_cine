from datetime import datetime
from typing import Optional

class Ticket:
    """
    Clase que representa un ticket de entrada al cine.
    
    Attributes:
        ticket_id (int): Identificador único del ticket.
        user_id (int): ID del usuario que compró el ticket.
        movie_id (int): ID de la película asociada.
        showtime (datetime): Fecha y hora de la función.
        seat_number (str): Número/Nombre del asiento.
        ticket_type (str): Tipo de ticket (general/preferencial).
        price (float): Precio pagado.
        status (str): Estado del ticket (activo/inactivo).
    """
    
    def __init__(self, ticket_id: int, user_id: int, movie_id: int, 
                    showtime: datetime, seat_number: str, ticket_type: str, 
                    price: float, status: str = "activo"):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime = showtime
        self.seat_number = seat_number
        self.ticket_type = ticket_type
        self.price = price
        self.status = status
    
    def to_dict(self) -> dict:
        """Convierte el objeto Ticket a un diccionario."""
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "showtime": self.showtime.strftime("%Y-%m-%d %H:%M"),
            "seat_number": self.seat_number,
            "ticket_type": self.ticket_type,
            "price": self.price,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Ticket':
        """Crea un objeto Ticket desde un diccionario."""
        return cls(
            ticket_id=data["ticket_id"],
            user_id=data["user_id"],
            movie_id=data["movie_id"],
            showtime=datetime.strptime(data["showtime"], "%Y-%m-%d %H:%M"),
            seat_number=data["seat_number"],
            ticket_type=data["ticket_type"],
            price=data["price"],
            status=data.get("status", "activo")
        )