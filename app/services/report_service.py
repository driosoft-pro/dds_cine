from typing import Dict
from datetime import datetime
from controllers import (
    TicketController, 
    ReservationController,
    PaymentController,
    MovieController,
    UserController
)
from core.database import Database

class ReportService:
    """Servicio para generar reportes y estadísticas."""
    
    def __init__(self, db: Database):
        self.ticket_controller = TicketController(db)
        self.reservation_controller = ReservationController(db)
        self.payment_controller = PaymentController(db)
        self.movie_controller = MovieController(db)
        self.user_controller = UserController(db)
    
    def generate_sales_report(self, start_date: datetime = None, 
                            end_date: datetime = None) -> Dict:
        """Genera un reporte de ventas en un rango de fechas."""
        tickets = self.ticket_controller.list_tickets()
        reservations = self.reservation_controller.list_reservations()
        payments = self.payment_controller.list_payments()
        
        if start_date and end_date:
            tickets = [t for t in tickets if start_date <= datetime.strptime(
                t['showtime'], '%Y-%m-%d %H:%M') <= end_date]
            reservations = [r for r in reservations if start_date <= datetime.strptime(
                r['showtime'], '%Y-%m-%d %H:%M') <= end_date]
            payments = [p for p in payments if start_date <= datetime.strptime(
                p.get('payment_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d') <= end_date]
        
        total_sales = sum(t['price'] for t in tickets) + sum(r['price'] for r in reservations)
        total_payments = sum(p['amount'] for p in payments)
        
        return {
            'total_tickets': len(tickets),
            'total_reservations': len(reservations),
            'total_sales': total_sales,
            'total_payments': total_payments,
            'tickets': tickets,
            'reservations': reservations,
            'payments': payments
        }
    
    def generate_movie_report(self, movie_id: int = None) -> Dict:
        """Genera un reporte de ventas por película."""
        tickets = self.ticket_controller.list_tickets()
        reservations = self.reservation_controller.list_reservations()
        
        if movie_id:
            tickets = [t for t in tickets if t['movie_id'] == movie_id]
            reservations = [r for r in reservations if r['movie_id'] == movie_id]
        
        movies = {}
        for ticket in tickets:
            movie_id = ticket['movie_id']
            if movie_id not in movies:
                movie = self.movie_controller.get_movie_by_id(movie_id)
                movies[movie_id] = {
                    'movie': movie,
                    'tickets': 0,
                    'reservations': 0,
                    'total': 0
                }
            movies[movie_id]['tickets'] += 1
            movies[movie_id]['total'] += ticket['price']
        
        for reservation in reservations:
            movie_id = reservation['movie_id']
            if movie_id not in movies:
                movie = self.movie_controller.get_movie_by_id(movie_id)
                movies[movie_id] = {
                    'movie': movie,
                    'tickets': 0,
                    'reservations': 0,
                    'total': 0
                }
            movies[movie_id]['reservations'] += 1
            movies[movie_id]['total'] += reservation['price']
        
        return movies
    
    def generate_user_report(self, user_id: int = None) -> Dict:
        """Genera un reporte de actividad por usuario."""
        tickets = self.ticket_controller.list_tickets()
        reservations = self.reservation_controller.list_reservations()
        payments = self.payment_controller.list_payments()
        
        if user_id:
            tickets = [t for t in tickets if t['user_id'] == user_id]
            reservations = [r for r in reservations if r['user_id'] == user_id]
            payments = [p for p in payments if p['user_id'] == user_id]
        
        users = {}
        for ticket in tickets:
            user_id = ticket['user_id']
            if user_id not in users:
                user = self.user_controller.get_user_by_id(user_id)
                users[user_id] = {
                    'user': user,
                    'tickets': 0,
                    'reservations': 0,
                    'payments': 0,
                    'total_spent': 0
                }
            users[user_id]['tickets'] += 1
            users[user_id]['total_spent'] += ticket['price']
        
        for reservation in reservations:
            user_id = reservation['user_id']
            if user_id not in users:
                user = self.user_controller.get_user_by_id(user_id)
                users[user_id] = {
                    'user': user,
                    'tickets': 0,
                    'reservations': 0,
                    'payments': 0,
                    'total_spent': 0
                }
            users[user_id]['reservations'] += 1
            users[user_id]['total_spent'] += reservation['price']
        
        for payment in payments:
            user_id = payment['user_id']
            if user_id not in users:
                user = self.user_controller.get_user_by_id(user_id)
                users[user_id] = {
                    'user': user,
                    'tickets': 0,
                    'reservations': 0,
                    'payments': 0,
                    'total_spent': 0
                }
            users[user_id]['payments'] += 1
        
        return users