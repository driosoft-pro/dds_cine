import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from models.user import User, Client, Admin
from models.movie import Movie, TwoDMovie, ThreeDMovie
from models.food_menu import MenuItem

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
                
            # Crear ítems de menú por defecto si no existen
            if not self.data['food_menus']:
                print("No se encontraron ítems de menú. Creando ítems por defecto...")
                self._create_default_food_items()
                self._save_data()
            else:
                print("Ítems de menú ya existentes en la base de datos.")
        
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def _load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
    
    def _save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)  # Asegurar que los caracteres especiales se guarden correctamente
    
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
                    {"date": date, "time": "12:00", "session": "mañana"},
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
        
    def save_food_item(self, item: MenuItem) -> bool:
        """Guarda un ítem del menú"""
        try:
            item_dict = item.to_dict()
            
            # Actualizar si existe
            for i, existing in enumerate(self.data['food_menus']):
                if existing['item_id'] == item.item_id:
                    self.data['food_menus'][i] = item_dict
                    break
            else:
                self.data['food_menus'].append(item_dict)
                
            self._save_data()
            return True
        except Exception:
            return False

    def get_food_item(self, item_id: int) -> Optional[MenuItem]:
        """Obtiene un ítem del menú por ID"""
        for item_data in self.data['food_menus']:
            if item_data['item_id'] == item_id:
                return self._dict_to_food_item(item_data)
        return None

    def get_all_food_items(self) -> List[MenuItem]:
        """Obtiene todos los ítems del menú"""
        return [self._dict_to_food_item(item) for item in self.data['food_menus']]

    def _dict_to_food_item(self, item_data: dict) -> MenuItem:
        """Convierte diccionario a objeto MenuItem"""
        from models.food_menu import Combo, Snack, Drink, Candy
        
        item_type = item_data.get('type', 'base')
        
        if item_type == 'combo':
            return Combo(
                item_id=item_data['item_id'],
                code=item_data['code'],
                product=item_data['product'],
                size=item_data['size'],
                price=item_data['price'],
                included_items=item_data['included_items'],
                status=item_data.get('status', 'active')
            )
        elif item_type == 'snack':
            return Snack(
                item_id=item_data['item_id'],
                code=item_data['code'],
                product=item_data['product'],
                size=item_data['size'],
                price=item_data['price'],
                status=item_data.get('status', 'active')
            )
        elif item_type == 'drink':
            return Drink(
                item_id=item_data['item_id'],
                code=item_data['code'],
                product=item_data['product'],
                size=item_data['size'],
                price=item_data['price'],
                status=item_data.get('status', 'active')
            )
        elif item_type == 'candy':
            return Candy(
                item_id=item_data['item_id'],
                code=item_data['code'],
                product=item_data['product'],
                price=item_data['price'],
                status=item_data.get('status', 'active')
            )
        else:
            return MenuItem(
                item_id=item_data['item_id'],
                code=item_data['code'],
                category=item_data['category'],
                product=item_data['product'],
                size=item_data['size'],
                price=item_data['price'],
                status=item_data.get('status', 'active')
            )

    def _create_default_food_items(self):
        """Crea ítems de menú por defecto más completos"""
        from models.food_menu import Combo, Snack, Drink, Candy
        
        default_items = [
            # Combos (4 items)
            Combo(1, "CP-001", "Combo Familiar", "Familiar", 35000,
                    ["Crispetas Grandes", "2 Gaseosas Grandes", "1 Nachos"]),
            Combo(2, "CP-002", "Combo Pareja", "Mediano", 28000,
                    ["Crispetas Medianas", "2 Gaseosas Medianas"]),
            Combo(3, "CP-003", "Combo Individual", "Pequeño", 18000,
                    ["Crispetas Pequeñas", "1 Gaseosa Pequeña"]),
            Combo(4, "CP-004", "Combo Infantil", "Pequeño", 15000,
                    ["Crispetas Pequeñas", "1 Jugo", "1 Chocolatina"]),
            
            # Snacks (5 items)
            Snack(5, "SN-001", "Crispetas Grandes", "Grande", 20000),
            Snack(6, "SN-002", "Crispetas Medianas", "Mediano", 15000),
            Snack(7, "SN-003", "Crispetas Pequeñas", "Pequeño", 8000),
            Snack(8, "SN-004", "Nachos con Queso", "Mediano", 18000),
            Snack(9, "SN-005", "Perro Caliente", "Estándar", 12000),
            
            # Bebidas (5 items)
            Drink(10, "BD-001", "Gaseosa Grande", "Grande", 10000),
            Drink(11, "BD-002", "Gaseosa Mediana", "Mediano", 8000),
            Drink(12, "BD-003", "Gaseosa Pequeña", "Pequeño", 6000),
            Drink(13, "BD-004", "Agua Mineral", "500ml", 5000),
            Drink(14, "BD-005", "Jugo Natural", "350ml", 7000),
            
            # Dulces (4 items)
            Candy(15, "DC-001", "Chocolatina", 4000),
            Candy(16, "DC-002", "Gomitas", 6000),
            Candy(17, "DC-003", "Paleta de Caramelo", 3000),
            Candy(18, "DC-004", "Paquete de Galletas", 8000)
        ]
        
        # Asegurarse que los combos tengan included_items
        for item in default_items:
            if isinstance(item, Combo) and not hasattr(item, 'included_items'):
                item.included_items = []
            self.data['food_menus'].append(item.to_dict())