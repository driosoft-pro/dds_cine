from datetime import datetime, timedelta
from typing import Dict, List, Any

def create_initial_data() -> Dict[str, List[Dict[str, Any]]]:
    """Crea datos iniciales para el sistema."""
    
    # Fechas para funciones
    today = datetime.now()
    showtimes = []
    
    # Películas iniciales
    movies = [
        {
            "movie_id": 1,
            "title": "Avengers: Endgame",
            "release_year": 2019,
            "director": "Anthony y Joe Russo",
            "category": "ciencia ficción",
            "synopsis": "Los Vengadores se unen para revertir el Snap de Thanos.",
            "duration": 181,
            "age_rating": "PG-13",
            "language": "Ing",
            "origin": "Estados Unidos",
            "room_type": "3D",
            "showtimes": [st for st in showtimes if st['jornada'] != 'mañana'],
            "hall": "premium",
            "ticket_price": 25000,
            "available_seats": {"general": 80, "preferencial": 20},
            "status": "activo"
        },
        {
            "movie_id": 2,
            "title": "El Rey León",
            "release_year": 2019,
            "director": "Jon Favreau",
            "category": "aventura",
            "synopsis": "Remake del clásico animado de Disney.",
            "duration": 118,
            "age_rating": "PG",
            "language": "Esp",
            "origin": "Estados Unidos",
            "room_type": "2D",
            "showtimes": showtimes,
            "hall": "regular",
            "ticket_price": 18000,
            "available_seats": {"general": 100},
            "status": "activo"
        },
        {
            "movie_id": 3,
            "title": "Joker",
            "release_year": 2019,
            "director": "Todd Phillips",
            "category": "drama",
            "synopsis": "Origen del famoso villano de DC Comics.",
            "duration": 122,
            "age_rating": "R",
            "language": "Ing",
            "origin": "Estados Unidos",
            "room_type": "3D",
            "showtimes": [st for st in showtimes if st['jornada'] == 'noche'],
            "hall": "premium",
            "ticket_price": 25000,
            "available_seats": {"general": 80, "preferencial": 20},
            "status": "activo"
        }
    ]
    
    # Generar horarios para cada película
    for day in range(15):  # 15 días de programación
        current_date = (today + timedelta(days=day)).strftime('%Y-%m-%d')
        
        # Avengers: Endgame - Solo tarde y noche
        showtimes.extend([
            {
                "showtime_id": len(showtimes) + 1,
                "movie_id": 1,
                "date": current_date,
                "start_time": "15:00",
                "end_time": "18:00",
                "jornada": "tarde",
                "available_seats": {"general": 80, "preferencial": 20}
            },
            {
                "showtime_id": len(showtimes) + 2,
                "movie_id": 1,
                "date": current_date,
                "start_time": "20:00",
                "end_time": "23:00",
                "jornada": "noche",
                "available_seats": {"general": 80, "preferencial": 20}
            }
        ])
        
        # El Rey León - Todas las jornadas
        showtimes.extend([
            {
                "showtime_id": len(showtimes) + 1,
                "movie_id": 2,
                "date": current_date,
                "start_time": "09:00",
                "end_time": "12:00",
                "jornada": "mañana",
                "available_seats": {"general": 100}
            },
            {
                "showtime_id": len(showtimes) + 2,
                "movie_id": 2,
                "date": current_date,
                "start_time": "15:00",
                "end_time": "18:00",
                "jornada": "tarde",
                "available_seats": {"general": 100}
            },
            {
                "showtime_id": len(showtimes) + 3,
                "movie_id": 2,
                "date": current_date,
                "start_time": "20:00",
                "end_time": "23:00",
                "jornada": "noche",
                "available_seats": {"general": 100}
            }
        ])
        
        # Joker - Solo noche
        showtimes.append({
            "showtime_id": len(showtimes) + 1,
            "movie_id": 3,
            "date": current_date,
            "start_time": "20:00",
            "end_time": "23:00",
            "jornada": "noche",
            "available_seats": {"general": 80, "preferencial": 20}
        })
    
    # Salas de cine
    cinemas = [
        {
            "cinema_id": 1,
            "name": "Sala 2D",
            "room_type": "2D",
            "capacity": {"general": 100},
            "available_seats": {"general": 100}
        },
        {
            "cinema_id": 2,
            "name": "Sala 3D",
            "room_type": "3D",
            "capacity": {"general": 80, "preferencial": 20},
            "available_seats": {"general": 80, "preferencial": 20}
        }
    ]
    
    # Menú de comida
    food_menu = [
        # Combos de Crispetas
        {
            "item_id": 1,
            "code": "CCP",
            "category": "Combos de Crispetas",
            "product": "Combo Crispetas Pequeñas + Gaseosa Pequeña",
            "size": "Pequeño",
            "price": 15000,
            "description": "Crispetas pequeñas + gaseosa pequeña",
            "status": "activo"
        },
        {
            "item_id": 2,
            "code": "CCM",
            "category": "Combos de Crispetas",
            "product": "Combo Crispetas Medianas + Gaseosa Mediana",
            "size": "Mediano",
            "price": 22000,
            "description": "Crispetas medianas + gaseosa mediana",
            "status": "activo"
        },
        {
            "item_id": 3,
            "code": "CCG",
            "category": "Combos de Crispetas",
            "product": "Combo Crispetas Grandes + Gaseosa Grande",
            "size": "Grande",
            "price": 28000,
            "description": "Crispetas grandes + gaseosa grande",
            "status": "activo"
        },
        {
            "item_id": 4,
            "code": "CCF",
            "category": "Combos de Crispetas",
            "product": "Combo Crispetas Familiares + 2 Gaseosas Grandes",
            "size": "Familiar",
            "price": 35000,
            "description": "Crispetas familiares + 2 gaseosas grandes",
            "status": "activo"
        },

        # Snacks
        {
            "item_id": 5,
            "code": "CP",
            "category": "Snacks",
            "product": "Crispetas Pequeñas",
            "size": "Pequeño",
            "price": 8000,
            "description": "Porción individual de crispetas pequeñas",
            "status": "activo"
        },
        {
            "item_id": 6,
            "code": "CM",
            "category": "Snacks",
            "product": "Crispetas Medianas",
            "size": "Mediano",
            "price": 15000,
            "description": "Porción mediana de crispetas",
            "status": "activo"
        },
        {
            "item_id": 7,
            "code": "CG",
            "category": "Snacks",
            "product": "Crispetas Grandes",
            "size": "Grande",
            "price": 20000,
            "description": "Porción grande de crispetas",
            "status": "activo"
        },
        {
            "item_id": 8,
            "code": "NQ",
            "category": "Snacks",
            "product": "Nachos con Queso",
            "price": 18000,
            "description": "Nachos crujientes acompañados de queso derretido",
            "status": "activo"
        },
        {
            "item_id": 9,
            "code": "PC",
            "category": "Snacks",
            "product": "Perro Caliente",
            "price": 12000,
            "description": "Perro caliente clásico con salsas al gusto",
            "status": "activo"
        },
        {
            "item_id": 10,
            "code": "HS",
            "category": "Snacks",
            "product": "Hamburguesa Sencilla",
            "price": 15000,
            "description": "Hamburguesa sencilla con carne, queso y vegetales",
            "status": "activo"
        },

        # Bebidas
        {
            "item_id": 11,
            "code": "GP",
            "category": "Bebidas",
            "product": "Gaseosa Pequeña",
            "size": "Pequeño",
            "price": 6000,
            "description": "Gaseosa pequeña 350ml",
            "status": "activo"
        },
        {
            "item_id": 12,
            "code": "GM",
            "category": "Bebidas",
            "product": "Gaseosa Mediana",
            "size": "Mediano",
            "price": 8000,
            "description": "Gaseosa mediana 500ml",
            "status": "activo"
        },
        {
            "item_id": 13,
            "code": "GG",
            "category": "Bebidas",
            "product": "Gaseosa Grande",
            "size": "Grande",
            "price": 10000,
            "description": "Gaseosa grande 750ml",
            "status": "activo"
        },
        {
            "item_id": 14,
            "code": "AE",
            "category": "Bebidas",
            "product": "Agua Embotellada",
            "price": 5000,
            "description": "Botella de agua natural 500ml",
            "status": "activo"
        },
        {
            "item_id": 15,
            "code": "JC",
            "category": "Bebidas",
            "product": "Jugo en Caja",
            "price": 7000,
            "description": "Jugo de frutas en caja individual",
            "status": "activo"
        },

        # Dulces
        {
            "item_id": 16,
            "code": "CHOC",
            "category": "Dulces",
            "product": "Chocolatina",
            "price": 4000,
            "description": "Chocolatina estándar",
            "status": "activo"
        },
        {
            "item_id": 17,
            "code": "PDD",
            "category": "Dulces",
            "product": "Paquete de Dulces",
            "price": 6000,
            "description": "Surtido de dulces variados",
            "status": "activo"
        }
    ]
    
    # Usuarios iniciales
    users = [
        {
            "user_id": 1,
            "username": "admin",
            "identification": "123456789",
            "name": "Admin00",
            "email": "admin@ddscine.com",
            "birth_date": "1980-01-01",
            "password": "3b612c75a7b5048a435fb6ec81e52ff92d6d795a8b5a9c17070f6a63c97a53b2",  # "Admin123" en SHA-256
            "status": "activo",
            "is_admin": True
        },
        {
            "user_id": 2,
            "username": "client",
            "identification": "987654321",
            "name": "Samuel Mosquera",
            "email": "samu@ddscine.com",
            "birth_date": "1990-05-15",
            "password": "b7827b17b0821b354fabf438d73691c2bf467af7a44c374f8c505a5ee08b0d5d",  # "Client123" en SHA-256
            "status": "activo",
            "is_admin": False
        }
    ]
    
    return {
        "movies.json": movies,
        "cinemas.json": cinemas,
        "food_menu.json": food_menu,
        "users.json": users,
        "tickets.json": [],
        "reservations.json": [],
        "payments.json": [],
        "showtimes.json": showtimes
    }