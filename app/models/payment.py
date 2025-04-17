from datetime import datetime
from typing import Optional

class Payment:
    """
    Clase que representa un pago en el sistema.
    
    Attributes:
        payment_id (int): Identificador único del pago.
        user_id (int): ID del usuario que realizó el pago.
        ticket_id (Optional[int]): ID del ticket asociado (si aplica).
        reservation_id (Optional[int]): ID de la reserva asociada (si aplica).
        amount (float): Monto pagado.
        payment_method (str): Método de pago (efectivo, tarjeta, transferencia).
        status (str): Estado del pago (activo/inactivo).
    """
    
    def __init__(self, payment_id: int, user_id: int, amount: float, 
                    payment_method: str, ticket_id: Optional[int] = None, 
                    reservation_id: Optional[int] = None, status: str = "activo"):
        self.payment_id = payment_id
        self.user_id = user_id
        self.ticket_id = ticket_id
        self.reservation_id = reservation_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
    
    def to_dict(self) -> dict:
        """Convierte el objeto Payment a un diccionario."""
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "ticket_id": self.ticket_id,
            "reservation_id": self.reservation_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Payment':
        """Crea un objeto Payment desde un diccionario."""
        return cls(
            payment_id=data["payment_id"],
            user_id=data["user_id"],
            ticket_id=data.get("ticket_id"),
            reservation_id=data.get("reservation_id"),
            amount=data["amount"],
            payment_method=data["payment_method"],
            status=data.get("status", "activo")
        )