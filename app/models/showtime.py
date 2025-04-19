from datetime import datetime, time
from typing import Dict

class Showtime:
    """
    Clase que representa un horario de función para una película.
    
    Attributes:
        showtime_id (int): Identificador único del horario.
        movie_id (int): ID de la película asociada.
        date (datetime.date): Fecha de la función.
        start_time (datetime.time): Hora de inicio.
        end_time (datetime.time): Hora estimada de finalización.
        jornada (str): Jornada (mañana, tarde, noche).
        available_seats (Dict): Asientos disponibles por tipo.
    """
    
    def __init__(self, showtime_id: int, movie_id: int, cinema_id: int,  # Añade cinema_id
                    date: datetime.date, start_time: time, end_time: time, 
                    jornada: str, available_seats: Dict[str, int]):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.cinema_id = cinema_id  # Nuevo campo
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.jornada = jornada
        self.available_seats = available_seats
    
    def to_dict(self) -> dict:
        return {
            "showtime_id": self.showtime_id,
            "movie_id": self.movie_id,
            "cinema_id": self.cinema_id,
            "date": self.date.strftime("%Y-%m-%d") if hasattr(self.date, 'strftime') else self.date,
            "start_time": self.start_time.strftime("%H:%M") if hasattr(self.start_time, 'strftime') else self.start_time,
            "end_time": self.end_time.strftime("%H:%M") if hasattr(self.end_time, 'strftime') else self.end_time,
            "jornada": self.jornada,
            "available_seats": self.available_seats
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Showtime':
        """Versión más robusta del método from_dict"""
        try:
            from datetime import datetime
            
            # Parseo seguro de fechas
            date_str = data.get('date', '')
            start_str = data.get('start_time', '')
            end_str = data.get('end_time', '')
            
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
            start_time = datetime.strptime(start_str, "%H:%M").time() if start_str else time(0, 0)
            end_time = datetime.strptime(end_str, "%H:%M").time() if end_str else time(0, 0)
            
            return cls(
                showtime_id=data["showtime_id"],
                movie_id=data["movie_id"],
                cinema_id=data["cinema_id"],
                date=date_obj,
                start_time=start_time,
                end_time=end_time,
                jornada=data.get("jornada", ""),
                available_seats=data.get("available_seats", {})
            )
        except ValueError as e:
            raise ValueError(f"Error al parsear datos del showtime: {str(e)}")