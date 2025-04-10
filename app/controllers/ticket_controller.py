from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models.ticket import Ticket, FoodItem, Purchase, Reservation
from models.cinema import CinemaHall
from services.ticket_pricing import calculate_ticket_price

class TicketController:
    def __init__(self, db, cinema_controller):
        self.db = db
        self.cinema_controller = cinema_controller
    
    def _get_next_id(self, items: List) -> int:
        return max(item.id for item in items) + 1 if items else 1
    
    def create_ticket(self, user_id: int, movie_id: int, showtime: dict, 
                    room_type: str, seat_numbers: List[str], ticket_type: str) -> Optional[Ticket]:
        try:
            # Verificar disponibilidad de asientos
            hall = self.cinema_controller.get_hall_for_showtime(room_type, showtime)
            if not hall or not all(hall.is_seat_available(seat) for seat in seat_numbers):
                return None
            
            # Calcular precio
            seat_type = hall.get_seat_type(seat_numbers[0])  # Todos los asientos del mismo tipo
            price = calculate_ticket_price(ticket_type, seat_type, showtime)
            
            # Crear ticket
            ticket = Ticket(
                ticket_id=self._get_next_id(self.db.get_all_tickets()),
                user_id=user_id,
                movie_id=movie_id,
                showtime=showtime,
                room_type=room_type,
                seats=seat_numbers,
                ticket_type=ticket_type,
                price=price,
                purchase_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            # Ocupar asientos
            if not self.cinema_controller.occupy_seats(room_type, showtime, seat_numbers, ticket.ticket_id):
                return None
            
            self.db.save_ticket(ticket)
            return ticket
        except Exception as e:
            print(f"Error creating ticket: {str(e)}")
            return None
    
    def create_purchase(self, user_id: int, tickets: List[Ticket], 
                        food_items: List[Dict], payment_method: str) -> Optional[Purchase]:
        try:
            # Validar tickets
            if not tickets:
                return None
                
            # Convertir food_items
            food_objects = [
                FoodItem(
                    item_id=item['item_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                ) for item in food_items
            ]
            
            # Calcular total
            total = sum(t.price for t in tickets) + sum(f.total_price for f in food_objects)
            
            purchase = Purchase(
                purchase_id=self._get_next_id(self.db.get_all_purchases()),
                user_id=user_id,
                tickets=tickets,
                food_items=food_objects,
                payment_method=payment_method,
                total_amount=total,
                purchase_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            self.db.save_purchase(purchase)
            return purchase
        except Exception as e:
            print(f"Error creating purchase: {str(e)}")
            # Liberar asientos si falla
            for ticket in tickets:
                self.cinema_controller.release_seats(ticket.room_type, ticket.showtime, ticket.seats)
            return None
    
    def create_reservation(self, user_id: int, movie_id: int, showtime: dict, 
                            room_type: str, seat_numbers: List[str]) -> Optional[Reservation]:
        try:
            # Verificar disponibilidad
            hall = self.cinema_controller.get_hall_for_showtime(room_type, showtime)
            if not hall or not all(hall.is_seat_available(seat) for seat in seat_numbers):
                return None
            
            # Crear reservación
            now = datetime.now()
            reservation = Reservation(
                reservation_id=self._get_next_id(self.db.get_all_reservations()),
                user_id=user_id,
                movie_id=movie_id,
                showtime=showtime,
                room_type=room_type,
                seats=seat_numbers,
                reservation_date=now.strftime("%Y-%m-%d %H:%M:%S"),
                expiry_date=(now + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
                status='pending'
            )
            
            # Reservar asientos
            if not self.cinema_controller.reserve_seats(room_type, showtime, seat_numbers, reservation.reservation_id):
                return None
            
            self.db.save_reservation(reservation)
            return reservation
        except Exception as e:
            print(f"Error creating reservation: {str(e)}")
            return None
    
    def confirm_reservation(self, reservation_id: int) -> Optional[Ticket]:
        """Convierte una reservación en ticket"""
        reservation = self.db.get_reservation(reservation_id)
        if not reservation or reservation.status != 'pending':
            return None
        
        try:
            # Crear ticket
            ticket = self.create_ticket(
                user_id=reservation.user_id,
                movie_id=reservation.movie_id,
                showtime=reservation.showtime,
                room_type=reservation.room_type,
                seat_numbers=reservation.seats,
                ticket_type='general'  # O se podría pedir al usuario
            )
            
            if ticket:
                reservation.status = 'confirmed'
                self.db.save_reservation(reservation)
                return ticket
            return None
        except Exception as e:
            print(f"Error confirming reservation: {str(e)}")
            return None
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        reservation = self.db.get_reservation(reservation_id)
        if not reservation:
            return False
        
        # Liberar asientos
        if not self.cinema_controller.release_seats(reservation.room_type, reservation.showtime, reservation.seats):
            return False
        
        reservation.status = 'cancelled'
        return self.db.save_reservation(reservation)
    
    def get_user_purchases(self, user_id: int) -> List[Purchase]:
        return [p for p in self.db.get_all_purchases() if p.user_id == user_id]
    
    def get_user_reservations(self, user_id: int) -> List[Reservation]:
        return [r for r in self.db.get_all_reservations() if r.user_id == user_id and r.status != 'cancelled']