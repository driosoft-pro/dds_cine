from datetime import datetime
from typing import Dict, List, Optional
from models.ticket import Ticket
from core.database import Database

class TicketController:
    """Controlador para manejar operaciones relacionadas con tickets."""
    
    def __init__(self, db: Database):
        self.db = db
        self.tickets_file = "tickets.json"
    
    def create_ticket(self, user_id: int, movie_id: int, showtime: datetime, 
                        seat_number: str, ticket_type: str, price: float) -> Dict:
        """Crea un nuevo ticket."""
        tickets = self.db.load_data(self.tickets_file)
        ticket_id = self.db.get_next_id("tickets.json", "ticket_id")
        
        
        new_ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            movie_id=movie_id,
            showtime=showtime,
            seat_number=seat_number,
            ticket_type=ticket_type,
            price=price
        )
        
        tickets.append(new_ticket.to_dict())
        self.db.save_data(self.tickets_file, tickets)
        return new_ticket.to_dict()
    
    def get_ticket_by_id(self, ticket_id: int) -> Optional[Dict]:
        """Obtiene un ticket por su ID."""
        tickets = self.db.load_data(self.tickets_file)
        for ticket in tickets:
            if ticket['ticket_id'] == ticket_id:
                return ticket
        return None
    
    def get_tickets_by_user(self, user_id: int) -> List[Dict]:
        """Obtiene todos los tickets de un usuario."""
        tickets = self.db.load_data(self.tickets_file)
        return [t for t in tickets if t['user_id'] == user_id and t['status'] == 'activo']
    
    def cancel_ticket(self, ticket_id: int) -> bool:
        """Cancela un ticket (cambia su estado a inactivo)."""
        tickets = self.db.load_data(self.tickets_file)
        for i, ticket in enumerate(tickets):
            if ticket['ticket_id'] == ticket_id:
                tickets[i]['status'] = 'inactivo'
                self.db.save_data(self.tickets_file, tickets)
                return True
        return False
    
    def list_tickets(self, active_only: bool = True) -> List[Dict]:
        """Lista todos los tickets."""
        tickets = self.db.load_data(self.tickets_file)
        if active_only:
            return [t for t in tickets if t['status'] == 'activo']
        return tickets