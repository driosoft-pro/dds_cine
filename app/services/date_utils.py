from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class DateUtils:
    """Utilidades para manejo de fechas y horarios."""
    
    @staticmethod
    def is_valid_reservation_date(showtime_date: datetime) -> Tuple[bool, str]:
        """Valida que una fecha de reserva esté dentro del rango permitido (2-7 días)."""
        today = datetime.now()
        min_date = today + timedelta(days=2)
        max_date = today + timedelta(days=7)
        
        if showtime_date < min_date:
            return False, "La reserva debe hacerse con al menos 2 días de anticipación"
        if showtime_date > max_date:
            return False, "La reserva no puede hacerse con más de 7 días de anticipación"
        return True, "Fecha de reserva válida"
    
    @staticmethod
    def is_valid_cancellation_date(showtime_date: datetime) -> Tuple[bool, str]:
        """Valida que una cancelación esté dentro del rango permitido (1-2 días antes)."""
        today = datetime.now()
        min_date = today + timedelta(days=1)
        max_date = today + timedelta(days=2)
        
        if showtime_date < min_date:
            return False, "La cancelación debe hacerse con al menos 1 día de anticipación"
        if showtime_date > max_date:
            return False, "La cancelación no puede hacerse con más de 2 días de anticipación"
        return True, "Fecha de cancelación válida"
    
    @staticmethod
    def generate_showtimes(start_date: datetime, days: int = 15) -> List[Dict]:
        """Genera horarios de funciones para un período de días."""
        showtimes = []
        jornadas = ['mañana', 'tarde', 'noche']
        times = {
            'mañana': ('09:00', '12:00'),
            'tarde': ('15:00', '18:00'),
            'noche': ('20:00', '23:00')
        }
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            for jornada in jornadas:
                start_time, end_time = times[jornada]
                showtimes.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'start_time': start_time,
                    'end_time': end_time,
                    'jornada': jornada
                })
        
        return showtimes