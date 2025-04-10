from typing import Literal, List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Ticket:
    """Clase base para tickets"""
    ticket_id: int
    user_id: int
    movie_id: int
    showtime: dict  # {date: str, time: str, session: str}
    room_type: Literal['2D', '3D']
    seats: List[str]
    ticket_type: Literal['general', 'preferential']
    price: float
    purchase_date: str
    status: Literal['active', 'used', 'cancelled'] = 'active'
    
    def to_dict(self) -> dict:
        return {
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'showtime': self.showtime,
            'room_type': self.room_type,
            'seats': self.seats,
            'ticket_type': self.ticket_type,
            'price': self.price,
            'purchase_date': self.purchase_date,
            'status': self.status,
            'type': 'standard'
        }

class FoodItem:
    """Clase para ítems de comida en una compra"""
    def __init__(self, item_id: int, quantity: int, unit_price: float):
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price
    
    def to_dict(self) -> dict:
        return {
            'item_id': self.item_id,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }

class Purchase:
    """Clase que representa una compra completa"""
    def __init__(self, purchase_id: int, user_id: int, tickets: List[Ticket], 
                    food_items: List[FoodItem], payment_method: str, 
                    total_amount: float, purchase_date: str):
        self.purchase_id = purchase_id
        self.user_id = user_id
        self.tickets = tickets
        self.food_items = food_items
        self.payment_method = payment_method
        self.total_amount = total_amount
        self.purchase_date = purchase_date
    
    def to_dict(self) -> dict:
        return {
            'purchase_id': self.purchase_id,
            'user_id': self.user_id,
            'tickets': [t.to_dict() for t in self.tickets],
            'food_items': [f.to_dict() for f in self.food_items],
            'payment_method': self.payment_method,
            'total_amount': self.total_amount,
            'purchase_date': self.purchase_date
        }

class Reservation:
    """Clase para reservaciones"""
    def __init__(self, reservation_id: int, user_id: int, movie_id: int, 
                    showtime: dict, seats: List[str], reservation_date: str, 
                    expiry_date: str, status: Literal['pending', 'confirmed', 'cancelled']):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.showtime = showtime
        self.seats = seats
        self.reservation_date = reservation_date
        self.expiry_date = expiry_date
        self.status = status
    
    def to_dict(self) -> dict:
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'showtime': self.showtime,
            'seats': self.seats,
            'reservation_date': self.reservation_date,
            'expiry_date': self.expiry_date,
            'status': self.status
        }