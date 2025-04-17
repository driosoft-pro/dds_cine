from datetime import datetime
from typing import List, Dict

class Movie:
    """
    Clase que representa una película en el sistema.
    
    Attributes:
        movie_id (int): Identificador único de la película.
        title (str): Título de la película.
        release_year (int): Año de lanzamiento.
        director (str): Director de la película.
        category (str): Categoría (acción, comedia, etc.).
        synopsis (str): Sinopsis de la película.
        duration (int): Duración en minutos.
        age_rating (str): Clasificación por edad (G, PG, etc.).
        language (str): Idioma principal.
        origin (str): País de origen.
        room_type (str): Tipo de sala (2D o 3D).
        showtimes (List[Dict]): Lista de horarios disponibles.
        hall (str): Tipo de sala (regular, premium).
        ticket_price (float): Precio base del ticket.
        available_seats (Dict): Asientos disponibles por tipo.
        status (str): Estado (activo/inactivo).
    """
    
    def __init__(self, movie_id: int, title: str, release_year: int, director: str, 
                    category: str, synopsis: str, duration: int, age_rating: str, 
                    language: str, origin: str, room_type: str, showtimes: List[Dict], 
                    hall: str, ticket_price: float, available_seats: Dict, status: str = "activo"):
        self.movie_id = movie_id
        self.title = title
        self.release_year = release_year
        self.director = director
        self.category = category
        self.synopsis = synopsis
        self.duration = duration
        self.age_rating = age_rating
        self.language = language
        self.origin = origin
        self.room_type = room_type
        self.showtimes = showtimes
        self.hall = hall
        self.ticket_price = ticket_price
        self.available_seats = available_seats
        self.status = status
    
    def to_dict(self) -> dict:
        """Convierte el objeto Movie a un diccionario."""
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "release_year": self.release_year,
            "director": self.director,
            "category": self.category,
            "synopsis": self.synopsis,
            "duration": self.duration,
            "age_rating": self.age_rating,
            "language": self.language,
            "origin": self.origin,
            "room_type": self.room_type,
            "showtimes": self.showtimes,
            "hall": self.hall,
            "ticket_price": self.ticket_price,
            "available_seats": self.available_seats,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Movie':
        """Crea un objeto Movie desde un diccionario."""
        return cls(
            movie_id=data["movie_id"],
            title=data["title"],
            release_year=data["release_year"],
            director=data["director"],
            category=data["category"],
            synopsis=data["synopsis"],
            duration=data["duration"],
            age_rating=data["age_rating"],
            language=data["language"],
            origin=data["origin"],
            room_type=data["room_type"],
            showtimes=data["showtimes"],
            hall=data["hall"],
            ticket_price=data["ticket_price"],
            available_seats=data["available_seats"],
            status=data.get("status", "activo")
        )