from datetime import datetime, time
from typing import Dict, List

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
    
    def __init__(self, showtime_id: int, movie_id: int, date: datetime.date, 
                    start_time: time, end_time: time, jornada: str, 
                    available_seats: Dict[str, int]):
        self.showtime_id = showtime_id
        self.movie_id = movie_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.jornada = jornada
        self.available_seats = available_seats
    
    def to_dict(self) -> dict:
        """Convierte el objeto Showtime a un diccionario."""
        return {
            "showtime_id": self.showtime_id,
            "movie_id": self.movie_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "start_time": self.start_time.strftime("%H:%M"),
            "end_time": self.end_time.strftime("%H:%M"),
            "jornada": self.jornada,
            "available_seats": self.available_seats
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Showtime':
        """Crea un objeto Showtime desde un diccionario."""
        from datetime import date
        return cls(
            showtime_id=data["showtime_id"],
            movie_id=data["movie_id"],
            date=date.fromisoformat(data["date"]),
            start_time=time.fromisoformat(data["start_time"]),
            end_time=time.fromisoformat(data["end_time"]),
            jornada=data["jornada"],
            available_seats=data["available_seats"]
        )