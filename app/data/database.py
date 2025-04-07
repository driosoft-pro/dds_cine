import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from models.user import User, Client, Admin
from models.movie import Movie, TwoDMovie, ThreeDMovie

class Database:
    """Clase para manejar la base de datos JSON del sistema."""
    
    def __init__(self):
        self.data_file = Path(__file__).parent / "data.json"
        self.data = {
            "users": [],
            "movies": [],
            "screenings": [],
            "tickets": [],
            "reservations": [],
            "food_menus": []
        }
    
    def initialize(self):
        try:
            # Verificar si el archivo de datos existe
            if not self.data_file.exists():
                print("Archivo data.json no encontrado. Creando uno nuevo...")
                self._save_data()
            else:
                print("Cargando datos desde data.json...")
                self._load_data()
            
            # Crear admin por defecto si no existe
            if not any(user['type'] == 'admin' for user in self.data['users']):
                print("No se encontró un administrador. Creando administrador por defecto...")
                admin_data = {
                    "user_id": 1,
                    "username": "admin",
                    "identification": "12345678",
                    "name": "Administrador",
                    "email": "admin@cinema.com",
                    "birth_date": "1995-10-05",
                    "password": "admin123",
                    "status": "active",
                    "type": "admin",
                }
                self.data['users'].append(admin_data)
                self._save_data()
            
            # Crear películas por defecto si no existen
            if not self.data['movies']:
                print("No se encontraron películas. Creando películas por defecto...")
                self._create_default_movies()
                self._save_data()
            else:
                print("Películas ya existentes en la base de datos.")
        
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def _load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
    
    def _save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)
    
    def save_user(self, user: User):
        user_dict = user.to_dict()
        
        # Verificar si el usuario ya existe
        for i, existing_user in enumerate(self.data['users']):
            if existing_user['user_id'] == user.user_id:
                self.data['users'][i] = user_dict
                break
        else:
            self.data['users'].append(user_dict)
        
        self._save_data()
    
    def get_user(self, user_id: int) -> Optional[User]:
        for user_data in self.data['users']:
            if user_data['user_id'] == user_id:
                return self._dict_to_user(user_data)
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        for user_data in self.data['users']:
            if user_data['username'] == username:
                return self._dict_to_user(user_data)
        return None
    
    def get_user_by_identification(self, identification: str) -> Optional[User]:
        for user_data in self.data['users']:
            if user_data['identification'] == identification:
                return self._dict_to_user(user_data)
        return None
    
    def get_all_users(self) -> List[User]:
        return [self._dict_to_user(user_data) for user_data in self.data['users']]
    
    def _dict_to_user(self, user_data: dict) -> Optional[User]:
        if user_data['type'] == 'client':
            return Client(
                user_id=user_data['user_id'],
                username=user_data['username'],
                identification=user_data['identification'],
                name=user_data['name'],
                email=user_data['email'],
                birth_date=user_data['birth_date'],
                password=user_data['password'],
                status=user_data['status']
            )
        else:
            return Admin(
                user_id=user_data['user_id'],
                username=user_data['username'],
                identification=user_data['identification'],
                name=user_data['name'],
                email=user_data['email'],
                birth_date=user_data['birth_date'],
                password=user_data['password'],
                status=user_data['status']
            )

    def _generate_showtimes(self, days: int, is_3d: bool = False) -> List[dict]:
        """Genera horarios de presentación para los próximos días."""
        showtimes = []
        base_time = datetime.now()
        
        for day in range(days):
            date = (base_time + timedelta(days=day)).strftime("%Y-%m-%d")
            
            if is_3d:
                # Horarios para 3D (menos funciones)
                showtimes.extend([
                    {"date": date, "time": "16:00", "session": "tarde"},
                    {"date": date, "time": "20:00", "session": "noche"}
                ])
            else:
                # Horarios para 2D (más funciones)
                showtimes.extend([
                    {"date": date, "time": "12:00", "session": "matiné"},
                    {"date": date, "time": "15:00", "session": "tarde"},
                    {"date": date, "time": "18:00", "session": "tarde"},
                    {"date": date, "time": "21:00", "session": "noche"}
                ])
        
        return showtimes    
    
    def save_movie(self, movie: Movie):
        movie_dict = movie.to_dict()
        
        # Verificar si la película ya existe
        for i, existing_movie in enumerate(self.data['movies']):
            if existing_movie['movie_id'] == movie.movie_id:
                self.data['movies'][i] = movie_dict
                break
        else:
            self.data['movies'].append(movie_dict)
        
        self._save_data()

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        for movie_data in self.data['movies']:
            if movie_data['movie_id'] == movie_id:
                return self._dict_to_movie(movie_data)
        return None

    def get_all_movies(self) -> List[Movie]:
        return [self._dict_to_movie(movie_data) for movie_data in self.data['movies']]

    def get_active_movies(self) -> List[Movie]:
        """Obtiene todas las películas activas."""
        return [self._dict_to_movie(m) for m in self.data['movies'] 
                if m.get('status', 'active') == 'active']

    def get_movies_by_status(self, status: str) -> List[Movie]:
        """Obtiene películas por estado (active/inactive)."""
        return [self._dict_to_movie(m) for m in self.data['movies'] 
                if m.get('status', 'active') == status]

    def _dict_to_movie(self, movie_data: dict) -> Optional[Movie]:
        if 'type' not in movie_data or movie_data['type'] == 'regular':
            return TwoDMovie(
                movie_id=movie_data['movie_id'],
                title=movie_data['title'],
                release_year=movie_data['release_year'],
                director=movie_data['director'],
                gender=movie_data['gender'],
                synopsis=movie_data['synopsis'],
                duration=movie_data['duration'],
                rating=movie_data['rating'],
                language=movie_data['language'],
                origin=movie_data['origin'],
                showtimes=movie_data['showtimes'],
                hall=movie_data['hall'],
                status=movie_data.get('status', 'active')
                
            )
        else:
            return ThreeDMovie(
                movie_id=movie_data['movie_id'],
                title=movie_data['title'],
                release_year=movie_data['release_year'],
                director=movie_data['director'],
                gender=movie_data['gender'],
                synopsis=movie_data['synopsis'],
                duration=movie_data['duration'],
                rating=movie_data['rating'],
                language=movie_data['language'],
                origin=movie_data['origin'],
                showtimes=movie_data['showtimes'],
                hall=movie_data['hall'],
                status=movie_data.get('status', 'active')
            )

    def _create_default_movies(self):
        """Crea películas por defecto y las agrega a la base de datos."""
        default_movies = [
            {
                "movie_id": 1,
                "title": "El Rey León",
                "release_year": 2019,
                "director": "Jon Favreau",
                "gender": "Animación",
                "synopsis": "Remake del clásico animado sobre el ciclo de la vida en la sabana africana.",
                "duration": 118,
                "rating": "PG",
                "language": "Español",
                "origin": "EE.UU.",
                "showtimes": self._generate_showtimes(3),
                "type": "2D",
                "hall": "regular",
                "status": "active"
            },
            {
                "movie_id": 2,
                "title": "Parásitos",
                "release_year": 2019,
                "director": "Bong Joon-ho",
                "gender": "Drama",
                "synopsis": "Una familia pobre que se infiltra en un hogar adinerado con consecuencias inesperadas.",
                "duration": 132,
                "rating": "R",
                "language": "Español",
                "origin": "Corea del Sur",
                "showtimes": self._generate_showtimes(2),
                "type": "3D",
                "hall": "regular",
                "status": "active"
            },
            {
                "movie_id": 3,
                "title": "Avatar",
                "release_year": 2009,
                "director": "James Cameron",
                "gender": "Ciencia Ficción",
                "synopsis": "Un marine parapléjico es enviado a la luna Pandora en una misión única.",
                "duration": 162,
                "rating": "PG-13",
                "language": "Español",
                "origin": "EE.UU.",
                "showtimes": self._generate_showtimes(4, True),
                "type": "3D",
                "hall": "premium",
                "status": "active"
            }
        ]
        
        for movie in default_movies:
            self.data['movies'].append(movie)
        print(f"{len(default_movies)} películas por defecto agregadas.")