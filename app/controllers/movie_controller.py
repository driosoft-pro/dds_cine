from typing import List, Optional, Dict, Literal
from models.movie import Movie, TwoDMovie, ThreeDMovie

class MovieController:
    """Controlador para gestionar películas del sistema."""
    
    def __init__(self, db):
        self.db = db

    def get_active_movies(self) -> List[Movie]:
        # Implementación real que consulta la base de datos
        return [m for m in self.db.get_all_movies() if m.status == 'active']
    
    def get_next_movie_id(self) -> int:
        """Obtiene el próximo ID autoincremental para una nueva película."""
        movies = self.db.get_all_movies()
        return max(movie.movie_id for movie in movies) + 1 if movies else 1
    
    def create_movie(self, movie_data: Dict, movie_type: Literal['2D', '3D']) -> Optional[Movie]:
        """
        Crea una nueva película en el sistema.
        """
        try:
            # Validar datos requeridos
            required_fields = [
                'title', 'release_year', 'director', 'gender', 'synopsis',
                'duration', 'rating', 'language', 'origin', 'showtimes', 'hall'
            ]
            if not all(field in movie_data for field in required_fields):
                return None
            
            # Validar rating
            if not Movie.validate_rating(movie_data['rating']):
                return None
            
            # Validar showtimes
            if not all(Movie.validate_showtime(st) for st in movie_data['showtimes']):
                return None
            
            # Obtener próximo ID
            movie_id = self.get_next_movie_id()
            
            # Crear instancia según el tipo de película
            common_args = {
                'movie_id': movie_id,
                'title': movie_data['title'],
                'release_year': movie_data['release_year'],
                'director': movie_data['director'],
                'gender': movie_data['gender'],
                'synopsis': movie_data['synopsis'],
                'duration': movie_data['duration'],
                'rating': movie_data['rating'],
                'language': movie_data['language'],
                'origin': movie_data['origin'],
                'showtimes': movie_data['showtimes'],
                'hall': movie_data['hall']
            }
            
            if movie_type == '2D':
                movie = TwoDMovie(**common_args)
            else:
                movie = ThreeDMovie(**common_args)
            
            self.db.save_movie(movie)
            return movie
            
        except Exception as e:
            print(f"Error creating movie: {e}")
            return None
    
    def get_movie(self, movie_id: int) -> Optional[Movie]:
        """Obtiene una película por su ID."""
        return self.db.get_movie(movie_id)
    
    def get_all_movies(self) -> List[Movie]:
        """Obtiene todas las películas del sistema."""
        return self.db.get_all_movies()
    
    def get_movies_by_room(self, room_type: str) -> List[Movie]:
        """Obtiene películas por tipo de sala (2D/3D)."""
        return [m for m in self.db.get_all_movies() if m.room_type == room_type]
    
    def update_movie(self, movie_id: int, update_data: Dict) -> Optional[Movie]:
        """Actualiza los datos de una película."""
        movie = self.get_movie(movie_id)
        if not movie:
            return None
        
        # Actualizar campos permitidos
        allowed_fields = {
            'title', 'release_year', 'director', 'gender', 'synopsis',
            'duration', 'rating', 'language', 'origin', 'showtimes',
            'hall', 'status'
        }
        
        for field, value in update_data.items():
            if field in allowed_fields and hasattr(movie, f"_{field}"):
                setattr(movie, f"_{field}", value)
        
        self.db.save_movie(movie)
        return movie
    
    def change_movie_status(self, movie_id: int, status: Literal['active', 'inactive']) -> bool:
        """Cambia el estado de una película (active/inactive)."""
        movie = self.get_movie(movie_id)
        if not movie:
            return False
        
        movie._status = status
        self.db.save_movie(movie)
        return True

    def search_movies(self, search_criteria: dict) -> List[Movie]:
        """
        Busca películas según múltiples criterios.
        
        Args:
            search_criteria: Diccionario con criterios de búsqueda.
                Puede incluir: title, gender, rating, room_type, status
                
        Returns:
            Lista de películas que coinciden con los criterios.
        """
        all_movies = self.get_all_movies()
        results = all_movies
        
        if 'title' in search_criteria:
            term = search_criteria['title'].lower()
            results = [m for m in results if term in m.title.lower()]
        
        if 'gender' in search_criteria:
            term = search_criteria['gender'].lower()
            results = [m for m in results if term in m.gender.lower()]
        
        if 'rating' in search_criteria:
            results = [m for m in results if m.rating == search_criteria['rating']]
        
        if 'room_type' in search_criteria:
            results = [m for m in results if m.room_type == search_criteria['room_type']]
        
        if 'status' in search_criteria:
            results = [m for m in results if m.status == search_criteria['status']]
        
        return results

    def get_active_movies(self) -> List[Movie]:
        """Obtiene todas las películas activas."""
        return [m for m in self.get_all_movies() if m.status == 'active']

    def get_movies_by_date(self, date: str) -> List[Movie]:
        """
        Obtiene películas que tienen funciones en una fecha específica.
        Formato de fecha: YYYY-MM-DD
        """
        try:
            movies_with_showtimes = []
            for movie in self.get_active_movies():
                matching_showtimes = [st for st in movie.showtimes if st['date'] == date]
                if matching_showtimes:
                    movie_copy = self._copy_movie_with_showtimes(movie, matching_showtimes)
                    movies_with_showtimes.append(movie_copy)
            return movies_with_showtimes
        except Exception:
            return []

    def _copy_movie_with_showtimes(self, movie: Movie, showtimes: List[dict]) -> Movie:
        """Crea una copia de la película con solo los showtimes especificados."""
        common_args = {
            'movie_id': movie.movie_id,
            'title': movie.title,
            'release_year': movie.release_year,
            'director': movie.director,
            'gender': movie.gender,
            'synopsis': movie.synopsis,
            'duration': movie.duration,
            'rating': movie.rating,
            'language': movie.language,
            'origin': movie.origin,
            'showtimes': showtimes,
            'hall': movie.hall,
            'status': movie.status
        }
        
        return ThreeDMovie(**common_args) if isinstance(movie, ThreeDMovie) else TwoDMovie(**common_args)