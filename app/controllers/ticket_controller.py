from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models.ticket import Ticket, FoodItem, Purchase, Reservation

class TicketController:
    def __init__(self, db):
        self.db = db
    
    def get_next_ticket_id(self) -> int:
        tickets = self.db.get_all_tickets()
        return max(t.ticket_id for t in tickets) + 1 if tickets else 1
    
    def get_next_purchase_id(self) -> int:
        purchases = self.db.get_all_purchases()
        return max(p.purchase_id for p in purchases) + 1 if purchases else 1
    
    def get_next_reservation_id(self) -> int:
        reservations = self.db.get_all_reservations()
        return max(r.reservation_id for r in reservations) + 1 if reservations else 1
    
    def create_ticket(self, user_id: int, movie_id: int, showtime: dict, 
                        room_type: str, seats: List[str], ticket_type: str, 
                        price: float) -> Optional[Ticket]:
        try:
            ticket = Ticket(
                ticket_id=self.get_next_ticket_id(),
                user_id=user_id,
                movie_id=movie_id,
                showtime=showtime,
                room_type=room_type,
                seats=seats,
                ticket_type=ticket_type,
                price=price,
                purchase_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            self.db.save_ticket(ticket)
            return ticket
        except Exception as e:
            print(f"Error creating ticket: {e}")
            return None
    
    def create_purchase(self, user_id: int, tickets: List[Ticket], 
                        food_items: List[Dict], payment_method: str) -> Optional[Purchase]:
        try:
            # Convertir food_items a objetos FoodItem
            food_objects = [
                FoodItem(
                    item_id=item['item_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price']
                ) for item in food_items
            ]
            
            # Calcular total
            tickets_total = sum(t.price for t in tickets)
            food_total = sum(f.total_price for f in food_objects)
            total = tickets_total + food_total
            
            purchase = Purchase(
                purchase_id=self.get_next_purchase_id(),
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
            print(f"Error creating purchase: {e}")
            return None
    
    def create_reservation(self, user_id: int, movie_id: int, showtime: dict, 
                            seats: List[str]) -> Optional[Reservation]:
        try:
            now = datetime.now()
            reservation = Reservation(
                reservation_id=self.get_next_reservation_id(),
                user_id=user_id,
                movie_id=movie_id,
                showtime=showtime,
                seats=seats,
                reservation_date=now.strftime("%Y-%m-%d %H:%M:%S"),
                expiry_date=(now + timedelta(days=2)).strftime("%Y-%m-%d"),
                status='pending'
            )
            self.db.save_reservation(reservation)
            return reservation
        except Exception as e:
            print(f"Error creating reservation: {e}")
            return None
    
    def confirm_reservation(self, reservation_id: int) -> bool:
        reservation = self.db.get_reservation(reservation_id)
        if not reservation:
            return False
        
        reservation.status = 'confirmed'
        return self.db.save_reservation(reservation)
    
    def cancel_ticket(self, ticket_id: int) -> bool:
        ticket = self.db.get_ticket(ticket_id)
        if not ticket:
            return False
        
        ticket.status = 'cancelled'
        return self.db.save_ticket(ticket)
    
    def get_user_purchases(self, user_id: int) -> List[Purchase]:
        return [p for p in self.db.get_all_purchases() if p.user_id == user_id]
    
    def get_user_reservations(self, user_id: int) -> List[Reservation]:
        return [r for r in self.db.get_all_reservations() if r.user_id == user_id]