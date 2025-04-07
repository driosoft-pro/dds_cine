from typing import List, Literal
from datetime import datetime

class Movie:
    """Clase que representa una película en el sistema."""
    
    def __init__(self, movie_id: int, title: str, release_year: int, director: str,
                gender: str, synopsis: str, duration: int, rating: str, 
                language: str, origin: str, room_type: Literal['2D', '3D'],
                showtimes: List[dict], hall: Literal['regular','premium'] = 'regular', 
                status: Literal['active', 'inactive'] = 'active'):
        """
        Inicializa una película con todos sus atributos.
        """
        self._movie_id = movie_id
        self._title = title
        self._release_year = release_year
        self._director = director
        self._gender = gender
        self._synopsis = synopsis
        self._duration = duration
        self._rating = rating
        self._language = language
        self._origin = origin
        self._room_type = room_type
        self._showtimes = showtimes
        self._hall = hall 
        self._status = status
    
    @property
    def movie_id(self) -> int:
        return self._movie_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def release_year(self) -> int:
        return self._release_year
    
    @property
    def director(self) -> str:
        return self._director
    
    @property
    def gender(self) -> str:
        return self._gender
    
    @property
    def synopsis(self) -> str:
        return self._synopsis
    
    @property
    def duration(self) -> int:
        return self._duration
    
    @property
    def rating(self) -> str:
        return self._rating
    
    @property
    def language(self) -> str:
        return self._language
    
    @property
    def origin(self) -> str:
        return self._origin
    
    @property
    def room_type(self) -> str:
        return self._room_type
    
    @property
    def showtimes(self) -> List[dict]:
        return self._showtimes

    @property
    def hall(self) -> str:
        return self._hall
    
    @hall.setter
    def hall(self, value: Literal['regular','premium']):
        self._hall = value
    
    @property
    def status(self) -> str:
        return self._status
    
    def to_dict(self) -> dict:
        """Convierte el objeto Movie a un diccionario para serialización."""
        return {
            "movie_id": self._movie_id,
            "title": self._title,
            "release_year": self._release_year,
            "director": self._director,
            "gender": self._gender,
            "synopsis": self._synopsis,
            "duration": self._duration,
            "rating": self._rating,
            "language": self._language,
            "origin": self._origin,
            "room_type": self._room_type,
            "showtimes": self._showtimes,
            "hall": self._hall,
            "status": self._status
        }
    
    @staticmethod
    def validate_rating(rating: str) -> bool:
        """Valida que el rating sea uno de los valores permitidos."""
        valid_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        return rating in valid_ratings
    
    @staticmethod
    def validate_showtime(showtime: dict) -> bool:
        """Valida que el showtime tenga el formato correcto."""
        required = ['date', 'time', 'session']
        return all(key in showtime for key in required)

class TwoDMovie(Movie):
    """Clase que representa una película 2D."""
    
    def __init__(self, movie_id: int, title: str, release_year: int, director: str,
                gender: str, synopsis: str, duration: int, rating: str, 
                language: str, origin: str, showtimes: List[dict],
                hall: Literal['regular','premium'] = 'regular', 
                status: Literal['active', 'inactive'] = 'active'):
        super().__init__(movie_id, title, release_year, director, gender, synopsis,
                        duration, rating, language, origin, '2D', showtimes, hall, status)
    
    def to_dict(self) -> dict:
        movie_dict = super().to_dict()
        movie_dict["type"] = "2d"
        return movie_dict

class ThreeDMovie(Movie):
    """Clase que representa una película 3D (regular o premium)."""
    
    def __init__(self, movie_id: int, title: str, release_year: int, director: str,
                gender: str, synopsis: str, duration: int, rating: str, 
                language: str, origin: str, showtimes: List[dict],
                hall: Literal['regular','premium'] = 'regular', 
                status: Literal['active', 'inactive'] = 'active'):
        super().__init__(movie_id, title, release_year, director, gender, synopsis,
                        duration, rating, language, origin, '3D', showtimes, hall, status)
    
    def to_dict(self) -> dict:
        movie_dict = super().to_dict()
        movie_dict["type"] = "3d"
        return movie_dict