from datetime import datetime
from typing import Dict, List, Optional
from models.movie import Movie
from core.database import Database

class MovieController:
    """Controlador para manejar operaciones relacionadas con películas."""
    
    def __init__(self, db: Database):
        self.db = db
        self.movies_file = "movies.json"
    
    def create_movie(self, title: str, release_year: int, director: str, 
                    category: str, synopsis: str, duration: int, 
                    age_rating: str, language: str, origin: str, 
                    room_type: str, showtimes: List[Dict], hall: str, 
                    ticket_price: float, available_seats: Dict) -> Dict:
        """Crea una nueva película."""
        movies = self.db.load_data(self.movies_file)
        movie_id = self.db.get_next_id("movies.json", "movie_id")
        
        new_movie = Movie(
            movie_id=movie_id,
            title=title,
            release_year=release_year,
            director=director,
            category=category,
            synopsis=synopsis,
            duration=duration,
            age_rating=age_rating,
            language=language,
            origin=origin,
            room_type=room_type,
            showtimes=showtimes,
            hall=hall,
            ticket_price=ticket_price,
            available_seats=available_seats
        )
        
        movies.append(new_movie.to_dict())
        self.db.save_data(self.movies_file, movies)
        return new_movie.to_dict()
    
    def get_movie_by_id(self, movie_id: int) -> Optional[Dict]:
        """Obtiene una película por su ID."""
        movies = self.db.load_data(self.movies_file)
        for movie in movies:
            if movie['movie_id'] == movie_id:
                return movie
        return None
    
    def update_movie(self, movie_id: int, **kwargs) -> Optional[Dict]:
        """Actualiza los datos de una película."""
        movies = self.db.load_data(self.movies_file)
        for i, movie in enumerate(movies):
            if movie['movie_id'] == movie_id:
                for key, value in kwargs.items():
                    if key in movie and key != 'movie_id':
                        movies[i][key] = value
                self.db.save_data(self.movies_file, movies)
                return movies[i]
        return None
    
    def delete_movie(self, movie_id: int) -> bool:
        """Elimina una película (cambia su estado a inactivo)."""
        movies = self.db.load_data(self.movies_file)
        for i, movie in enumerate(movies):
            if movie['movie_id'] == movie_id:
                movies[i]['status'] = 'inactivo'
                self.db.save_data(self.movies_file, movies)
                return True
        return False
    
    def list_movies(self, active_only: bool = True) -> List[Dict]:
        """Lista todas las películas."""
        movies = self.db.load_data(self.movies_file)
        if active_only:
            return [m for m in movies if m['status'] == 'activo']
        return movies
    
    def search_movies(self, title: str = None, category: str = None, 
                        date: datetime = None, available: bool = True) -> List[Dict]:
        """Busca películas por diferentes criterios."""
        movies = self.db.load_data(self.movies_file)
        results = []
        
        for movie in movies:
            if movie['status'] != 'activo':
                continue
                
            match = True
            if title and title.lower() not in movie['title'].lower():
                match = False
            if category and category.lower() != movie['category'].lower():
                match = False
            if date:
                has_showtime = any(
                    datetime.strptime(st['date'], "%Y-%m-%d").date() == date.date()
                    for st in movie['showtimes']
                )
                if not has_showtime:
                    match = False
            if available:
                total_seats = sum(movie['available_seats'].values())
                if total_seats <= 0:
                    match = False
            
            if match:
                results.append(movie)
        
        return results